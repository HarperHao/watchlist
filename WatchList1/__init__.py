"""
Author   : HarperHao
TIME    ： 2020/10/26
FUNCTION:  包构造文件，创建程序实例
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pymysql

app = Flask(__name__)

app.secret_key = 'HarperHao'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/watchlist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
pymysql.install_as_MySQLdb()

db = SQLAlchemy(app)
login_manager = LoginManager(app)


# 用户回调函数
@login_manager.user_loader
def load_user(user_id):
    from WatchList1.models import User
    # 用user_id作为主键去查询对应的用户
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login'


# 模版上下文处理函数
@app.context_processor
def inject_user():
    from WatchList1.models import User
    user = User.query.first()
    # 返回{'user':'user'}
    return dict(user=user)

from WatchList1 import commands,views,errors
