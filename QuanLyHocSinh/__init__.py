from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager

app = Flask(__name__,template_folder='template')
app.secret_key="qdwqdwdqwd^$$^%#%#%$#%#%#$%#%"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/quanlyhocsinh?charset=utf8mb4' % quote('quan123456')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
login = LoginManager(app = app)