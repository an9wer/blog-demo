import datetime
from flask import render_template, session, redirect, request
from . import admin
from ..models import Admin, Post, Comment
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

@admin.route('/edit')
@login_required
def edit():
	return render_template('edit.html')

@admin.route('/posts')
@login_required
def posts():
	sort = request.args.get('sort', default='id', type=str)
	if sort == 'category':
		posts = Post.query.order_by(Post.category).all()
	elif sort == 'publish_time':
		posts = Post.query.order_by(Post.publish_time).all()
	elif sort == 'title':
		posts = Post.query.order_by(Post.title).all()
	elif sort == 'views':
		posts = Post.query.order_by(post.view_number).all()
	'''
	elif sorts == 'comments':
	'''	
	posts = Post.query.all()
	return render_template('posts.html',
						   posts=posts)

@admin.route('/comments')
@login_required
def comments():
	comments = Comment.query.all()
	return render_template('comments.html',
						   comments=comments)
