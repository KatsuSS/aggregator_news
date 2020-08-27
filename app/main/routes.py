from flask import render_template, flash, redirect, url_for, request, current_app
from app.app import db
from app.models import News, Resource
from app.main import bp
from datetime import datetime, timedelta


@bp.route('/', methods=['GET'])
def create_table():
    since = datetime.now() - timedelta(hours=24)
    news_afisha, news_village = [], []
    news = News.query.filter(News.timestamp > since).order_by(News.timestamp.desc()).all()
    for new in news:
        if new.source.title == 'afisha':
            news_afisha.append(new)
        elif new.source.title == 'the-village':
            news_village.append(new)
    return render_template("table.html", title="Test", news_afisha=news_afisha, news_village=news_village)
