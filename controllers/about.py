import logging

from poab.lib.base import *
from sqlalchemy import asc, desc, and_, or_
import time, datetime, calendar

log = logging.getLogger(__name__)

class AboutController(BaseController):

    def index(self):
        time_format = "%Y-%m-%d"
        birthday = datetime.datetime(*time.strptime('1980-10-02',time_format)[:6])
        now=datetime.datetime.now()
        c.age=(now-birthday).days/365
        return render("/about/index.html")

    def c(self):
        time_format = "%Y-%m-%d"
        birthday = datetime.datetime(*time.strptime('1980-10-02',time_format)[:6])
        now=datetime.datetime.now()
        c.age=(now-birthday).days/365
        return render("/about/index.html")


