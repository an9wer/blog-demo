from flask import request, render_template, jsonify, redirect, url_for
from . import visitor
from .. import db
from ..models import Post, Comment, Visitor, Category

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
	post = Post.query.filter_by(id=post_id).first()
	comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.timestamp.asc()).all()
	'''the number of view should plus one'''
	post.view_number += 1
	db.session.add(post)
	db.session.commit()
	return render_template('post.html',
						   post=post,
						   comments=comments)

@visitor.route('/archive')
def archive():
	posts = Post.query.order_by(Post.publish_time.desc()).all()
	categories = Category.query.all()
	return render_template('archive.html',
						   posts=posts,
						   categories=categories)

@visitor.route('/_submit_comment_ajax', methods=['POST'])
def comment_submit_ajax():
	name = request.form.get('name', type=str)
	email = request.form.get('email', type=str)
	url = request.form.get('url', type=str)
	body = request.form.get('body', type=str)
	post_id = request.form.get('post_id', type=int)

	if name and email and body :
		v = Visitor.query.filter_by(name=name).first()
		'''The visitor name must be unique, but one email may refer to multiple visitor names.'''
		if v:
			'''If both of the visitor name and email are existed, it prove that the visitor has been existed.
			   We only need to add the comment to database.
			'''
			if v.email == email:
				c = Comment(body=body, post_id=post_id, visitor=v)
				db.session.add(c)
				db.session.commit()
				return jsonify(id=c.id,
							   name=name,
							   timestamp=c.timestamp,
							   body=body)
			else:
				'''If the visitor name is existed but the email is not existed, It means that the visitor's name has been registered.
				   It is not allowed.
				'''
				return jsonify(error='your name has already been registered')
		else:
			'''One email may refer to multiple visitor names.
			   If the visitor name is not existed, We need to  add both of the visitor and comment to database.
			''' 
			v = Visitor(name=name, email=email, url=url)
			c = Comment(body=body, post_id=post_id, visitor=v)
			db.session.add_all([v, c])
			db.session.commit()
			return jsonify(id=c.id,
						   name=name,
						   timestamp=c.timestamp,
						   body=body)
	return jsonify(error='Please validate your information')

