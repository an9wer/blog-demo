from . import db
from datetime import datetime

class Category(db.Model):
	__tablename__ = 'category'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60))
	posts = db.relationship('Post', backref='category')

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
	title = db.Column(db.String(120))
	body = db.Column(db.Text)
	publish_time = db.Column(db.DateTime, default=datetime.utcnow)
	view_number = db.Column(db.Integer, default=0)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

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
		


