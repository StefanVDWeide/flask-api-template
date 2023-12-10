import os
from dotenv import load_dotenv

# Set base directory of the app
basedir = os.path.abspath(os.path.dirname(__file__))

# Load the .env and .flaskenv variables
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    """
    Set the config variables for the Flask app

    """

    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # psotgresql crednetials. If you want to use postgres db, uncomment the following lines and comment out  above  SQLALCHEMY_DATABASE_URI corresponding to sqlite
    #hostname = os.getenv("DB_HOSTNAME")
    #user = os.getenv("USERNAME_DB")
    #database = os.getenv("DATABASE")
    #password = os.getenv("PASSWORD")
    #port = os.getenv("PORT")
    #  SQLALCHEMY_DATABASE_URI = f"postgresql://{user}:{password}@{hostname}:{port}/{database}"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    REDIS_URL = os.environ.get("REDIS_URL") or "redis://"
