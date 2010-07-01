from poab.tests import *

class TestMiscController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='misc'))
        # Test response...
