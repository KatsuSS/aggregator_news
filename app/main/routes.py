from flask import render_template, request, current_app
from app.models import News, Resource
from app.main import bp
from datetime import datetime, timedelta
from app.app import cache
from app.main.services import create_next_prev_page, get_news_per_page


@bp.route('/', methods=['GET'])
@cache.cached(timeout=120)
def index():
    since = datetime.now() - timedelta(hours=24)
    all_news = {
        'afisha': {"news": [],
                   "link": ""},
        'village': {"news": [],
                    "link": ""},
        'vc': {"news": [],
               "link": ""}
    }
    news = News.query.filter(News.timestamp > since).order_by(News.timestamp.desc()).all()
    resources = Resource.query.all()
    for new in news:
        if new.source.title == 'afisha':
            all_news['afisha']["news"].append(new)
        elif new.source.title == 'the-village':
            all_news['village']["news"].append(new)
        elif new.source.title == 'vc':
            all_news['vc']["news"].append(new)
    all_news['afisha']["link"] = resources[0].home_page
    all_news['village']["link"] = resources[1].home_page
    all_news['vc']["link"] = resources[2].home_page
    return render_template("table.html", title="My", all_news=all_news)


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
