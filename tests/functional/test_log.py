from poab.tests import *

class TestLogController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='log'))
        # Test response...
