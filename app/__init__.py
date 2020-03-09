from flask import Flask
# This allows us to keep our configs in a separate folder
from config import Config
# SQLAlchemy to aid in high-level database
from flask_sqlalchemy import SQLAlchemy
# Initializing the Migrate extension for databases
from flask_migrate import Migrate
# Initializing the flask-login extension
from flask_login import LoginManager
# Setting up portions of the email settings to send logs to the administrator
import logging
# For logging purposes and to email logs to the admin
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
# Setting up the email
from flask_mail import Mail
# Flask installed bootstrap!
from flask_bootstrap import Bootstrap
# For timezone issues, we will use flask-moment
from flask_moment import Moment
# Flask-Babel will help with translations, however, we will be skipping this section for now
# from flask_babel import Babel
# elasticsearch will allow us to search the entire website
from elasticsearch import Elasticsearch


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# This is the url_for() call to get the url for the login
# We are using this to restrict certain pages for members who are logged in
login.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
# babel = Babel(app)
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    if app.config['ELASTICSEARCH_URL'] else None

from app import routes, models, errors

# If an error occurs, the log will be sent to the administrator email
# when the debugger is turned off
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    # logging the errors to a file
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    # This line tells us when the server was started/restarted
    app.logger.info('Microblog startup')
