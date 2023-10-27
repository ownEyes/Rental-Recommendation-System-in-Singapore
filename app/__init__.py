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
from app.extension import db
from app.services.DataManger import DataManager
from app.services.MapDrawer import MapDrawer
from app.services.Recommender import Recommender

# bootstrap = Bootstrap5()
login_manager = LoginManager()
csrf = CSRFProtect()
bcrypt = Bcrypt()
# db = SQLAlchemy()
# logger = logging.getLogger("my_logger")

# def register_logger(logger):
    
#     logger.setLevel(logging.DEBUG)
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.DEBUG)
#     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     console_handler.setFormatter(formatter)
#     logger.addHandler(console_handler)
#     return logger

def register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    bcrypt.init_app(app)
    

    # bootstrap.init_app(app)
    
    #login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication','util', 'home'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):
    with app.app_context():
        try:
            # 尝试创建所有表
            db.create_all()
        except Exception as e:
            print('> Error: DBMS Exception: ' + str(e))

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'database.db')

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove() 

def register_services(app):
    app.data_manager = DataManager(app)
    poi_cols=app.config['POI_COLUMNS']
    poi_df= app.data_manager.get_pois_df(poi_cols+["name","formatted_address",'lat', 'lng'])
    
    mapcenter=app.config['MAP_CENTER']
    geojson_file_path=app.config['GEOJSON_FILE_PATH']
    semantic_groups=app.config['SEMANTIC_GROUPS']
    colors=app.config['COLORS']
    app.map_drawer = MapDrawer(poi_df,mapcenter,geojson_file_path,semantic_groups,colors)

    modelpath=app.config['MF_MODEL_PATH']
    topn=app.config['RECOMMEND_DEFAULT_TOPN']
    alpha=app.config['ALPHA']
    app.recommender = Recommender(modelpath,topn,alpha)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    with app.app_context():
        register_services(app)
    # app.logger=register_logger(logger)
    return app