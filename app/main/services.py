from flask import url_for, request, current_app
from flask_sqlalchemy import Pagination
from app.models import News, Resource
from datetime import datetime, timedelta
from typing import Dict


def create_next_prev_page(resource: str, news: Pagination) -> (str, str):
    """Получить ссылку на новую/предыдущую страницу"""
    next_url = url_for(f'main.{resource}', page=news.next_num) if news.has_next else None
    prev_url = url_for(f'main.{resource}', page=news.prev_num) if news.has_prev else None
    return next_url, prev_url


def get_news_per_page(resource_id: int) -> Pagination:
    """Получить разделение новостей на страницы"""
    page = request.args.get('page', 1, type=int)
    return News.query.filter_by(user_id=resource_id).order_by(News.timestamp.desc())\
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)


def get_news_for_last_day() -> list:
    """Получить все новости за последние 24 часа"""
    since = datetime.now() - timedelta(hours=24)
    return News.query.filter(News.timestamp > since).order_by(News.timestamp.desc()).all()


def structure_news_by_resource(news: list) -> Dict:
    """Структурирование новостей по СМИ"""
    structured_news = {
        'afisha': {"news": [],
                   "link": ""},
        'village': {"news": [],
                    "link": ""},
        'vc': {"news": [],
               "link": ""}
    }
    resources = Resource.query.all()
    for new in news:
        if new.source.title == 'afisha':
            structured_news['afisha']["news"].append(new)
        elif new.source.title == 'the-village':
            structured_news['village']["news"].append(new)
        elif new.source.title == 'vc':
            structured_news['vc']["news"].append(new)
    structured_news['afisha']["link"] = resources[0].home_page
    structured_news['village']["link"] = resources[1].home_page
    structured_news['vc']["link"] = resources[2].home_page
    return structured_news


def get_resource_news_on_the_page(name_resource):
    resource_id = current_app.config['RESOURCE_ID'][request.path[1:]]
    news_per_page = get_news_per_page(resource_id)
    next_url, prev_url = create_next_prev_page(name_resource, news_per_page)
    return news_per_page, next_url, prev_url
