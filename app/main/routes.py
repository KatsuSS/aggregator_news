from flask import render_template
from app.main import bp
from app.app import cache
from app.main.services import get_news_for_last_day, structure_news_by_resource, get_resource_news_on_the_page
from app.models import News


@bp.route('/', methods=['GET'])
@cache.cached(timeout=120)
def index():
    news = get_news_for_last_day()
    structured_news = structure_news_by_resource(news)
    return render_template("table.html", title="My", all_news=structured_news)


@bp.route('/afisha', methods=['GET'])
@cache.cached(timeout=120, query_string=True)
def afisha():
    news_per_page, next_url, prev_url = get_resource_news_on_the_page("afisha")
    return render_template("news.html", news=news_per_page.items, title="Afisha",
                           next_url=next_url, prev_url=prev_url)


@bp.route('/post/<int:id>', methods=['GET'])
@cache.cached(timeout=120, query_string=True)
def one_post(id: int):
    post = News.query.get_or_404(id)
    return render_template("post.html", post=post)


@bp.route('/village', methods=['GET'])
@cache.cached(timeout=120, query_string=True)
def village():
    news_per_page, next_url, prev_url = get_resource_news_on_the_page("village")
    return render_template("news.html", news=news_per_page.items, title="The-Village",
                           next_url=next_url, prev_url=prev_url)


@bp.route('/vc', methods=['GET'])
@cache.cached(timeout=120, query_string=True)
def vc():
    news_per_page, next_url, prev_url = get_resource_news_on_the_page("vc")
    return render_template("news.html", news=news_per_page.items, title="VC",
                           next_url=next_url, prev_url=prev_url)
