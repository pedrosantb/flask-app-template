from flask import render_template, flash, redirect, request, url_for, jsonify, session
from app import app, db
from app.forms import LoginForm, RegistrationForm
from sqlalchemy import update, create_engine
import os
import json
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Users

from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

@app.route('/')
@app.route('/index/')
def index():
    title = "Index page"
    return render_template('index.html', title=title)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid user or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup/', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit:
        user = Users(email=form.email.data, status=0)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User registrated sucessfully')
        return redirect(url_for('login'))
    
    return render_template('registration.html', form=form)


# Usefull tag:
# @login_required
