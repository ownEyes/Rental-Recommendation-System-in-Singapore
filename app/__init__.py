# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
# from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from importlib import import_module

from flask_wtf.csrf import CSRFProtect
import logging
from app.services.DataManger import DataManager
from app.services.MapDrawer import MapDrawer
from app.services.Recommender import Recommender

from app.extension import db
# bootstrap = Bootstrap5()
login_manager = LoginManager()
csrf = CSRFProtect()
bcrypt = Bcrypt()
logger = logging.getLogger("my_logger")

def register_logger(logger):
    
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

def register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    # app.data_manager = DataManager()
    # app.map_drawer = MapDrawer()
    # app.recommender = Recommender()
    

    # bootstrap.init_app(app)
    
    #login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication','util', 'home'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_file_path = os.path.join(basedir, 'database', 'database.db')
    if not os.path.exists(database_file_path):
        print("Error: Database file not found at", database_file_path)
        # 这里你可以选择创建数据库文件，或者退出程序
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_file_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # db.init_app(app)
    # @app.got_first_request
    # def initialize_database():
    #     try:
    #         db.create_all()
    #     except Exception as e:

    #         print('> Error: DBMS Exception: ' + str(e) )

    #         # fallback to SQLite
    #         basedir = os.path.abspath(os.path.dirname(__file__))
    #         app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '/app/database/dtatbase.db')

    #         print('> Fallback to SQLite ')
    #         db.create_all()
    # return

    # @app.teardown_request
    # def shutdown_session(exception=None):
    #     db.session.remove() 


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    app.logger=register_logger(logger)
    return app

    # @app.before_first_request
    # def initialize_data_manager():
        