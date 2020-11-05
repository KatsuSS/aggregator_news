from datetime import datetime, timedelta
import re
from app.utils.logger import init_logger


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
