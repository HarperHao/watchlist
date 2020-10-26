"""
Author   : HarperHao
TIME    ： 2020/10/26
FUNCTION:  错误处理函数
"""
from flask import render_template
from WatchList import app


# 404错误处理函数
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
