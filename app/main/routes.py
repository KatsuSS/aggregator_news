from flask import render_template, flash, redirect, url_for, request, current_app
from app.app import db
from app.models import News, Resource
from app.main import bp
from app.parseinfo.parsing import Requestor


@bp.route('/', methods=['GET'])
def index():
    res = Requestor(["https://daily.afisha.ru/news/", "https://www.the-village.ru/news"])
    news = res.get_request()
    from pprint import pprint
    pprint(news)
    afisha = Resource.query.get(1)
    village = Resource.query.get(2)
    for new in news:
        for val in new.values():
            new_post = News.query.filter_by(header=val['title']).first()
            if new_post is None:
                if val['name'] == "afisha":
                    post = News(header=val['title'], link=val['link'], source=afisha)
                    db.session.add(post)
                elif val['name'] == "the-village":
                    post = News(header=val['title'], link=val['link'], source=village)
                    db.session.add(post)
    db.session.commit()
    return render_template("base.html", title="Test")


@bp.route('/table', methods=['GET'])
def create_table():
    resource = Resource.query.all()
    print(resource)
    from pprint import pprint
    news = News.query.all()
    pprint(news)
    return render_template("base.html", title="Test")