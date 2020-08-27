from app.parseinfo.parsing import Requestor
from app.models import Resource, News


base_url = ["https://daily.afisha.ru/news/", "https://www.the-village.ru/news"]


def add_news(app, db):
    res = Requestor(["https://daily.afisha.ru/news/", "https://www.the-village.ru/news"])
    news = res.get_request()
    with app.app_context():
        afisha = Resource.query.get(1)
        village = Resource.query.get(2)
        for new in news:
            for val in new.values():
                new_post = News.query.filter_by(header=val['title']).first()
                if new_post is None:
                    if val['name'] == "afisha":
                        post = News(header=val['title'], link=val['link'], source=afisha, timestamp=val['time'])
                        db.session.add(post)
                    elif val['name'] == "the-village":
                        post = News(header=val['title'], link=val['link'], source=village, timestamp=val['time'])
                        db.session.add(post)
        db.session.commit()




