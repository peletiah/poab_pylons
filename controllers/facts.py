import logging

from poab.lib.base import *
from sqlalchemy import and_
import time, datetime

log = logging.getLogger(__name__)

class FactsController(BaseController):

    def index(self):
        time_format = "%Y-%m-%d"
        birthday = datetime.datetime(*time.strptime('1980-10-02',time_format)[:6])
        now=datetime.datetime.now()
        c.age=(now-birthday).days/365
        return render("/facts/index.html")
 
    def stats(self):
        return render("/facts/stats.html")
         
