from poab.tests import *

class TestTrackFullController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='track_full'))
        # Test response...
