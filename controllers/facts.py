import logging

from poab.lib.base import *
from sqlalchemy import asc, desc, and_, or_
import time, datetime, calendar
from decimal import Decimal, ROUND_HALF_UP

log = logging.getLogger(__name__)

class FactsController(BaseController):

    def index(self):
        redirect_to(controller='facts', action='stats')
        time_format = "%Y-%m-%d"
        birthday = datetime.datetime(*time.strptime('1980-10-02',time_format)[:6])
        now=datetime.datetime.now()
        c.age=(now-birthday).days/365
        return render("/facts/index.html")
    
    def c(self,id):
        redirect_to(controller='facts', action='stats')
        return render("/facts/stats.html")


    def stats(self,id):
        #Total Distance:
        q = model.Session.query(model.track).filter(and_(model.track.distance!=None,model.track.date>='2010-08-31'))
        c.total_distance=int(q.sum(model.track.distance))
        c.daily_avg=int(c.total_distance/q.count())
        c.max_distance=int(q.order_by(desc(model.track.distance)).first().distance)
        c.min_distance=int(q.order_by(asc(model.track.distance)).first().distance)
        #Totals speed
        q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.timestamp>='2010-08-31', model.trackpoint.velocity>0, model.trackpoint.velocity<70))
        c.avg_speed=q.sum(model.trackpoint.velocity)/q.count()
        #Totals altitude
        q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.timestamp>='2010-08-31', model.trackpoint.altitude!=None))
        c.max_altitude=q.order_by(desc(model.trackpoint.altitude)).first().altitude
        c.min_altitude=q.order_by(asc(model.trackpoint.altitude)).first().altitude
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

    def distance(self,id):
        c.distance='''{
label: 'Distance(km)',
data:['''
        q=model.Session.query(model.trackpoint).filter(model.trackpoint.id==id)
        c.infomarker = q.one()
        q = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
        c.track = q.one()
        q=model.Session.query(model.trackpoint).filter(model.trackpoint.track_id==c.track.id)
        trackpoint=q.order_by(asc(model.trackpoint.timestamp)).first()
        oldlat=float(trackpoint.latitude)
        oldlon=float(trackpoint.longitude)
        distance=0
        trackpoints=q.order_by(asc(model.trackpoint.timestamp)).all()
        for trackpoint in trackpoints:
            newlat=float(trackpoint.latitude)
            newlon=float(trackpoint.longitude)
            if oldlat==newlat and oldlon==newlon:
                pass
            else:
                try:
                    distance=distance+h.distance_on_unit_sphere(oldlat, oldlon, newlat, newlon)*6373
                except typeError:
                    return oldlat,oldlon,newlat,newlon
            oldlat=newlat
            oldlon=newlon
            timestamp=trackpoint.timestamp
            c.distance=c.distance+'''['''+str(calendar.timegm(timestamp.timetuple()) * 1000)+''', '''+str(distance)+'''], '''
        c.distance=c.distance+''']}'''
        return c.distance
