import logging

from poab.lib.base import *
from sqlalchemy import asc, desc, and_, or_

import time, datetime
from decimal import Decimal, ROUND_HALF_UP


log = logging.getLogger(__name__)

class TrackController(BaseController):


    def index(self):
        c.markerlist='''['''
        try:
        #selection by date-range
            daterange=request.params['viewbydate']
            lastdate=daterange.split()[2]
            time_format = "%Y-%m-%d"
            lastdate = time.strptime(lastdate,time_format)
            lastdate=datetime.datetime(*lastdate[:6])
            delta = datetime.timedelta(days=1)
            q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.infomarker==True,model.trackpoint.timestamp > daterange.split()[0],model.trackpoint.timestamp <= lastdate+delta))
            c.infomarkers = q.order_by(asc(model.trackpoint.timestamp)).all()
            if c.infomarkers:
                pass
            else:
                #nothing found in the specified date-range
                q = model.Session.query(model.trackpoint).filter(model.trackpoint.infomarker==True)
                c.infomarkers = q.order_by(asc(model.trackpoint.timestamp)).all()
                c.error = 'no results for selected date(s)!'
        except KeyError:
        #selection of all entries
            q = model.Session.query(model.trackpoint).filter(model.trackpoint.infomarker==True)
            c.infomarkers = q.order_by(asc(model.trackpoint.timestamp)).all()
        for c.infomarker in c.infomarkers:
            q = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
            if q.count() == 1:
                c.track = q.one()
                total_mins = c.track.timespan.seconds / 60
                mins = total_mins % 60
                hours = total_mins / 60
                timespan = str(hours)+'h '+str(mins)+'min'
                rounded_distance=str(c.track.distance.quantize(Decimal("0.01"), ROUND_HALF_UP))+'km'
                date=c.track.date.strftime('%B %d, %Y')
                trackpts=c.track.gencpoly_pts
                tracklevels=c.track.gencpoly_levels
                trackcolor=c.track.color
            else:
                q = model.Session.query(model.timezone).filter(model.timezone.id==c.infomarker.timezone_id)
                c.timezone = q.one()
                localtime=c.infomarker.timestamp+c.timezone.utcoffset
                rounded_distance=''
                timespan=''
                date=localtime.strftime('%B %d, %Y')
                trackpts=''
                tracklevels=''
                trackcolor=''
            c.markerlist=c.markerlist + '''{'lat':%s, 'lon':%s, 'gal':"/track/gallery/%s", 'trackdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s"},''' % (c.infomarker.latitude,c.infomarker.longitude,c.infomarker.id,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor)
        c.markerlist=c.markerlist + '''];'''
        return render("/track/index.html")

    def gallery(self,id):
        q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==id)
        c.images = q.order_by(asc(model.imageinfo.flickrdatetaken)).limit(24)
        return render("/track/gallery.html")
    
    def infomarker(self,id):
        c.markerlist='''['''
        q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==id)
        c.infomarker = q.one()
        q = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
        if q.count() == 1:
            c.track = q.one()
            total_mins = c.track.timespan.seconds / 60
            mins = total_mins % 60
            hours = total_mins / 60
            timespan = str(hours)+'h '+str(mins)+'min'
            rounded_distance=str(c.track.distance.quantize(Decimal("0.01"), ROUND_HALF_UP))+'km'
            date=c.track.date.strftime('%B %d, %Y')
            trackpts=c.track.gencpoly_pts
            tracklevels=c.track.gencpoly_levels
            trackcolor=c.track.color
        else:
            q = model.Session.query(model.timezone).filter(model.timezone.id==c.infomarker.timezone_id)
            c.timezone = q.one()
            localtime=c.infomarker.timestamp+c.timezone.utcoffset
            rounded_distance=''
            timespan=''
            date=localtime.strftime('%B %d, %Y')
            trackpts=''
            tracklevels=''
            trackcolor=''
        c.markerlist=c.markerlist + '''{'lat':%s, 'lon':%s, 'gal':"/track/gallery/%s", 'trackdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s"},''' % (c.infomarker.latitude,c.infomarker.longitude,c.infomarker.id,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor)
        c.markerlist=c.markerlist + '''];'''
        return render("/track/index.html")

