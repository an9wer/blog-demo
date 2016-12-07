from . import db
from datetime import datetime

class Category(db.Model):
	__tablename__ = 'category'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	posts = db.relationship('Post', backref='category')

	'''generate fake data'''
	@staticmethod
	def generate_fake(count=10):
		from faker import Factory
		fake = Factory.create()
		for i in range(count):
			c = Category(name = fake.word())
			db.session.add(c)
			db.session.commit()

class Post(db.Model):
	__tablename__ = 'post'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), unique=True)
	body = db.Column(db.Text)
	publish_time = db.Column(db.DateTime, default=datetime.utcnow)
	view_number = db.Column(db.Integer, default=0)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	comments = db.relationship('Comment', backref='post')

	'''generate fake data'''
	@staticmethod
	def generate_fake(count=100):
		from faker import Factory
		from random import randint
		fake = Factory.create()
		for i in range(count):
			c = Category.query.offset(randint(0, Category.query.count()-1)).first()
			p = Post(title = fake.sentence(),
					 body = fake.text(randint(2000, 3000)),
					 publish_time = fake.iso8601(),
					 view_number = randint(1000, 2000),
					 category = c)
			db.session.add(p)
			db.session.commit()

class Comment(db.Model):
	__tablename__ = 'comment'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
	visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))

	'''generate fake data'''
	@staticmethod
	def generate_fake(count=600):
		from faker import Factory
		from random import randint
		fake = Factory.create()
		for i in range(count):
			v = Visitor.query.offset(randint(0, Visitor.query.count()-1)).first()
			p = Post.query.offset(randint(0, Post.query.count()-1)).first()
			c = Comment(body = fake.text(randint(50, 300)),
						timestamp = fake.iso8601(),
						post = p,
						visitor = v)
			db.session.add(c)
			db.session.commit()

class Visitor(db.Model):
	__tablename__ = 'visitor'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True)
	email = db.Column(db.String(120))
	url = db.Column(db.String(120))
	comments = db.relationship('Comment', backref='visitor')

	'''generate fake data'''
	@staticmethod
	def generate_fake(count=30):
		from faker import Factory
		fake = Factory.create()
		for i in range(count):
			v = Visitor(name = fake.name(),
						email = fake.email(),
						url = fake.url())
			db.session.add(v)
			db.session.commit()

