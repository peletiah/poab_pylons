import logging

from poab.lib.base import *

log = logging.getLogger(__name__)

class TrackController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
	bla='asdf'
	c.markerlist='''['''
	q = model.Session.query(model.trackpoint).filter(model.trackpoint.infomarker==True)
	c.infomarkers = q.all()
	for c.infomarker in c.infomarkers:
	    q2 = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
	    c.tracks = q2.all()
	    q3 = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.track_id)
	    c.images = q3.all()
	    for c.track in c.tracks:
		c.markerlist=c.markerlist + '''{'lat':%s, 'lon':%s, 'gal':"gallery/%s", 'encpts':"%s", 'enclvl':"%s"}''' % (c.infomarker.latitude,c.infomarker.longitude,c.infomarker.id,c.track.gencpoly_pts,c.track.gencpoly_levels)
	c.markerlist=c.markerlist + '''];'''
        return render("/track/index.html")

    def gallery(self,id):
	q3 = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==id)
	c.images = q3.limit(5)
    	return render("/track/gallery.html")



