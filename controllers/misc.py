import logging

from poab.lib.base import *

log = logging.getLogger(__name__)

class MiscController(BaseController):

    def index(self):
        return render("/misc/index.html")

    def navstring(self,country_id):
        c.navstring=h.countryDetails(model,int(country_id)).replace('\\','')
        return c.navstring

    def country_svg(self,country_id):
        country_id=int(country_id)
        if country_id==0:
            return render("/misc/world_svg.html")

        q = model.Session.query(model.country).filter(model.country.iso_numcode==country_id)
        c.country=q.one()
        return render("/misc/country_svg.html")
