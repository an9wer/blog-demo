import datetime
from flask import render_template, session, redirect, request
from . import admin
from ..models import Admin
from Naruto.api.decorators import login_required

@admin.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		a = Admin.query.first()
		name = request.form.get('name')
		password = request.form.get('password')
		if a.name == name and a.verify_password(password):
			session['logged_in'] = 'ok'
			return redirect('/admin/')
	return render_template('login.html')

@admin.route('/')
@login_required
def index():
	return  render_template('dashboard.html')

@admin.route('/posts')
@login_required
def posts():
	return render_template('posts.html')
