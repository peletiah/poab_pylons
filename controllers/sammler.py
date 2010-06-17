import logging

from poab.lib.base import *

log = logging.getLogger(__name__)

class SammlerController(BaseController):

    def index(self):
        return render("/sammler/index.html")
