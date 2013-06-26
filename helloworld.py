import os
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users
from greeting import Greeting


class MainPage(webapp2.RequestHandler):
  def get(self):
    greetings = Greeting().uniqueList()

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

class Guestbook(webapp2.RequestHandler):
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

application = webapp2.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook)],
                                     debug=True)