from flask import Flask, render_template, request, redirect, url_for

from app.authentication import blueprint


@blueprint.route('/login')
def login():
    # 这里返回 nav.html 的内容
    return render_template('login.html')
@blueprint.route('/signup')
def signup():
    # 这里返回 nav.html 的内容
    return render_template('sign-up.html')