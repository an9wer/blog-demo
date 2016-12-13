import mistune
from flask import render_template, session, redirect, request
from sqlalchemy import func
from . import admin
from .. import db
from ..models import Admin, Post, Comment, Visitor, Category
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

@admin.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
	categories = Category.query.all()
	if request.method == 'POST':
		title = request.form.get('title')
		category = request.form.get('category')
		new_category = request.form.get('new_category')
		abstract = request.form.get('abstract')
		body = request.form.get('body')
		body_html = mistune.markdown(body)
		if new_category:
			c = Category(name=new_category)
		else:
			c = Category.query.filter_by(name=category).first()
		post = Post(title=title, abstract=abstract, body=body, body_html=body_html, category=c)
		db.session.add(post)
		db.session.commit()
		return redirect('/')
	return render_template('edit.html',
						   categories=categories)

@admin.route('/posts')
@login_required
def posts():
	sort = request.args.get('sort', default='id', type=str)
	posts = Post.query.outerjoin(Comment)\
					  .add_column(func.count(Comment.post_id))\
					  .group_by(Post.id)\
					  .order_by(Post.id)\
					  .all()
	if sort == 'category':
		posts = Post.query.outerjoin(Comment)\
						  .add_column(func.count(Comment.post_id))\
						  .group_by(Post.id)\
						  .order_by(Post.category_id)\
						  .all()
	elif sort == 'publish time':
		posts = Post.query.outerjoin(Comment)\
						  .add_column(func.count(Comment.post_id))\
						  .group_by(Post.id)\
						  .order_by(Post.publish_time.desc())\
						  .all()
	elif sort == 'title':
		posts = Post.query.outerjoin(Comment)\
						  .add_column(func.count(Comment.post_id))\
						  .group_by(Post.id)\
						  .order_by(Post.title)\
						  .all()
	elif sort == 'views':
		posts = Post.query.outerjoin(Comment)\
						  .add_column(func.count(Comment.post_id))\
						  .group_by(Post.id)\
						  .order_by(Post.view_number.desc())\
						  .all()
	elif sort == 'comments':
		posts = Post.query.outerjoin(Comment)\
						  .add_column(func.count(Comment.post_id))\
						  .group_by(Post.id)\
						  .order_by(func.count(Comment.post_id).desc())\
						  .all()
	return render_template('posts.html',
						   posts=posts)

@admin.route('/comments')
@login_required
def comments():
	sort = request.args.get('sort', default='post id', type=str)
	comments = Comment.query.join(Post).join(Visitor)\
							.with_entities(Post.id, Visitor.name, Visitor.email, Visitor.url, Comment.timestamp, Comment.body)\
							.order_by(Post.id)\
							.all()
	if sort == 'visitor':
		comments = Comment.query.join(Post).join(Visitor)\
								.with_entities(Post.id, Visitor.name, Visitor.email, Visitor.url, Comment.timestamp, Comment.body)\
								.order_by(Visitor.name)\
								.all()
	elif sort == 'email':
		comments = Comment.query.join(Post).join(Visitor)\
								.with_entities(Post.id, Visitor.name, Visitor.email, Visitor.url, Comment.timestamp, Comment.body)\
								.order_by(Visitor.email)\
								.all()
	elif sort == 'url':
		comments = Comment.query.join(Post).join(Visitor)\
								.with_entities(Post.id, Visitor.name, Visitor.email, Visitor.url, Comment.timestamp, Comment.body)\
								.order_by(Visitor.url)\
								.all()
	elif sort == 'timestamp':
		comments = Comment.query.join(Post).join(Visitor)\
								.with_entities(Post.id, Visitor.name, Visitor.email, Visitor.url, Comment.timestamp, Comment.body)\
								.order_by(Comment.timestamp.desc())\
								.all()
	elif sort == 'comment body':
		comments = Comment.query.join(Post).join(Visitor)\
								.with_entities(Post.id, Visitor.name, Visitor.email, Visitor.url, Comment.timestamp, Comment.body)\
								.order_by(Comment.body)\
								.all()
	return render_template('comments.html',
						   comments=comments)
