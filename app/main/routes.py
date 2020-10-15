from flask import render_template, request, current_app
from app.main import bp
from app.app import cache
from app.main.services import create_next_prev_page, get_news_per_page, \
    get_news_for_last_day, structure_news_by_resource


@bp.route('/', methods=['GET'])
@cache.cached(timeout=120)
def index():
    news = get_news_for_last_day()
    structured_news = structure_news_by_resource(news)
    return render_template("table.html", title="My", all_news=structured_news)


@bp.route('/afisha', methods=['GET'])
@cache.cached(timeout=120, query_string=True)
def afisha():
    resource_id = current_app.config['RESOURCE_ID'][request.path[1:]]
    news_per_page = get_news_per_page(resource_id)
    next_url, prev_url = create_next_prev_page("afisha", news_per_page)
    return render_template("news.html", news=news_per_page.items, title="Afisha",
                           next_url=next_url, prev_url=prev_url)


@bp.route('/village', methods=['GET'])
@cache.cached(timeout=120, query_string=True)
def village():
    resource_id = current_app.config['RESOURCE_ID'][request.path[1:]]
    news_per_page = get_news_per_page(resource_id)
    next_url, prev_url = create_next_prev_page("village", news_per_page)
    return render_template("news.html", news=news_per_page.items, title="The-Village",
                           next_url=next_url, prev_url=prev_url)


@bp.route('/vc', methods=['GET'])
@cache.cached(timeout=120, query_string=True)
def vc():
    resource_id = current_app.config['RESOURCE_ID'][request.path[1:]]
    news_per_page = get_news_per_page(resource_id)
    next_url, prev_url = create_next_prev_page("vc", news_per_page)
    return render_template("news.html", news=news_per_page.items, title="VC",
                           next_url=next_url, prev_url=prev_url)
