from flask import render_template, url_for, request, current_app
from app.models import News
from app.main import bp
from datetime import datetime, timedelta


@bp.route('/', methods=['GET'])
def index():
    since = datetime.now() - timedelta(hours=24)
    news_afisha, news_village, news_vc = [], [], []
    news = News.query.filter(News.timestamp > since).order_by(News.timestamp.desc()).all()
    for new in news:
        if new.source.title == 'afisha':
            news_afisha.append(new)
        elif new.source.title == 'the-village':
            news_village.append(new)
        elif new.source.title == 'vc':
            news_vc.append(new)
    return render_template("table.html", title="Test", news_afisha=news_afisha, news_village=news_village,
                           news_vc=news_vc)

#TODO: Объединить все 3 view - видоизменение (Mixin)?
@bp.route('/afisha', methods=['GET'])
def afisha():
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(user_id=1).order_by(News.timestamp.desc())\
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.afisha', page=news.next_num) if news.has_next else None
    prev_url = url_for('main.afisha', page=news.prev_num) if news.has_prev else None
    return render_template("news.html", news=news.items, title="Afisha", next_url=next_url, prev_url=prev_url)


@bp.route('/village', methods=['GET'])
def village():
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(user_id=2).order_by(News.timestamp.desc())\
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.village', page=news.next_num) if news.has_next else None
    prev_url = url_for('main.village', page=news.prev_num) if news.has_prev else None
    return render_template("news.html", news=news.items, title="The-Village", next_url=next_url, prev_url=prev_url)


@bp.route('/vc', methods=['GET'])
def vc():
    page = request.args.get('page', 1, type=int)
    news = News.query.filter_by(user_id=3).order_by(News.timestamp.desc())\
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.vc', page=news.next_num) if news.has_next else None
    prev_url = url_for('main.vc', page=news.prev_num) if news.has_prev else None
    return render_template("news.html", news=news.items, title="The-Village", next_url=next_url, prev_url=prev_url)
