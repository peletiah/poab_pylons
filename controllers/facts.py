import logging

from poab.lib.base import *
from sqlalchemy import asc, desc, and_, or_
import time, datetime, calendar

log = logging.getLogger(__name__)

class FactsController(BaseController):

    def index(self):
        time_format = "%Y-%m-%d"
        birthday = datetime.datetime(*time.strptime('1980-10-02',time_format)[:6])
        now=datetime.datetime.now()
        c.age=(now-birthday).days/365
        return render("/facts/index.html")
 
    def stats(self,id):
        c.infomarker=id
        if id==None:
            q=model.Session.query(model.trackpoint).filter(model.trackpoint.infomarker==True)
            trackpoint=q.first()
            c.infomarker=trackpoint.id
        return render("/facts/stats.html")

    def infomarker(self,id):
        c.altitude='''{
label: 'Altitude(m)',
data:['''
        q=model.Session.query(model.trackpoint).filter(model.trackpoint.id==id)
        c.infomarker = q.one()
        q = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
        c.track = q.one()
        q=model.Session.query(model.trackpoint).filter(model.trackpoint.track_id==c.track.id)
        trackpoints=q.order_by(asc(model.trackpoint.timestamp)).all()
        for trackpoint in trackpoints:
            altitude=trackpoint.altitude
            timestamp=trackpoint.timestamp
            c.altitude=c.altitude+'''['''+str(calendar.timegm(timestamp.timetuple()) * 1000)+''', '''+str(altitude)+'''], '''
        c.altitude=c.altitude+''']}'''
        return c.altitude
        
