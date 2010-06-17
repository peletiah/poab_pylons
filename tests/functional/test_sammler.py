from poab.tests import *

class TestSammlerController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='sammler'))
        # Test response...
