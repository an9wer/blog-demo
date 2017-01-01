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
    return  render_template('edit.html')

@admin.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    categories = Category.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        abstract = request.form.get('abstract')
        body = request.form.get('body')
        body_html = mistune.markdown(body)
        print(body_html)
        '''If the category is not existed, we need to add it to the database.'''
        c = Category.query.filter_by(name=category).first()
        if not c:
            c = Category(name=category)
        post = Post(title=title, abstract=abstract, body=body, body_html=body_html, category=c)
        '''We don't need to db.sessoin.add(c), because the save-update cascade is on by default.'''
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    return render_template('edit.html',
                           categories=categories)

@admin.route('/modify', methods=['GET', 'POST'])
@login_required
def modify():
    id = session.get('id')
    title = session.get('title')
    category = session.get('category')
    abstract = session.get('abstract')
    body = session.get('body')
    if request.method == 'POST':
        post = Post.query.filter_by(id=id).first()
        post.title = request.form.get('title')
        post.abstract = request.form.get('abstract')
        post.body = request.form.get('body')
        post.body_html = mistune.markdown(request.form.get('body'))
        print(post.body_html)
        '''If the category is not existed, we need to add it to the database.'''
        c = Category.query.filter_by(name=request.form.get('category')).first()
        if not c:
            c = Category(name=post.category)
            ad.session.add(c)
        '''Here we can't use "post.category = c" '''
        post.category_id = c.id
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    categories = Category.query.all()
    return render_template('modify.html',
                           categories=categories,
                           title=title,
                           category=category,
                           abstract=abstract,
                           body=body)
    
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

@admin.route('/posts/modify', methods=['POST'])
@login_required
def posts_modify():
    post_id = request.form.get('post_id')
    post = Post.query.filter_by(id=post_id).first()
    session['id'] = post.id
    session['title'] = post.title
    session['category'] = post.category.name
    session['abstract'] = post.abstract
    session['body'] = post.body
    return redirect('/admin/modify')

@admin.route('/posts/delete', methods=['POST'])
@login_required
def posts_delete():
    post_id = request.form.get('post_id')
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect('/admin/posts')

@admin.route('/comments')
@login_required
def comments():
    sort = request.args.get('sort', default='comment id', type=str)
    comments = Comment.query.join(Post).join(Visitor)\
                            .with_entities(Comment.id, Post.id, Visitor.name, Visitor.email,
                                           Visitor.url, Comment.timestamp, Comment.body)\
                            .order_by(Comment.id)\
                            .all()
    if sort == 'post id':
        comments = Comment.query.join(Post).join(Visitor)\
                                .with_entities(Comment.id, Post.id, Visitor.name, Visitor.email,
                                               Visitor.url, Comment.timestamp, Comment.body)\
                                .order_by(Post.id)\
                                .all()
    if sort == 'visitor':
        comments = Comment.query.join(Post).join(Visitor)\
                                .with_entities(Comment.id, Post.id, Visitor.name, Visitor.email,
                                               Visitor.url, Comment.timestamp, Comment.body)\
                                .order_by(Visitor.name)\
                                .all()
    elif sort == 'email':
        comments = Comment.query.join(Post).join(Visitor)\
                                .with_entities(Comment.id, Post.id, Visitor.name, Visitor.email,
                                               Visitor.url, Comment.timestamp, Comment.body)\
                                .order_by(Visitor.email)\
                                .all()
    elif sort == 'url':
        comments = Comment.query.join(Post).join(Visitor)\
                                .with_entities(Comment.id, Post.id, Visitor.name, Visitor.email,
                                               Visitor.url, Comment.timestamp, Comment.body)\
                                .order_by(Visitor.url)\
                                .all()
    elif sort == 'timestamp':
        comments = Comment.query.join(Post).join(Visitor)\
                                .with_entities(Comment.id, Post.id, Visitor.name, Visitor.email,
                                               Visitor.url, Comment.timestamp, Comment.body)\
                                .order_by(Comment.timestamp.desc())\
                                .all()
    elif sort == 'comment body':
        comments = Comment.query.join(Post).join(Visitor)\
                                .with_entities(Comment.id, Post.id, Visitor.name, Visitor.email,
                                               Visitor.url, Comment.timestamp, Comment.body)\
                                .order_by(Comment.body)\
                                .all()
    return render_template('comments.html',
                           comments=comments)

@admin.route('/comments/delete', methods=['POST'])
@login_required
def comments_delete():
    comment_id = request.form.get('comment_id')
    comment = Comment.query.filter_by(id=comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect('/admin/comments')
