import template
import json
import time
import argparse
import codecs
from markdown import markdown
from bottle import route, run, static_file, error, abort, redirect, request

import os

POSTS_DIR = './posts'
HOME_MESSAGE = './home.md'

class Page(object):
    def __init__(self, url, title):
        self.url = url
        self.title = title
pages = [
    Page('/', 'Home')
    ]

@route('/')
def blog_index():
    return blog_page(0)

@route('/<page_num:int>')
def blog_page(page_num):
    posts_folder = filter(lambda x: x[-5:] == '.json', os.listdir(POSTS_DIR))
    posts = []
    tags = request.query.get('tags')
    for filename in posts_folder:
        post = json.load(open(POSTS_DIR + '/' + filename))
        post['date'] = format_date(post['timestamp'])
        post['title'] = filename[:-5]
        post['text_location'] = POSTS_DIR + '/' + filename[:-5] + '.md'
        if tags is None or set(post['tags']).issuperset(tags.split()):
            posts.append(post)
    # equality is unlikely
    posts.sort(cmp=lambda a,b: -1 if a['timestamp'] > b['timestamp'] else 1)
    posts = posts[page_num*10:(page_num+1)*10]
    for i in xrange(len(posts)):
        posts[i]['body'] = markdown(codecs.open(posts[i]['text_location'], 'r', 'utf-8').read())
    return template.render("blog.html", {'posts': posts,
                                         'pages': pages,
                                         'page': pages[0] if page_num == 0 else None,
                                         'tags': "?tags=" + '+'.join(tags.split())
                                         if tags is not None else "",
                                         'next': '/' + str(page_num+1),
                                         'prev': ('/' + str(page_num-1))
                                         if page_num > 0 else None})
    
@route('/post/<post_name>')
def blog_post(post_name):
    try:
        post = json.load(open(POSTS_DIR + '/' + post_name + '.json'))
        post['date'] = format_date(post['timestamp'])
        post['title'] = post_name
        post['body'] = markdown(codecs.open(POSTS_DIR + '/' + post_name + '.md', 'r', 'utf-8').read())
        return template.render("blog.html", {'posts': [post],
                                             'pages': pages,
                                             'page': None,
                                             'tags': "",
                                             'next': None,
                                             'prev': None})
    except IOError:
        abort(404)

@route('/<something:path>/')
def slash_redir(something):
    redirect("/" + something)

@route('/css/<filename:re:.*\\.css>')
def serve_css(filename):
    return static_file(filename, root='./css', mimetype='text/css')

@route('/js/<filename:re:.*\\.js>')
def serve_js(filename):
    return static_file(filename, root='./js', mimetype='application/javascript')

@route('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root='./', mimetype='image/x-icon')

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
    arg_parser = argparse.ArgumentParser(
        description="Runs the spybee server.")
    arg_parser.add_argument("-d", "--debug", action="store_const",
                            const=True, default=False,
                            help="Turns on traceback on 500 errors and\n"
                            "sets host to 'localhost'")
    arg_parser.add_argument("-p", "--port", default="8080", nargs='?',
                            help="Port for server to listen on "
                            "(default: 8080).")
    args = arg_parser.parse_args().__dict__
    
    if not args['port'].isdigit():
        arg_parser.print_usage()
        print "error: port must be a decimal integer"
    else:
        run(host='localhost' if args['debug'] else '0.0.0.0',
            port=args['port'], debug=args['debug'],
	    server='paste')
