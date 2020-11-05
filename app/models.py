from app.app import db
from datetime import datetime
from flask import url_for


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
            }
        }
        return data


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    home_page = db.Column(db.String(120), index=True, unique=True)
    news = db.relationship('News', backref='source', lazy='dynamic')

    def __repr__(self):
        return f'<Resource {self.title}>'


class News(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(255), index=True, unique=True)
    body = db.Column(db.Text)
    link = db.Column(db.String(255), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('resource.id'))

    def __repr__(self):
        return f'<News {self.header}>'

    def to_dict(self):
        data = {
            'header': self.header,
            'body': self.body,
            'time': self.timestamp.isoformat() + 'Z',
            '_links': {
                'self': self.link,
                'resource': url_for('api.get_resource_news', id=self.user_id)
            }
        }
        return data
