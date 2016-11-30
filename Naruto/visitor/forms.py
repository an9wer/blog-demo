from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, URL

class CommentForm(FlaskForm):
	name = StringField('your name:', validators=[DataRequired(message='please enter your name'), 
												 Length(min=1, max=60)])
	email = StringField('your email:', validators=[DataRequired(message='please enter your email'),
												   Email()])
	url = StringField('your website URL:', validators=[URL()])
	body = TextAreaField('your comment:', validators=[DataRequired(message='please enter your comment')])
	submit = SubmitField('commit')
