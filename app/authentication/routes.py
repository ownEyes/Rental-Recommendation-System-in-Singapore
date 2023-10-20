from flask import Flask, render_template, request, redirect, url_for,flash
from flask_login import current_user

from app import bcrypt,db
from app.authentication import blueprint
from app.authentication.form import LoginForm,SignupForm
from app.authentication.models import User

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    # 这里返回 nav.html 的内容
    if form.validate_on_submit():  
        
        return redirect(url_for('home_blueprint.userin')) 

    return render_template('login.html',form=form)
@blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form=SignupForm()
    # if form.validate_on_submit():
    
    #     return redirect(url_for('authentication_blueprint.login')) 
    # return render_template('sign-up.html',form=form)

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    title = 'User sign up'
    # form = SignupForm()

    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data

        password = bcrypt.generate_password_hash(form.password.data)

        user = User(name=name, username=username, password=password)

        db.session.add(user)

        db.session.commit()

        flash('Successfully registered!', category='success')
        return redirect(url_for('home'))
    return render_template('sign-up.html', form=form, title=title, signup=True)