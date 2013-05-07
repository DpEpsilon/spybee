import template
from markdown import markdown
from bottle import route, run, static_file, error

class Page(object):
	def __init__(self, url, title):
		self.url = url
		self.title = title
pages = [
	Page('/', 'Home'),
	Page('/blah', 'Stuff'),
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

@route('/blog/<post>')
def blog_post(post):
	return markdown(open('./posts/' + post + '.md').read())

@error(404)
def error404(error):
	return """<h1>404 - File Not Found</h1>
How do we found file?"""

if __name__ == '__main__':
	run(host='localhost', port=8080, debug=True)
