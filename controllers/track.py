import logging

from poab.lib.base import *
from sqlalchemy import and_
import time, datetime

log = logging.getLogger(__name__)

class TrackController(BaseController):

    def index(self):
	c.markerlist='''['''
	try:
	    daterange=request.params['viewbydate']
	    lastdate=daterange.split()[2]
	    time_format = "%Y-%m-%d"
	    lastdate = time.strptime(lastdate,time_format)
	    lastdate=datetime.datetime(*lastdate[:6])
	    delta = datetime.timedelta(days=1)
	    q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.infomarker==True,model.trackpoint.timestamp > daterange.split()[0],model.trackpoint.timestamp <= lastdate+delta))
	    c.infomarkers = q.all()
	    if c.infomarkers:
		pass
	    else:
		q = model.Session.query(model.trackpoint).filter(model.trackpoint.infomarker==True)
		c.infomarkers = q.all()
		c.error = 'no results for selected date(s)!'
	except KeyError:
	    q = model.Session.query(model.trackpoint).filter(model.trackpoint.infomarker==True)
	    c.infomarkers = q.all()
        for c.infomarker in c.infomarkers:
            q = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
            c.tracks = q.all()
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.track_id)
            c.images = q.limit(8)
            for c.track in c.tracks:
                c.markerlist=c.markerlist + '''{'lat':%s, 'lon':%s, 'gal':"/track/gallery/%s", 'encpts':"%s", 'enclvl':"%s"},''' % (c.infomarker.latitude,c.infomarker.longitude,c.infomarker.id,c.track.gencpoly_pts,c.track.gencpoly_levels)
        c.markerlist=c.markerlist + '''];'''
        return render("/track/index.html")

    def gallery(self,id):
	q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==id)
	c.images = q.limit(24)
    	return render("/track/gallery.html")


