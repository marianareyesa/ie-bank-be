from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
# from applicationinsights.flask.ext import AppInsights

app = Flask(__name__)

load_dotenv()

# Select environment based on the ENV environment variable
#Loading some configuration
if os.getenv('ENV') == 'local':
    print("Running in local mode")
    app.config.from_object('config.LocalConfig')
elif os.getenv('ENV') == 'dev':
    print("Running in development mode")
    app.config.from_object('config.DevelopmentConfig')
elif os.getenv('ENV') == 'ghci':
    print("Running in github mode")
    app.config.from_object('config.GithubCIConfig')
else:
    print("Running in production mode")
    app.config.from_object('config.ProductionConfig')


db = SQLAlchemy(app)

from iebank_api.models import Account

with app.app_context():
    db.create_all() #This line creates a database
CORS(app)

from iebank_api import routes

#Initialize application insights and force fllushing application insights
#if(os.getenv('ENV') == 'dev'):
 #   appinsights = AppInsights(app)
  #  @app.after_request
   # def after_request(response):
    #    appinsights.flush()
     #   return response