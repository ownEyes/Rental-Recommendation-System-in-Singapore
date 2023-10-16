from app.util import blueprint
from flask import render_template, request

@blueprint.route('/nav')
def nav():
    # 这里返回 nav.html 的内容
    return render_template('nav.html')