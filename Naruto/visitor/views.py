from . import visitor
from flask import request, render_template
from ..models import Post

@visitor.route('/')
def index():
	print(request.headers)
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.publish_time.desc()).paginate(page=page, per_page=10, error_out=False)
	posts = pagination.items
	return render_template('visitor/index.html',
						   page=page,
						   pagination=pagination,
						   posts=posts)

@visitor.route('/post/<int:post_id>')
def show_post(post_id):
	post = Post.query.filter_by(id=post_id).first()
	return render_template('visitor/show_post.html',
						   post=post)
