from . import visitor
from flask import request, render_template
from ..models import Post, Comment
from .forms import CommentForm

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

@visitor.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
	form = CommentForm()
	if form.validate_on_submit():
		visitor = Visitor(name=form.name.data, email=form.email.data, url=form.url.data)
		comment = Comment(body=form.body.data)
		db.session.add_all([visitor, comment])
		db.session.commit()
		return 'success'
	post = Post.query.filter_by(id=post_id).first()
	comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.timestamp.asc()).all()
	return render_template('visitor/show_post.html',
						   form=form,
						   post=post,
						   comments=comments)
