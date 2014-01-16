from jinja2 import Environment, FileSystemLoader
from pyhaml_jinja import HamlExtension
from flask import Flask
from flask import session
import os
from datetime import datetime

app = Flask(__name__)


def get_news_items():

  class NewsItem(object):

    # This is the initiator of the class. This is the 1st thing that will be
    # called when the class is invoked.
    def __init__(self, title, date_created):
      self.title = title
      self.date_created = date_created

    # This function allows a string to be displayed when the class is printed.
    def __str__(self):
      return 'News item: %s' % self.title

  item = NewsItem(title='Title of my article!!', date_created=datetime.now())
  return [item, item, item, item]

def get_current_profile():
  return session.get('username')

def render_template(template_name, data):

  # Gets the current location of this file.
  app_root = os.path.dirname(__file__)

  # Adds /templates to the current directory.
  template_root = os.path.join(app_root, 'templates')
  env = Environment(extensions=[HamlExtension], loader=
    FileSystemLoader(template_root))
  template = env.get_template(template_name)
  return template.render(data)

# `home` is the function that is mapped on to the `/` route.
@app.route('/')
def home():
  items = get_news_items()
  profile = get_current_profile()
  items = sorted(items, key=lambda i: i.date_created)
  html = render_template(
      template_name='home.haml',
      data={'items': items, 'profile': profile})
  return html

@app.route('/login')
def login():
  session['username'] = 'jj'
  return 'Logged in...'

@app.route('/logout')
def logout():
  session.pop('username', None)
  return 'Logged out...'

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
  app.run(debug=True)
