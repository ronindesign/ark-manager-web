# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from flask import Flask, send_from_directory, session, redirect, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from celery import Celery, Task
from apps.config import Config
from flask_babel import Babel

db = SQLAlchemy()
login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('authentication', 'home', 'tables', 'charts', 'tasks', 'file_manager', ):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


def create_app(config):

    # Read debug flag
    DEBUG = (os.getenv('DEBUG', 'False') == 'True')

    # Contextual
    static_prefix = '/static'
    templates_dir = os.path.dirname(Config.basedir)

    TEMPLATES_FOLDER = os.path.join(templates_dir,'templates')
    STATIC_FOLDER = os.path.join(templates_dir,'static')

    def get_locale():
        return session.get('locale', 'en')
    
    app = Flask(__name__, static_url_path=static_prefix, template_folder=TEMPLATES_FOLDER, static_folder=STATIC_FOLDER)

    @app.route('/media/<path:filename>')
    def media_files(filename):
        return send_from_directory(Config.MEDIA_FOLDER, filename)
    
    @app.route('/set_locale/<locale>')
    def set_locale(locale):
        session['locale'] = locale
        return redirect(request.referrer)

    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost",
            result_backend="redis://localhost",
            task_ignore_result=True,
        ),
    )
    # app.config.from_prefixed_env()
    celery_init_app(app)

    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)

    babel = Babel(app)
    babel.init_app(app=app, locale_selector=get_locale)

    return app
