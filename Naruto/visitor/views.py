from . import visitor
from flask import render_template

@visitor.route('/index')
def index():
	return render_template('base.html')
