"""
Author   : HarperHao
TIME    ： 2020/10/
FUNCTION:  模型类
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from WatchList import db


# 构造数据库模型
class User(db.Model, UserMixin):
    # 表名
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    # 用来设置密码的方法
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 用来验证密码的方法
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    # 电影的年份
    year = db.Column(db.String(4))
