from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
# from app.parseinfo.parsing import Requestor
from app.models import Resource, News


base_url = ["https://daily.afisha.ru/news/", "https://www.the-village.ru/news"]


def add_news():
    news = News.query.all()
    # resourse = Requestor(base_url)
    # news = resourse.get_request()
    # print(news)

add_news()
#
# scheduler = AsyncIOScheduler()
# scheduler.add_job()
# scheduler.start()


