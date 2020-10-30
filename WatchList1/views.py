"""
Author   : HarperHao
TIME    ： 2020/10/26
FUNCTION:  视图函数
"""

from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, current_user, logout_user
# 引入app对象和数据库对象db
from WatchList1 import app, db
from WatchList1.models import User, Movie


# 主视图
@app.route('/', methods=['GET', 'POST'])
def index():
    print('test')

    if request.method == 'POST':
        # 获取表单数据
        # 传入表单对应输入字段的name值
        # request.form是一个特殊的字典

        # 如果当前用户没有认证
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        title = request.form.get('title')
        year = request.form.get('year')
        print(title)
        print(year)
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            # 显示错误信息
            flash('Invalid input.')
            # 无效输入的话重定向到主页
            return redirect(url_for('index'))
        # 如果数据无误的话，将表单信息添加到数据库中
        else:
            movie_item = Movie(title=title, year=year)
            db.session.add(movie_item)
            db.session.commit()
            flash('成功添加')
            # 重定向回主界面
            return redirect(url_for('index'))
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index3.html', user=user, movies=movies)


# 编辑视图
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required  # 登录保护
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        # 如果数据错误
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('无效输入!')
            return redirect(url_for('edit', movie_id=movie_id))
        # 如果输入没有问题，则更改数据库中的内容
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('数据更新成功')
        # 数据更新成功，返回主界面
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


# 删除视图
@app.route('/movie/delete/<int:movie_id>', methods=["POST"])
@login_required  # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('此电影被删除')
    return redirect(url_for('index'))


# 设置视图
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """支持登录用户name的修改"""
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash("无效的输入")
            return redirect(url_for('settings'))

        current_user.name = name
        db.session.commit()
        flash('用户名已修改')
        return redirect(url_for('index'))

    return render_template('settings.html')


# 用户认证函数(登录函数)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 判断是否为空输入
        if not username or not password:
            flash('无效的输入')
            return redirect(url_for('login'))
        # 输入格式正确
        else:
            user = User.query.first()
            # 验证用户名和密码是否一致
            if username == user.username and user.validate_password(password):
                login_user(user)
                flash('登录成功！')
                return redirect(url_for('index'))
            # 如果用户名和密码不一致
            else:
                flash('用户名或密码错误！')
                return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))
