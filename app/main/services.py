from flask import url_for, request, current_app
from flask_sqlalchemy import Pagination
from app.models import News


def create_next_prev_page(resource: str, news: Pagination) -> (str, str):
    next_url = url_for(f'main.{resource}', page=news.next_num) if news.has_next else None
    prev_url = url_for(f'main.{resource}', page=news.prev_num) if news.has_prev else None
    return next_url, prev_url


def get_news_per_page(resource_id: int) -> Pagination:
    page = request.args.get('page', 1, type=int)
    return News.query.filter_by(user_id=resource_id).order_by(News.timestamp.desc())\
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)

