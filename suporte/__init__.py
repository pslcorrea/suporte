from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
session = Session


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///suporte.db'
app.config['SECRET_KEY'] = '4427d82b06044b0f73f015ba822d74a9'
database = SQLAlchemy(app)

from suporte import routes
