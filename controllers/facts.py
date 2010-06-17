import logging

from poab.lib.base import *
from sqlalchemy import asc, desc, and_, or_
import time, datetime, calendar
import calc_distance

log = logging.getLogger(__name__)

class FactsController(BaseController):

    def index(self):
        redirect_to(controller='facts', action='stats')
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
                    distance=distance+calc_distance.distance_on_unit_sphere(oldlat, oldlon, newlat, newlon)*6373
                except typeError:
                    return oldlat,oldlon,newlat,newlon
            oldlat=newlat
            oldlon=newlon
            timestamp=trackpoint.timestamp
            c.distance=c.distance+'''['''+str(calendar.timegm(timestamp.timetuple()) * 1000)+''', '''+str(distance)+'''], '''
        c.distance=c.distance+''']}'''
        return c.distance

    def tabbed(self,id):
        c.infomarker=id
        if id==None:
            q=model.Session.query(model.trackpoint).filter(model.trackpoint.infomarker==True)
            trackpoint=q.first()
            c.infomarker=trackpoint.id
        return render("/facts/tabbed.html")


