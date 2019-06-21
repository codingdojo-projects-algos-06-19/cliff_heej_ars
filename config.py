from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import re

app = Flask(__name__)
#config to tell our app witch database we should connecting to 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzatime.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
#code that allow create migrate and table and bcrypt
migrate = Migrate(app, db)
app.secret_key='group_project_arshiya_heejin_cliff'
bcrypt = Bcrypt(app)