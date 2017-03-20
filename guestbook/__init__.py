# coding: utf-8
import shelve
from datetime import datetime

from flask import Flask, request, render_template, redirect, escape, Markup

application = Flask(__name__)

DATA_FILE='guestbook.dat'

def save_data(name, comment, create_at):
	""" save data commited
	"""
	# open the database file with shelve
	database = shelve.open(DATA_FILE)
	# if greeting_list not exists, create a new list
	if 'greeting_list' not in database:
		greeting_list = []
	else:
		greeting_list = database['greeting_list']
	# append the data commited to the head of the list
	greeting_list.insert(0, {'name': name, 'comment': comment, 'create_at': create_at})
	# update the database
	database['greeting_list'] = greeting_list
	# close the database
	database.close()

def load_data():
	""" return the data commited
	"""
	# open database file with shelve
	database = shelve.open(DATA_FILE)
	# return greeting_list list, if no data in it ,return []
	greeting_list = database.get('greeting_list', [])
	# close database
	database.close()
	return greeting_list 

@application.route('/')
def index():
	""" show the page use templet
	"""
	greeting_list = load_data()
	return render_template('index.html', greeting_list = greeting_list)


@application.route('/post', methods=['POST'])
def post():
	"""URL to commit the comment
	"""
	# get the data commited
	name = request.form.get('name')
	comment = request.form.get('comment')
	create_at = datetime.now()
	# save data
	save_data(name, comment, create_at)
	# redirect to the home page	
	return redirect('/')

@application.template_filter('nl2br')
def nl2br_filter(s):
	# replace the '\n' to '<br>'
	return escape(s).replace('\n', Markup('<br>'))

@application.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
	return dt.strftime('%Y/%m/%d %H:%M:%S')


def main():
	application.run('127.0.0.1', 8000)

if __name__ == '__main__':
	# run the application in ip:127.0.0.1 at port 8000
	application.run('127.0.0.1', 8000, debug=True) 
