from poab.tests import *

class TestMarocController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='maroc'))
        # Test response...
