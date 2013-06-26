from datetime import timedelta
from google.appengine.ext import db

class Greeting(db.Model):
  author = db.UserProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

  def DateTimeStr(self):
    pst = self.date + timedelta(hours=-8)
    return pst.strftime("%d-%b-%Y %I:%M:%S%p PST")

  def uniqueList(self):
      greetings = Greeting.all().order('-date').fetch(None)
      ulist = []
      last = ""
      for greeting in greetings:
        if last != greeting.content:
            ulist.append(greeting)
            last = greeting.content
      return ulist


