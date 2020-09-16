from app.utils.parser import Requestor
from app.models import Resource, News


def add_news(app, db) -> None:
    """
    Служит для APScheduler-а, для сбора данных и загрузки в БД
    :param app: Flask приложение
    :param db: БД
    :return:
    """
    res = Requestor(["https://daily.afisha.ru/news/", "https://www.the-village.ru/news", "https://vc.ru/"])
    news = res.get_request()
    with app.app_context():
        resource = Resource.query.all()
        last_news = News.query.order_by(News.timestamp.desc()).first()
        for new in news:
            for val in new.values():
                if val['time'] > last_news.timestamp:
                    if val['name'] == "afisha":
                        post = News(header=val['title'], link=val['link'], source=resource[0], timestamp=val['time'])
                        db.session.add(post)
                    elif val['name'] == "the-village":
                        post = News(header=val['title'], link=val['link'], source=resource[1], timestamp=val['time'])
                        db.session.add(post)
                    elif val['name'] == "vc":
                        post = News(header=val['title'], link=val['link'], source=resource[2], timestamp=val['time'])
                        db.session.add(post)
        db.session.commit()
