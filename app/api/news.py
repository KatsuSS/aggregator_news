from app.api import bp
from flask import jsonify
from app.models import News, Resource
from flask import request
from app.api.services import get_number_posts_per_page


@bp.route('/news/<int:id>', methods=['GET'])
def get_new(id: int) -> dict:
    return jsonify(News.query.get_or_404(id).to_dict())


@bp.route('/news', methods=['GET'])
def get_news() -> dict:
    page, per_page = get_number_posts_per_page(request)
    data = News.to_collection_dict(News.query.order_by(News.timestamp.desc()), page, per_page, 'api.get_news')
    return jsonify(data)


@bp.route('/news/resource/<int:id>', methods=['GET'])
def get_resource_news(id: int) -> dict:
    resource = Resource.query.get_or_404(id)
    page, per_page = get_number_posts_per_page(request)
    data = News.to_collection_dict(News.query.filter_by(user_id=id).order_by(News.timestamp.desc()),
                                   page, per_page, 'api.get_news')
    return jsonify(data)
