from flask import render_template, url_for, request, current_app
from app.models import News, Resource
from app.main import bp
from datetime import datetime, timedelta
from app.app import cache


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
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(user_id=1).order_by(News.timestamp.desc())\
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.afisha', page=news.next_num) if news.has_next else None
    prev_url = url_for('main.afisha', page=news.prev_num) if news.has_prev else None
    return render_template("news.html", news=news.items, title="Afisha", next_url=next_url, prev_url=prev_url)


@bp.route('/village', methods=['GET'])
@cache.cached(timeout=120, query_string=True)
def village():
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(user_id=2).order_by(News.timestamp.desc())\
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.village', page=news.next_num) if news.has_next else None
    prev_url = url_for('main.village', page=news.prev_num) if news.has_prev else None
    return render_template("news.html", news=news.items, title="The-Village", next_url=next_url, prev_url=prev_url)


@bp.route('/vc', methods=['GET'])
@cache.cached(timeout=120, query_string=True)
def vc():
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(user_id=3).order_by(News.timestamp.desc())\
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.vc', page=news.next_num) if news.has_next else None
    prev_url = url_for('main.vc', page=news.prev_num) if news.has_prev else None
    return render_template("news.html", news=news.items, title="VC", next_url=next_url, prev_url=prev_url)
