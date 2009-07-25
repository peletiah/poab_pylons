import logging

from poab.lib.base import *
from sqlalchemy import and_
import time, datetime

log = logging.getLogger(__name__)

class FactsController(BaseController):

    def index(self):
        return render("/facts/index.html")
         
