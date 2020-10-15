from app.utils.parser import Requestor
from app.models import Resource, News
from app.utils.logger import init_logger


logger = init_logger()


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
                        db.session.add(_create_new_in_db(val, resource[0]))
                    elif val['name'] == "the-village":
                        db.session.add(_create_new_in_db(val, resource[1]))
                    elif val['name'] == "vc":
                        db.session.add(_create_new_in_db(val, resource[2]))
        try:
            db.session.commit()
        except Exception as e:
            print("Ошибка добавления в БД")
            logger.error(f"Ошибка добавления в БД: {e}")


def _create_new_in_db(new, source):
    """Создание новости(поста) с параметрами"""
    return News(header=new['title'], link=new['link'], source=source, timestamp=new['time'])
