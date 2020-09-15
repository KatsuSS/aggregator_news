from app.utils.parser import Requestor
from app.models import Resource, News


#TODO: Изменить добавление постов в БД?
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
        afisha = Resource.query.get(1)
        village = Resource.query.get(2)
        vc = Resource.query.get(3)
        for new in news:
            for val in new.values():
                new_post = News.query.filter_by(link=val['link']).first()
                if new_post is None:
                    if val['name'] == "afisha":
                        post = News(header=val['title'], link=val['link'], source=afisha, timestamp=val['time'])
                        db.session.add(post)
                    elif val['name'] == "the-village":
                        post = News(header=val['title'], link=val['link'], source=village, timestamp=val['time'])
                        db.session.add(post)
                    elif val['name'] == "vc":
                        post = News(header=val['title'], link=val['link'], source=vc, timestamp=val['time'])
                        db.session.add(post)
        db.session.commit()
