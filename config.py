import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ENV = "development"
    SECRET_KEY = os.environ.get('SECRET_KEY') or "CHANGE-THIS-SECRET-KEY"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "bti4@!rtx1cZRC8EX#1kRhO57degNv*c7#&B"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
