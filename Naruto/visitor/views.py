from flask import request, render_template, jsonify, redirect, url_for
from . import visitor
from .forms import CommentForm
from .. import db
from ..models import Post, Comment, Visitor

@visitor.route('/')
def index():
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.publish_time.desc()).paginate(page=page, per_page=10, error_out=False)
	posts = pagination.items
	return render_template('index.html',
						   page=page,
						   pagination=pagination,
						   posts=posts) 

@visitor.route('/post/<int:post_id>', methods=['GET'])
def post(post_id):
	form = CommentForm()
	post = Post.query.filter_by(id=post_id).first()
	comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.timestamp.asc()).all()
	return render_template('post.html',
						   form=form,
						   post=post,
						   comments=comments)

@visitor.route('/_validate_input_ajax', methods=['POST'])
def validate_input_ajax():
	form = CommentForm()
	form.validate_on_submit()
	name_errors = form.name.errors
	email_errors = form.email.errors
	url_errors = form.url.errors
	body_errors= form.body.errors
	return jsonify(name_errors=name_errors,
				   email_errors=email_errors,
				   url_errors=url_errors,
				   body_errors=body_errors)

@visitor.route('/_submit_comment_ajax', methods=['POST'])
def comment_submit_ajax():
	form = CommentForm()
	'''ensure the input of url is correct or none'''
	if form.url.data == '' or form.url.validate(form):
		if form.name.validate(form) and form.email.validate(form) and form.body.validate(form):
			name = form.name.data
			email = form.email.data
			url = form.url.data
			body = form.body.data
			post_id = request.form.get('post_id', type=int)
			'''ensure the name is unique'''
			v = Visitor.query.filter_by(name=name).first()
			if v:
				'''If the visitor name is existed'''
				if Visitor.query.filter_by(email=email).first():
					'''If both of the visitor name and email are existed, it prove that the visitor has been existed.
					   We only need to add the comment to database.
					'''
					comment = Comment(body=body, post_id=post_id, visitor=v)
					db.session.add(comment)
					db.session.commit()
					print(comment.timestamp)
					return jsonify(id=comment.id,
								   name=name,
								   timestamp=comment.timestamp,
								   body=body)
				else:
					'''If the visitor name is existed but the email is not existed, It means that the visitor's name has been registered.
					   It is not allowed.
					'''
					return jsonify(error='your name has already been registered')
			else:
				'''If the visitor name is not existed.'''
				if Visitor.query.filter_by(email=email).first():
					'''If the visitor name is not existed but the email has been existed, It means the visitor email has been registered.
					   It is not allowed.
					'''
					return jsonify(error='your email has already been registered')
				else:
					'''If none of the visitor name and email are existed, We need to  add both of the visitor and comment to database.'''
					visitor = Visitor(name=name, email=email, url=url)
					comment = Comment(body=body, post_id=post_id, visitor=visitor)
					db.session.add_all([visitor, comment])
					db.session.commit()
					return jsonify(id=comment.id,
								   name=name,
								   timestamp=comment.timestamp,
								   body=body)
	return jsonify(error='Please validate your information')
