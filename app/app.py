from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.parseinfo.scheduler import add_news
    scheduler = BackgroundScheduler()
    scheduler.add_job(add_news, 'interval', args=[app, db], minutes=10)
    scheduler.start()

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
