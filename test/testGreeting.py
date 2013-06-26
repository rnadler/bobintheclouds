import unittest
from google.appengine.ext import db
from google.appengine.ext import testbed
from greeting import Greeting


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def addGreeting(self, content):
        greeting = Greeting()
        greeting.content = content
        greeting.put()

    def clearGreetingDb(self):
        for g in Greeting.all():
            Greeting.delete(g)

    def testInsertEntity(self):
        Greeting().put()
        self.assertEqual(1, len(Greeting.all().fetch(2)))

    def testUniqueList(self):
        self.clearGreetingDb()
        self.addGreeting("one")
        self.addGreeting("two")
        self.addGreeting("two")
        self.addGreeting("two")
        self.addGreeting("three")
        self.assertEqual(5, len(Greeting().all().fetch(None)))
        self.assertEqual(3, len(Greeting().uniqueList()))


if __name__ == '__main__':
    unittest.main()
