from flask import current_app


def get_number_posts_per_page(request) -> (int, int):
    """Получить страницу и количество постов на ней"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', current_app.config['POSTS_PER_PAGE_API'], type=int), 100)
    return page, per_page
