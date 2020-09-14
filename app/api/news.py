from app.api import bp
from flask import jsonify
from app.models import News, Resource
from flask import request


@bp.route('/news/<int:id>', methods=['GET'])
def get_new(id):
    return jsonify(News.query.get_or_404(id).to_dict())


@bp.route('/news', methods=['GET'])
def get_news():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = News.to_collection_dict(News.query.order_by(News.timestamp.desc()), page, per_page, 'api.get_news')
    return jsonify(data)


@bp.route('/news/resource/<int:id>', methods=['GET'])
def get_resource_news(id):
    resource = Resource.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = News.to_collection_dict(News.query.filter_by(user_id=id).order_by(News.timestamp.desc()),
                                   page, per_page, 'api.get_news')
    return jsonify(data)
