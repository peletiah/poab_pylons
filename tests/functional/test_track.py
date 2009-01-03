from poab.tests import *

class TestTrackController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='track'))
        # Test response...
