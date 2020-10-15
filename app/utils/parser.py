from bs4 import BeautifulSoup
import aiohttp
import asyncio
from datetime import datetime, timedelta
import re
from app.utils.logger import init_logger
from typing import List


logger = init_logger()


def format_time_new(create_time: str) -> datetime:
    """
    Переформатирует время из (y-m-dTh:m:00.000+03:00) в формат (y-m-d h:m:00)
    :param create_time: исходная строка(время)
    :return: время формата y-m-d h:m:00
    """
    try:
        time = re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', create_time).group(0).replace("T", " ")
    except AttributeError as e:
        time = datetime.now()
        logger.info(f"Не получилось выделить время {e}")
    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    return time


def format_time(create_time: str) -> datetime:
    """
    Переформатирует время из (h:m) в формат (y-m-d h:m:00)
    :param create_time: исходная строка(время)
    :return: время формата y-m-d h:m:00
    """
    if "ВЧЕРА" in create_time:
        time = datetime.now() - timedelta(days=1)
    else:
        time = datetime.now()
    try:
        hour, minute = re.search(r'\d{1,2}:\d{2}', create_time).group(0).split(':')
    except AttributeError as e:
        logger.info(f"Не получилось выделить время {e}")
        hour, minute = time.hour, time.minute
    time = datetime(year=time.year, month=time.month, day=time.day, hour=int(hour), minute=int(minute))
    return time


class Requestor:
    """
    Класс для парсинга(сбора) информации с СМИ
    """
    def __init__(self, url: List[str]):
        """
        :param url: список интернет ресурсов
        """
        self.url = url

    async def _get_page(self, session, url: str) -> dict:
        """
        Получение страницы и вывод нужной информации
        :param session: текущая сессия
        :param url: url-адрес страницы
        :return: полученные распарсеные данные
        """
        try:
            async with session.get(url) as response:
                page_content = await response.text()
                return self._get_page_info(page_content, url)
        except aiohttp.ClientError as err:
            logger.error(f"Connected er: {err}")
            print(err)

    def _get_page_info(self, page_content: str, url: str) -> dict:
        """
        Вызов нужного парсера в соответсвии со СМИ
        :param page_content: содержимое страницы
        :param url: url адрес ресурса
        :return: распарсенные данные
        """
        soup = BeautifulSoup(page_content, "lxml")
        if "the-village" in url:
            return self._get_info_village(soup)
        elif "afisha" in url:
            return self._get_info_afisha(soup)
        elif "vc" in url:
            return self._get_info_vc(soup)
        else:
            logger.info(f"Пустая страница")
            return {}

    def _get_info_village(self, soup) -> dict:
        """
        Парсинг нужных данных со страницы the-village
        :param soup: BS4
        :return: dict данных
        """
        url = "https://www.the-village.ru"
        data = {}
        ads = _get_posts_village(soup)
        if ads:
            for key, ad in enumerate(ads):
                try:
                    title, link, create_time = _get_post_attributes_village(ad)
                except AttributeError:
                    continue
                create_time = format_time_new(create_time)
                data[key] = {"title": title,
                             "name": "the-village",
                             "link": url + link,
                             "time": create_time}
        return data

    def _get_info_afisha(self, soup) -> dict:
        """
        Парсинг нужных данных со страницы afisha
        :param soup: BS4
        :return: dict данных
        """
        url = "https://daily.afisha.ru"
        data = {}
        ads = _get_posts_afisha(soup)
        if ads:
            for key, ad in enumerate(ads):
                try:
                    title, link, create_time = _get_post_attributes_afisha(ad)
                except AttributeError:
                    continue
                create_time = format_time(create_time)
                data[key] = {"title": title,
                             "name": "afisha",
                             "link": url + link,
                             "time": create_time}
        return data

    def _get_info_vc(self, soup):
        """
        Парсинг нужных данных со страницы vc.ru
        :param soup: BS4
        :return: dict данных
        """
        data = {}
        ads = _get_posts_vc(soup)
        if ads:
            for key, ad in enumerate(ads):
                try:
                    title, link, create_time = _get_post_attributes_vc(ad)
                except AttributeError as e:
                    continue
                create_time = format_time(create_time)
                data[key] = {"title": title,
                             "name": "vc",
                             "link": link,
                             "time": create_time}
        return data

    async def _create_task(self) -> list:
        """
        Создание тасков для выполнения
        :return:
        """
        tasks = []
        async with aiohttp.ClientSession() as session:
            for page in self.url:
                task = asyncio.ensure_future(self._get_page(session, page))
                tasks.append(task)
            result = await asyncio.gather(*tasks)
            return result

    def get_request(self) -> list:
        """
        Запуск
        :return:
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(self._create_task())
        return data


def _get_posts_village(soup):
    """
    Получть все посты на странице
    """
    try:
        ads = soup.find('div', class_="application-components-base-Layout--Layout__gridColumnLeft3x") \
            .find_all('div', class_='application-components-base-NewsBlockCard--NewsBlockCard__container')
    except AttributeError as e:
        logger.error(f"Tags changed village: {e}")
        ads = None
    return ads


def _get_post_attributes_village(ad) -> (str, str, str):
    """
    Получить атрибуты поста: название, ссылку и время
    """
    break_space = u'\xa0'
    try:
        title = ad.find("h3", class_="application-components-base-NewsBlockCard--NewsBlockCard__title") \
            .getText().strip().replace(break_space, ' ')
        link = ad.find("a", class_="application-components-base-NewsBlockCard--NewsBlockCard__link")["href"]
        create_time = ad.find("div", class_="application-components-base-Layout--Layout__hidden") \
            .find("time").getText().strip()
    except AttributeError as e:
        logger.error(f"Tags changed village: {e}")
        raise AttributeError
    return title, link, create_time


def _get_posts_afisha(soup):
    """
    Получть все посты на странице
    """
    try:
        ads = soup.find('div', class_="news-feed").find('div', attrs={"data-page-counter": "1"})\
            .find_all("div", class_="news-feed__item")
    except AttributeError as e:
        logger.error(f"Tags changed afisha: {e}")
        ads = None
    return ads


def _get_post_attributes_afisha(ad) -> (str, str, str):
    """
    Получить атрибуты поста: название, ссылку и время
    """
    break_space = u'\xa0'
    try:
        title = ad.find("a", class_="news-feed__title").getText().strip().replace(break_space, ' ')
        create_time = ad.find("span", class_="news-feed__datetime").getText().strip()
        link = ad.find("a", class_="news-feed__title")['href']
    except AttributeError as e:
        logger.error(f"Tags changed afisha: {e}")
        raise AttributeError
    return title, link, create_time


def _get_posts_vc(soup):
    """
    Получть все посты на странице
    """
    try:
        ads = soup.find('div', class_="news_widget__content__inner").find_all("div", class_="news_item")
    except AttributeError as e:
        logger.error(f"Tags changed vc: {e}")
        ads = None
    return ads


def _get_post_attributes_vc(ad) -> (str, str, str):
    """
    Получить атрибуты поста: название, ссылку и время
    """
    try:
        title = ad.find("a", class_="news_item__title").getText().strip()
        create_time = ad.find("time", class_="time").getText().strip()
        link = ad.find("a", class_="news_item__title")['href']
    except AttributeError as e:
        logger.error(f"Tags changed vc: {e}")
        raise AttributeError
    return title, link, create_time
