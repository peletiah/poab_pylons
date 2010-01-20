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
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.id)
            if q.count() > 0:
                firstimage = q.order_by(asc(model.imageinfo.id)).limit(1)
                for image in firstimage:
                    #creates the infomarker-image_icon-and-ajax-link(fancy escaping for js needed):
                    gallerylink="""<span class=\\"image_icon\\"><a href=\\"javascript:showSubcontent(\'/track/gallery/%s/%s\')\\"></a></span>""" % (c.infomarker.id,image.id)
            else:
                gallerylink=''
            q = model.Session.query(model.log).filter(model.log.infomarker_id==c.infomarker.id)
            if q.count() > 0:
                firstlog = q.order_by(asc(model.log.id)).limit(1)
                for log in firstlog:
                    #creates the infomarker-log_icon-and-ajax-link(fancy escaping for js needed):
                    loglink="""<span class=\\"log_icon\\"><a href=\\"javascript:showSubcontent(\'/track/log/%s/%s\')\\"></a></span>""" % (c.infomarker.id,log.id)
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
            c.markerlist=c.markerlist + '''{'lat':%s, 'lon':%s, 'gal':"%s",'log':"%s", 'markerdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s"},''' % (c.infomarker.latitude,c.infomarker.longitude,gallerylink,loglink,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor)
        c.markerlist=c.markerlist + '''];'''
        return render("/track/index.html")

    def infomarker(self,id):
        c.markerlist='''['''
        q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==id)
        c.infomarker = q.one()
        q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.id)
        if q.count() > 0:
            firstimage = q.order_by(asc(model.imageinfo.id)).limit(1)
            for image in firstimage:
                #creates the infomarker-image_icon-and-ajax-link(fancy escaping for js needed):
                gallerylink="""<span class=\\"image_icon\\"><a href=\\"javascript:showSubcontent(\'/track/gallery/%s/%s\')\\"></a></span>""" % (c.infomarker.id,image.id)
        else:
            gallerylink=''
        q = model.Session.query(model.log).filter(model.log.infomarker_id==c.infomarker.id)
        if q.count() > 0:
            firstlog = q.order_by(asc(model.log.id)).limit(1)
            for log in firstlog:
                #creates the infomarker-log_icon-and-ajax-link(fancy escaping for js needed):
                loglink="""<span class=\\"log_icon\\"><a href=\\"javascript:showSubcontent(\'/track/log/%s/%s\')\\"></a></span>""" % (c.infomarker.id,log.id)
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
        c.markerlist=c.markerlist + '''{'lat':%s, 'lon':%s, 'gal':"%s",'log':"%s", 'markerdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s"},''' % (c.infomarker.latitude,c.infomarker.longitude,gallerylink,loglink,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor)
        c.markerlist=c.markerlist + '''];'''
        return render("/track/index.html")



    def gallery(self,infomarker,startfromimg):
        #first imageid
        q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==infomarker)
        firstimage = q.order_by(asc(model.imageinfo.id)).limit(1)
        for image in firstimage:
            c.firstimageid=image.id
        #last imageid
        lastimage = q.order_by(desc(model.imageinfo.id)).limit(1)
        for image in lastimage:
            c.lastimageid=image.id
        #imagedetails for the current page
        q = model.Session.query(model.imageinfo).filter(and_(model.imageinfo.infomarker_id==infomarker,model.imageinfo.id >= startfromimg))
        c.images = q.order_by(asc(model.imageinfo.flickrdatetaken)).limit(24)
        #last imageid on current page
        images_asc = q.order_by(asc(model.imageinfo.id)).limit(24)
        for image in images_asc:
                c.lastimgonpage=image.id
        #count images on current page
        c.imagecount = q.limit(24).count()
        #first imageid on current page(no limit to 24 as we order decreasing and want the first id, not the 24th from the end)
        images_desc = q.order_by(desc(model.imageinfo.id)).all()
        for image in images_desc:
                c.firstimgonpage=image.id
        #first imageid on next page
        imagesnextpage = q.order_by(asc(model.imageinfo.id)).limit(25)
        for image in imagesnextpage:
                c.startfromimg=image.id
        #first imageid on previous page
        q = model.Session.query(model.imageinfo).filter(and_(model.imageinfo.infomarker_id==infomarker,model.imageinfo.id < c.startfromimg))
        if c.imagecount==24:
            imagesprevpage = q.order_by(desc(model.imageinfo.id)).limit(48)
        else:
            #there are less than 24 images on the page, so imagesprevpage is not 2x24 pictures away
            imagesprevpage = q.order_by(desc(model.imageinfo.id)).limit(23+c.imagecount)
        for image in imagesprevpage:
                c.prevstartfromimg=image.id
        return render("/track/gallery.html")
    

