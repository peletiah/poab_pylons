from poab.tests import *

class TestFeedController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='feed'))
        # Test response...
