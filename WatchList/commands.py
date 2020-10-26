"""
Author   : HarperHao
TIME    ： 2020/10/26
FUNCTION:  命令函数
"""

import click

from WatchList import app, db
from WatchList.models import User, Movie


@app.cli.command()
@click.option('--drop', is_flag=True, help="Create after drop")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化成功')


@app.cli.command()
def forge():
    """生成数据"""
    # db.create_all()到底有什么用，为什么每个函数都在用它
    db.create_all()
    name = 'HarperHao'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    # 创建user数据
    user = User(name=name)
    db.session.add(user)
    # 创建books数据
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('创建数据成功')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login')
def admin(username, password):
    """创建管理员用户"""
    db.create_all()

    user = User.query.first()
    print(user.username)
    print(user)
    flag = True
    if user is not None:
        user.username = username
        user.set_password(password)
        flag = False
    # 如果管理员还没有被创建，则创建一个管理员
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)
    # 提交会话
    db.session.commit()
    click.echo('创建管理员成功')
    print(flag)
