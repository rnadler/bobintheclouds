import os
from google.appengine.ext.webapp import template

import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from datetime import timedelta

class Greeting(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
  def DateTimeStr(self):
    pst = self.date + timedelta(hours=-8)
    return pst.strftime("%d-%b-%Y %I:%M:%S%p PST")

class MainPage(webapp.RequestHandler):
  def get(self):
    greetings_query = Greeting.all().order('-date')
    greetings = greetings_query.fetch(500)

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    template_values = {
      'greetings': greetings,
      'url': url,
      'url_linktext': url_linktext,
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class Guestbook(webapp.RequestHandler):
  def post(self):
    greeting = Greeting()
    cont = self.request.get('content')
    if cont != "":
        if cont.lower().find("http") >= 0:
            self.response.out.write("<h4>Sorry, HTTP is not allowed in the comment.</h4>Use the Back button to return to the Guest Book.")
            return
        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = cont
        greeting.put()
        self.redirect('/')
    else:
      self.response.out.write("<h4>Please enter a comment.</h4>Use the Back button to return to the Guest Book.")

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
