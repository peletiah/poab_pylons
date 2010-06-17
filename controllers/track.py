import logging

from poab.lib.base import *
from sqlalchemy import asc, desc, and_, or_

import time, datetime
from decimal import Decimal, ROUND_HALF_UP


log = logging.getLogger(__name__)

class TrackController(BaseController):


    def index(self):
        c.markerlist='''['''
        c.country_shapes_list='''['''
        #selection of all entries
        q = model.Session.query(model.trackpoint).filter(model.trackpoint.infomarker==True)
        c.infomarkers = q.order_by(asc(model.trackpoint.timestamp)).all()
        for c.infomarker in c.infomarkers:
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.id)
            if q.count() > 0:
                firstimage = q.order_by(asc(model.imageinfo.id)).limit(1)
                for image in firstimage:
                    #creates the infomarker-image_icon-and-ajax-link(fancy escaping for js needed):
                    gallerylink="""<span class=\\"image_icon\\"><a href=\\"javascript:showSubcontent(\'/view/gallery/%s/%s\')\\"></a></span>""" % (c.infomarker.id,image.id)
            else:
                gallerylink=''
            q = model.Session.query(model.log).filter(model.log.infomarker_id==c.infomarker.id)
            if q.count() > 0:
                #creates the infomarker-log_icon-and-ajax-link(fancy escaping for js needed)                
                loglink="""<span class=\\"log_icon\\"><a href=\\"javascript:showSubcontent(\'/log/minimal/%s\')\\"></a></span>""" % (c.infomarker.id)
            else:
                loglink=''

            q = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
            if q.count() == 1:
                c.track = q.one()
                total_mins = c.track.timespan.seconds / 60
                mins = total_mins % 60
                hours = total_mins / 60
                timespan = '<b>duration:</b> %sh%smin<br />' % (str(hours),str(mins))
                rounded_distance='<b>distance:</b> %skm<br />' % (str(c.track.distance.quantize(Decimal("0.01"), ROUND_HALF_UP)))
                date=c.track.date.strftime('%B %d, %Y')
                trackpts=c.track.gencpoly_pts
                tracklevels=c.track.gencpoly_levels
                trackcolor=c.track.color
            else:
                q = model.Session.query(model.timezone).filter(model.timezone.id==c.infomarker.timezone_id)
                c.timezone = q.one()
                localtime=c.infomarker.timestamp+c.timezone.utcoffset
                date=localtime.strftime('%B %d, %Y')
                rounded_distance=''
                timespan=''
                trackpts=''
                tracklevels=''
                trackcolor=''
            q = model.Session.query(model.country_shapes).filter(model.country_shapes.country_id==32)
            country_shapes=q.all()
            for country_shape in country_shapes:
                c.country_shapes_list=c.country_shapes_list+'''{'encpts':"%s",'enclvl':"%s",'shapecolor':"%s"},''' % (country_shape.gencpoly_pts,country_shape.gencpoly_levels,country_shape.color)
                
            c.markerlist=c.markerlist + '''{'lat':%s, 'lon':%s, 'gal':"%s",'log':"%s", 'markerdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s"},''' % (c.infomarker.latitude,c.infomarker.longitude,gallerylink,loglink,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor)
        c.country_shapes_list=(c.country_shapes_list + '''];''').replace('},];','}];')
        c.markerlist=(c.markerlist + '''];''').replace('},];','}];')
        return render("/track/index.html")

    def infomarker(self,id):
        q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==id)
        c.infomarker = q.one()
        q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.id)
        if q.count() > 0:
            firstimage = q.order_by(asc(model.imageinfo.id)).limit(1)
            for image in firstimage:
                #creates the infomarker-image_icon-and-ajax-link(fancy escaping for js needed):
                gallerylink="""<span class=\\"image_icon\\"><a href=\\"javascript:showSubcontent(\'/view/gallery/%s/%s\')\\"></a></span>""" % (c.infomarker.id,image.id)
        else:
            gallerylink=''
        q = model.Session.query(model.log).filter(model.log.infomarker_id==c.infomarker.id)
        if q.count() > 0:
            #creates the infomarker-log_icon-and-ajax-link(fancy escaping for js needed):
            loglink="""<span class=\\"log_icon\\"><a href=\\"javascript:showSubcontent(\'/log/minimal/%s\')\\"></a></span>""" % (c.infomarker.id)
        else:
            loglink=''
        q = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
        if q.count() == 1:
            c.track = q.one()
            total_mins = c.track.timespan.seconds / 60
            mins = total_mins % 60
            hours = total_mins / 60
            timespan = '<b>duration:</b> %sh%smin<br />' % (str(hours),str(mins))
            rounded_distance = '<b>distance:</b> %skm<br />' % (str(c.track.distance.quantize(Decimal("0.01"), ROUND_HALF_UP)))
            date=c.track.date.strftime('%B %d, %Y')
            trackpts=c.track.gencpoly_pts
            tracklevels=c.track.gencpoly_levels
            trackcolor=c.track.color
        else:
            #WTF is happening here?
            q = model.Session.query(model.timezone).filter(model.timezone.id==c.infomarker.timezone_id)
            c.timezone = q.one()
            localtime=c.infomarker.timestamp+c.timezone.utcoffset
            rounded_distance=''
            timespan=''
            date=localtime.strftime('%B %d, %Y')
            trackpts=''
            tracklevels=''
            trackcolor=''
        c.markerlist='''[{'lat':%s, 'lon':%s, 'gal':"%s",'log':"%s", 'markerdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s"}];''' % (c.infomarker.latitude,c.infomarker.longitude,gallerylink,loglink,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor)
        return render("/track/index.html")



    def simple(self,trackpoint,imageid):
        q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==trackpoint)
        c.trackpoint = q.one()
        q = model.Session.query(model.track).filter(model.track.id==c.trackpoint.track_id)
        if q.count() == 1:
            c.track = q.one()
            total_mins = c.track.timespan.seconds / 60
            mins = total_mins % 60
            hours = total_mins / 60
            timespan = '<b>duration:</b> %sh%smin<br />' % (str(hours),str(mins))
            location = c.trackpoint.location
            date=c.track.date.strftime('%B %d, %Y')
            trackpts=c.track.gencpoly_pts
            tracklevels=c.track.gencpoly_levels
            trackcolor=c.track.color
        else:
            #WTF is happening here?
            q = model.Session.query(model.timezone).filter(model.timezone.id==c.trackpoint.timezone_id)
            c.timezone = q.one()
            localtime=c.trackpoint.timestamp+c.timezone.utcoffset
            location=c.trackpoint.location
            timespan=''
            date=localtime.strftime('%B %d, %Y')
            trackpts=''
            tracklevels=''
            trackcolor=''
        q = model.Session.query(model.imageinfo).filter(model.imageinfo.id==imageid)
        c.imageinfo=q.one()
        flickrthumb='http://farm%s.static.flickr.com/%s/%s_%s_t.jpg' % (c.imageinfo.flickrfarm,c.imageinfo.flickrserver,c.imageinfo.flickrphotoid,c.imageinfo.flickrsecret)
        c.markerlist='''[{'lat':%s, 'lon':%s, 'altitude':%s, 'markerdate':"%s", 'location':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s", 'flickrthumb':"%s"}];''' % (c.trackpoint.latitude,c.trackpoint.longitude,c.trackpoint.altitude,date,location,timespan,trackpts,tracklevels,trackcolor,flickrthumb)
        return render("/track/minimal_map.html")


    def tabbed_solo(self):
        c.markerlist='''['''
        q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.infomarker==True,model.trackpoint.id==113328))
        c.infomarkers = q.order_by(asc(model.trackpoint.timestamp)).all()
        for c.infomarker in c.infomarkers:
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.id)
            if q.count() > 0:
                firstimage = q.order_by(asc(model.imageinfo.id)).limit(1)
                for image in firstimage:
                    #creates the infomarker-image_icon-and-ajax-link(fancy escaping for js needed):
                    gallerylink="""<span class=\\"image_icon\\"><a href=\\"javascript:showSubcontent(\'/view/gallery/%s/%s\')\\"></a></span>""" % (c.infomarker.id,image.id)
            else:
                gallerylink=''
            q = model.Session.query(model.log).filter(model.log.infomarker_id==c.infomarker.id)
            if q.count() > 0:
                #creates the infomarker-log_icon-and-ajax-link(fancy escaping for js needed)                
                loglink="""<span class=\\"log_icon\\"><a href=\\"javascript:showSubcontent(\'/log/minimal/%s\')\\"></a></span>""" % (c.infomarker.id)
            else:
                loglink=''

            q = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
            if q.count() == 1:
                c.track = q.one()
                total_mins = c.track.timespan.seconds / 60
                mins = total_mins % 60
                hours = total_mins / 60
                timespan = '<b>duration:</b> %sh%smin<br />' % (str(hours),str(mins))
                rounded_distance='<b>distance:</b> %skm<br />' % (str(c.track.distance.quantize(Decimal("0.01"), ROUND_HALF_UP)))
                date=c.track.date.strftime('%B %d, %Y')
                trackpts=c.track.gencpoly_pts
                tracklevels=c.track.gencpoly_levels
                trackcolor=c.track.color
                q = model.Session.query(model.trackpoint).filter(model.trackpoint.track_id==c.infomarker.track_id)
                if q.count() > 1:
                    trackpoints = q.all()
                    c.trkptlist='''['''
                    for trackpoint in trackpoints:
                        c.trkptlist=c.trkptlist+'''(%s, %s),''' % (str(trackpoint.latitude),str(trackpoint.longitude))
                    trkptlist=(c.trkptlist + ''']''').replace(',]',']')                              
                else:
                    trkptlist=''
            else:
                q = model.Session.query(model.timezone).filter(model.timezone.id==c.infomarker.timezone_id)
                c.timezone = q.one()
                localtime=c.infomarker.timestamp+c.timezone.utcoffset
                date=localtime.strftime('%B %d, %Y')
                rounded_distance=''
                timespan=''
                trackpts=''
                tracklevels=''
                trackcolor=''
                trkptlist=''
            c.markerlist=c.markerlist + '''{'lat':%s, 'lng':%s, 'gal':"%s",'log':"%s", 'markerdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s", 'trkptlist':"%s"},''' % (c.infomarker.latitude,c.infomarker.longitude,gallerylink,loglink,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor,trkptlist)
        c.markerlist=(c.markerlist + '''];''').replace('},];','}];')
        #return trkptlist
        return render("/track/tabbed_solo.html")
 
        
 
    def tabbed(self):
        c.markerlist='''['''
        q = model.Session.query(model.trackpoint).filter(model.trackpoint.infomarker==True)
        c.infomarkers = q.order_by(asc(model.trackpoint.timestamp)).all()
        for c.infomarker in c.infomarkers:
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.id)
            if q.count() > 0:
                firstimage = q.order_by(asc(model.imageinfo.id)).limit(1)
                for image in firstimage:
                    #creates the infomarker-image_icon-and-ajax-link(fancy escaping for js needed):
                    gallerylink="""<span class=\\"image_icon\\"><a href=\\"javascript:showSubcontent(\'/view/gallery/%s/%s\')\\"></a></span>""" % (c.infomarker.id,image.id)
            else:
                gallerylink=''
            q = model.Session.query(model.log).filter(model.log.infomarker_id==c.infomarker.id)
            if q.count() > 0:
                #creates the infomarker-log_icon-and-ajax-link(fancy escaping for js needed)                
                loglink="""<span class=\\"log_icon\\"><a href=\\"javascript:showSubcontent(\'/log/minimal/%s\')\\"></a></span>""" % (c.infomarker.id)
            else:
                loglink=''

            q = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
            if q.count() == 1:
                c.track = q.one()
                total_mins = c.track.timespan.seconds / 60
                mins = total_mins % 60
                hours = total_mins / 60
                timespan = '<b>duration:</b> %sh%smin<br />' % (str(hours),str(mins))
                rounded_distance='<b>distance:</b> %skm<br />' % (str(c.track.distance.quantize(Decimal("0.01"), ROUND_HALF_UP)))
                date=c.track.date.strftime('%B %d, %Y')
                trackpts=c.track.gencpoly_pts
                tracklevels=c.track.gencpoly_levels
                trackcolor=c.track.color
            else:
                q = model.Session.query(model.timezone).filter(model.timezone.id==c.infomarker.timezone_id)
                c.timezone = q.one()
                localtime=c.infomarker.timestamp+c.timezone.utcoffset
                date=localtime.strftime('%B %d, %Y')
                rounded_distance=''
                timespan=''
                trackpts=''
                tracklevels=''
                trackcolor=''
            c.markerlist=c.markerlist + '''{'lat':%s, 'lng':%s, 'gal':"%s",'log':"%s", 'markerdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s"},''' % (c.infomarker.latitude,c.infomarker.longitude,gallerylink,loglink,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor)
        c.markerlist=(c.markerlist + '''];''').replace('},];','}];')
        #return c.markerlist
        return render("/track/tabbed.html")
 
        
