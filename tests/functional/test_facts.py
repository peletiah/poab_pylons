from poab.tests import *

class TestFactsController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='facts'))
        # Test response...
