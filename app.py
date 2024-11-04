from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import csv
from io import StringIO
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mo_atif_secret_key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_coins.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login page when unauthorized

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
