from poab.tests import *

class TestViewController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='view'))
        # Test response...
