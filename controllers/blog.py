import logging

from poab.lib.base import *

log = logging.getLogger(__name__)

class BlogController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
	q = model.Session.query(model.log)
        c.posts = q.limit(10)
        return render("/log/index.html")

    def show(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
	q = model.Session.query(model.log)
        c.posts = q.limit(10)
        return render("/log/index.html")
