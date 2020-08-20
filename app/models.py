from app.app import db
from datetime import datetime


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    home_page = db.Column(db.String(120), index=True, unique=True)
    news = db.relationship('News', backref='source', lazy='dynamic')

    def __repr__(self):
        return f'<Resource {self.title}>'


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(120), index=True, unique=True)
    link = db.Column(db.String(120), index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('resource.id'))

    def __repr__(self):
        return f'<News {self.header}>'

