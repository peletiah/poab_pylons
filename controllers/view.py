import logging

from poab.lib.base import *

log = logging.getLogger(__name__)

class ViewController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
        return render("/view/index.html")
