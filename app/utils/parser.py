from bs4 import BeautifulSoup
import aiohttp
import asyncio
from app.utils.logger import init_logger
from typing import List
from app.utils.services import format_time, format_time_new, _get_post_attributes_vc, _get_posts_vc, \
    _get_post_attributes_afisha, _get_posts_afisha, _get_posts_village, _get_post_attributes_village


logger = init_logger()


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
                # return self._get_page_info(page_content, url)
                data = self._get_page_info(page_content, url)
        except aiohttp.ClientError as err:
            logger.error(f"Connected er: {err}")
            print(err)

        try:
            for _, post in data.items():
                async with session.get(post["link"]) as response:
                    page_content = await response.text()
                    post["body"] = self._get_page_info(page_content, url, body=True)
        except aiohttp.ClientError as err:
            logger.error(f"Connected er: {err}")
            print(err)
        return data

    def _get_page_info(self, page_content: str, url: str, body: bool = False) -> dict:
        """
        Вызов нужного парсера в соответсвии со СМИ
        :param page_content: содержимое страницы
        :param url: url адрес ресурса
        :return: распарсенные данные
        """
        soup = BeautifulSoup(page_content, "lxml")
        if "the-village" in url:
            return self._get_info_village(soup) if not body else self._get_post_body_village(soup)
        elif "afisha" in url:
            return self._get_info_afisha(soup) if not body else self._get_post_body_afisha(soup)
        elif "vc" in url:
            return self._get_info_vc(soup) if not body else self._get_post_body_vc(soup)
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


    def _get_post_body_village(self, soup) -> str:
        # TODO: ДОДЕЛАТЬ
        try:
            ads = soup.find('div', class_="stk-post").find_all('p', class_='stk-reset')
        except AttributeError as e:
            logger.error(f"Tags body changed village: {e}")
            ads = None
        body = []
        break_space = u'\xa0'
        if ads:
            for ad in ads:
                body.append(ad.getText().strip().replace(break_space, ' '))
        return " ".join(body)


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


    def _get_post_body_afisha(self, soup) -> str:
        # TODO: ДОДЕЛАТЬ
        try:
            ads = soup.find('div', class_="news-body").find_all('div', class_='news-paragraph js-mediator-article')
        except AttributeError as e:
            logger.error(f"Tags body changed afisha: {e}")
            ads = None
        body = []
        break_space = u'\xa0'
        if ads:
            for ad in ads:
                for p in ad.find_all('p'):
                    body.append(p.getText().strip().replace(break_space, ' '))
        return " ".join(body)


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
                except AttributeError:
                    continue
                create_time = format_time(create_time)
                data[key] = {"title": title,
                             "name": "vc",
                             "link": link,
                             "time": create_time}
        return data


    def _get_post_body_vc(self, soup) -> str:
        # TODO: ДОДЕЛАТЬ
        try:
            ads = soup.find('div', class_="content content--full").find_all('div', class_='l-island-a')
        except AttributeError as e:
            logger.error(f"Tags body changed village: {e}")
            ads = None
        body = []
        break_space = u'\xa0'
        if ads:
            for ad in ads:
                for p in ad.find_all('p'):
                    body.append(p.getText().strip().replace(break_space, ' '))
                for li in ad.find_all('li'):
                    body.append(li.getText().strip().replace(break_space, ' '))
        return " ".join(body)


    async def _create_task(self) -> list:
        """
        Создание тасков для выполнения
        :return:
        """
        tasks = []
        async with aiohttp.ClientSession() as session:
            for page in self.url:
                task = asyncio.create_task(self._get_page(session, page))
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


# if __name__ == "__main__":
#     res = Requestor(["https://daily.afisha.ru/news/", "https://www.the-village.ru/news", "https://vc.ru/"])
#     news = res.get_request()
#     from pprint import pprint
#     pprint(news)
