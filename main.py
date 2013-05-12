import template
import json
import time
from markdown import markdown
from bottle import route, run, static_file, error, abort, redirect

import os

POSTS_DIR = './posts'

class Page(object):
	def __init__(self, url, title):
		self.url = url
		self.title = title
pages = [
	Page('/', 'Home'),
	Page('/blog', 'Blog')
	]

@route('/css/<filename:re:.*\\.css>')
def serve_css(filename):
	return static_file(filename, root='./css', mimetype='text/css')

@route('/css/<filename:re:.*\\.js>')
def serve_js(filename):
	return static_file(filename, root='./js', mimetype='application/javascript')

@route('/favicon.ico')
def favicon():
	return static_file('favicon.ico', root='./', mimetype='image/x-icon')

@route('/')
def index():
	return template.render("index.html", {'pages': pages, 'page': pages[0]})

@route('/blog/posts/<post_name>')
def blog_post(post_name):
	try:
		post = json.load(open(POSTS_DIR + '/' + post_name + '.json'))
		post['date'] = format_date(post['timestamp'])
		post['title'] = post_name
		post['body'] = markdown(open(POSTS_DIR + '/' + post_name + '.md').read())
		return template.render("blog.html", {'posts': [post],
											 'pages': pages,
											 'page': pages[1]})
	except IOError:
		abort(404)

@route('/blog/<page_num:int>')
def blog_page(page_num):
	if page == "":
		redirect("/blog")
	posts_folder = filter(lambda x: x[-5:] == '.json', os.listdir(POSTS_DIR))
	posts = []
	for filename in posts_folder:
		post = json.load(open(POSTS_DIR + '/' + filename))
		post['date'] = format_date(post['timestamp'])
		post['title'] = filename[:-5]
		post['text_location'] = POSTS_DIR + '/' + filename[:-5] + '.md'
		posts.append(post)
	# equality is unlikely
	posts.sort(cmp=lambda a,b: -1 if a['timestamp'] > b['timestamp'] else 1)
	posts = posts[page_num*10:(page_num+1)*10]
	for i in xrange(len(posts)):
		posts[i]['body'] = markdown(open(posts[i]['text_location']).read())
	return template.render("blog.html", {'posts': posts,
										 'pages': pages,
										 'page': pages[1]})

@route('/<something:path>/')
def slash_redir(something):
	redirect("/" + something)
	
@route('/blog')
def blog_index():
	return blog_page(0)

@error(404)
def error404(error):
	return """<h1>404 - File Not Found</h1>
How do we found file?"""

months = ['January', 'Februrary', 'March',
		  'April', 'May', 'June',
		  'July', 'August', 'September',
		  'October', 'November', 'December']
def format_date(timestamp):
	time_object = time.localtime(timestamp)
	return months[time_object.tm_mon - 1] + " " + \
		str(time_object.tm_mday) + ", " + str(time_object.tm_year)

if __name__ == '__main__':
	run(host='localhost', port=8080, debug=True)
