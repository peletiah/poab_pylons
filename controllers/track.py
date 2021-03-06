import logging

from poab.lib.base import *
from sqlalchemy import asc, desc, and_, or_

import time, datetime
from decimal import Decimal, ROUND_HALF_UP
import re


log = logging.getLogger(__name__)

class TrackController(BaseController):


    def index(self):
        redirect_to(action='c')
        

    def c(self,id1):
        c.markerlist='''['''
        older_createdate='2010-08-31'
        c.country_id=int(id1)
        c.navstring=h.countryDetails(model,c.country_id)
        #selection of all entries
        if c.country_id==0:
            q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.infomarker==True,model.trackpoint.timestamp>=older_createdate))
        else:
            q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.country_id==c.country_id,model.trackpoint.infomarker==True))
        c.infomarkers = q.order_by(asc(model.trackpoint.timestamp)).all()
        for c.infomarker in c.infomarkers:
            q = model.Session.query(model.log).filter(model.log.infomarker_id==c.infomarker.id)
            if q.count() > 0:
                #creates the infomarker-log_icon-and-ajax-link(fancy escaping for js needed)                
                loglink="""<span class=\\"log_icon\\"><a href=\\"javascript:map_shrink();showSubcontent(\'/log/minimal/%s\')\\"></a></span>""" % (c.infomarker.id)
                log=q.first()
                p=re.compile("http://twitter.com/derreisende/statuses/(?P<guid>\d{1,})")
                if p.search(log.topic):
                    c.twitter=True
                else:
                    c.twitter=False
            else:
                loglink=''
            if c.infomarker.id!=1 and c.twitter==False:
                q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.id)
                if q.count() > 0:
                    firstimage = q.order_by(asc(model.imageinfo.id)).limit(1)
                    for image in firstimage:
                        #creates the infomarker-image_icon-and-ajax-link(fancy escaping for js needed):
                        gallerylink="""<span class=\\"image_icon\\"><a href=\\"javascript:map_shrink();showSubcontent(\'/view/gallery/%s/%s\')\\"></a></span>""" % (c.infomarker.id,image.id)
                else:
                    gallerylink=''
                
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
                    maxlat=c.track.maxlat
                    maxlon=c.track.maxlon
                    minlat=c.track.minlat
                    minlon=c.track.minlon
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
                    maxlat=''
                    maxlon=''
                    minlat=''
                    minlon=''
                if c.twitter!=True:
                    c.markerlist=c.markerlist + '''{'lat':%s, 'lon':%s, 'gal':"%s",'log':"%s", 'markerdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s", 'maxlat':"%s", 'maxlon':"%s", 'minlat':"%s",'minlon':"%s"},''' % (c.infomarker.latitude,c.infomarker.longitude,gallerylink,loglink,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor,maxlat,maxlon,minlat,minlon)
                    #c.markerlist=c.markerlist + '''{'lat':%s, 'lon':%s, 'gal':"%s",'log':"%s", 'markerdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s"},''' % (c.infomarker.latitude,c.infomarker.longitude,gallerylink,loglink,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor)
        c.markerlist=(c.markerlist + '''];''').replace('},];','}];')
        return render("/track/index.html")

    def infomarker(self,id):
        c.country_id=0
        q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==id)
        c.infomarker = q.one()
        q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.id)
        if q.count() > 0:
            firstimage = q.order_by(asc(model.imageinfo.id)).limit(1)
            for image in firstimage:
                #creates the infomarker-image_icon-and-ajax-link(fancy escaping for js needed):
                gallerylink="""<span class=\\"image_icon\\"><a href=\\"javascript:map_shrink();showSubcontent(\'/view/gallery/%s/%s\')\\"></a></span>""" % (c.infomarker.id,image.id)
        else:
            gallerylink=''
        q = model.Session.query(model.log).filter(model.log.infomarker_id==c.infomarker.id)
        if q.count() > 0:
            #creates the infomarker-log_icon-and-ajax-link(fancy escaping for js needed):
            loglink="""<span class=\\"log_icon\\"><a href=\\"javascript:map_shrink();showSubcontent(\'/log/minimal/%s\')\\"></a></span>""" % (c.infomarker.id)
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
            maxlat=c.track.maxlat
            maxlon=c.track.maxlon
            minlat=c.track.minlat
            minlon=c.track.minlon
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
            maxlat=''
            maxlon=''
            minlat=''
            minlon=''
        c.markerlist='''[{'lat':%s, 'lon':%s, 'gal':"%s",'log':"%s", 'markerdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s", 'maxlat':"%s", 'maxlon':"%s", 'minlat':"%s",'minlon':"%s",}];''' % (c.infomarker.latitude,c.infomarker.longitude,gallerylink,loglink,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor,maxlat,maxlon,minlat,minlon)
        c.navstring='''<li class="navigation"><ul><li class="navli"><a href="#" title="Journal-entries for all countries" onclick="resetContent\(\);">All</a>&#8594; Infomarker &#8594;<a href="/track/infomarker/%s" title="View track %s alone">%s</a></li></ul></li>''' % (c.infomarker.id,c.infomarker.id,c.infomarker.id)
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
        if c.trackpoint.altitude==None:
            altitude=""
        else:
            altitude=c.trackpoint.altitude
        if imageid!=None:
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.id==imageid)
            c.imageinfo=q.one()
            flickrthumb='http://farm%s.static.flickr.com/%s/%s_%s_t.jpg' % (c.imageinfo.flickrfarm,c.imageinfo.flickrserver,c.imageinfo.flickrphotoid,c.imageinfo.flickrsecret)
        else:
            flickrthumb=""
        c.markerlist='''[{'lat':%s, 'lon':%s, 'altitude':"%s", 'markerdate':"%s", 'location':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s", 'flickrthumb':"%s"}];''' % (c.trackpoint.latitude,c.trackpoint.longitude,altitude,date,location,timespan,trackpts,tracklevels,trackcolor,flickrthumb)
        return render("/track/minimal_map.html")

    def markerbounds(self,country_id):
        c.markerlist='''['''
        c.country_id=int(country_id)
        c.navstring=h.countryDetails(model,c.country_id)
        #selection of all entries
        if c.country_id==0:
            q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.infomarker==True,model.trackpoint.timestamp>='2010-08-31'))
        else:
            q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.country_id==c.country_id,model.trackpoint.infomarker==True))
        c.infomarkers = q.order_by(asc(model.trackpoint.timestamp)).all()
        for c.infomarker in c.infomarkers:
            q = model.Session.query(model.log).filter(model.log.infomarker_id==c.infomarker.id)
            if q.count() > 0:
                #creates the infomarker-log_icon-and-ajax-link(fancy escaping for js needed)                
                loglink="""<span class=\\"log_icon\\"><a href=\\"javascript:map_shrink();showSubcontent(\'/log/minimal/%s\')\\"></a></span>""" % (c.infomarker.id)
                log=q.first()
                p=re.compile("http://twitter.com/derreisende/statuses/(?P<guid>\d{1,})")
                if p.search(log.topic):
                    c.twitter=True
                else:
                    c.twitter=False
            else:
                loglink=''
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.id)
            if q.count() > 0:
                firstimage = q.order_by(asc(model.imageinfo.id)).limit(1)
                for image in firstimage:
                    #creates the infomarker-image_icon-and-ajax-link(fancy escaping for js needed):
                    gallerylink="""<span class=\\"image_icon\\"><a href=\\"javascript:map_shrink();showSubcontent(\'/view/gallery/%s/%s\')\\"></a></span>""" % (c.infomarker.id,image.id)
            else:
                gallerylink=''
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
                maxlat=c.track.maxlat
                maxlon=c.track.maxlon
                minlat=c.track.minlat
                minlon=c.track.minlon
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
                maxlat=''
                maxlon=''
                minlat=''
                minlon=''    
            if c.twitter!=True and c.infomarker.id!=1:
                    c.markerlist=c.markerlist + '''{'lat':%s, 'lon':%s, 'gal':"%s",'log':"%s", 'markerdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s", 'maxlat':"%s", 'maxlon':"%s", 'minlat':"%s",'minlon':"%s"},''' % (c.infomarker.latitude,c.infomarker.longitude,gallerylink,loglink,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor,maxlat,maxlon,minlat,minlon)
                    #c.markerlist=c.markerlist + '''{'lat':%s, 'lon':%s, 'gal':"%s",'log':"%s", 'markerdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s"},''' % (c.infomarker.latitude,c.infomarker.longitude,gallerylink,loglink,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor)
        c.markerlist=(c.markerlist + '''];''').replace('},];','}];')
        return c.markerlist


    def byimg(self,imagename):
        c.markerlist='''['''
        older_createdate='2010-08-31'
        gallerylink=''
        loglink=''
        c.viewall=False
        if imagename==None:
            q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.infomarker==True,model.trackpoint.timestamp>=older_createdate))
            c.viewall=True
        else:
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.imgname.like('%'+imagename+'%'))
            if q.count() > 1:
                c.error='Multiple images found, please elaborate'
                q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.infomarker==True,model.trackpoint.timestamp>=older_createdate))
                c.viewall=True
            elif q.count() < 1:
                c.error='No images found'
                q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.infomarker==True,model.trackpoint.timestamp>=older_createdate))
                c.viewall=True
            else:
                image=q.one()
                q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==image.trackpoint_id)
                c.infomarkers=q.all()
        c.infomarkers = q.order_by(asc(model.trackpoint.timestamp)).all()
        for c.infomarker in c.infomarkers:
            if c.viewall==True:
                q = model.Session.query(model.track).filter(and_(model.track.id==c.infomarker.track_id,model.track.color=='FF0000'))
            else:
                q = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
            if q.count() == 1:
                c.track = q.one()
                total_mins = c.track.timespan.seconds / 60
                mins = total_mins % 60
                hours = total_mins / 60
                timespan = '<b>duration:</b> %sh%smin<br />' % (str(hours),str(mins))
                rounded_distance='<b>distance:</b> %skm<br />' % (str(c.track.distance.quantize(Decimal("0.01"), ROUND_HALF_UP)))
                date=c.track.date.strftime('%d. %B %Y')
                trackpts=c.track.gencpoly_pts
                tracklevels=c.track.gencpoly_levels
                trackcolor=c.track.color
                c.temperature=c.infomarker.temperature
                c.altitude=c.infomarker.altitude
                c.date=date
                maxlat=c.track.maxlat
                maxlon=c.track.maxlon
                minlat=c.track.minlat
                minlon=c.track.minlon
            else:
                q = model.Session.query(model.timezone).filter(model.timezone.id==c.infomarker.timezone_id)
                c.timezone = q.one()
                localtime=c.infomarker.timestamp+c.timezone.utcoffset
                date=localtime.strftime('%d. %B %Y')
                rounded_distance=''
                c.temperature=c.infomarker.temperature
                c.altitude=c.infomarker.altitude
                c.date=date
                timespan=''
                trackpts=''
                tracklevels=''
                trackcolor=''
                maxlat=''
                maxlon=''
                minlat=''
                minlon=''
            c.markerlist=c.markerlist + '''{'lat':%s, 'lon':%s, 'gal':"%s",'log':"%s", 'markerdate':"%s", 'distance':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s", 'maxlat':"%s", 'maxlon':"%s", 'minlat':"%s",'minlon':"%s"},''' % (c.infomarker.latitude,c.infomarker.longitude,gallerylink,loglink,date,rounded_distance,timespan,trackpts,tracklevels,trackcolor,maxlat,maxlon,minlat,minlon)
        c.markerlist=(c.markerlist + '''];''').replace('},];','}];')
        return render("/track/byimg.html")


        #else:
        #    q = model.Session.query(model.imageinfo).filter(model.imageinfo.imgname.like('%'+imagename+'%'))
        #    if q.count() > 1:
        #        return 'Multiple images found, please elaborate'
        #    elif q.count() < 1:
        #        return 'No images found'
        #    image=q.one()
        #    q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==image.infomarker_id)
        #    c.trackpoint = q.one()
        #    q = model.Session.query(model.track).filter(model.track.id==c.trackpoint.track_id)
        #if q.count() == 1:
        #    c.track = q.one()
        #    total_mins = c.track.timespan.seconds / 60
        #    mins = total_mins % 60
        #    hours = total_mins / 60
        #    timespan = '<b>duration:</b> %sh%smin<br />' % (str(hours),str(mins))
        #    location = c.trackpoint.location
        #    date=c.track.date.strftime('%B %d, %Y')
        #    trackpts=c.track.gencpoly_pts
        #    tracklevels=c.track.gencpoly_levels
        #    trackcolor=c.track.color
        #else:
        #    #WTF is happening here?
        #    q = model.Session.query(model.timezone).filter(model.timezone.id==c.trackpoint.timezone_id)
        #    c.timezone = q.one()
        #    localtime=c.trackpoint.timestamp+c.timezone.utcoffset
        #    location=c.trackpoint.location
        #    timespan=''
        #    date=localtime.strftime('%B %d, %Y')
        #    trackpts=''
        #    tracklevels=''
        #    trackcolor=''
        #if c.trackpoint.altitude==None:
        #    altitude=""
        #else:
        #    altitude=c.trackpoint.altitude
        #if image.id!=None:
        #    q = model.Session.query(model.imageinfo).filter(model.imageinfo.id==image.id)
        #    c.imageinfo=q.one()
        #    flickrthumb='http://farm%s.static.flickr.com/%s/%s_%s_t.jpg' % (c.imageinfo.flickrfarm,c.imageinfo.flickrserver,c.imageinfo.flickrphotoid,c.imageinfo.flickrsecret)
        #else:
        #    flickrthumb=""
        #c.markerlist='''[{'lat':%s, 'lon':%s, 'altitude':"%s", 'markerdate':"%s", 'location':"%s", 'timespan':"%s", 'encpts':"%s", 'enclvl':"%s", 'color':"%s", 'flickrthumb':"%s"}];''' % (c.trackpoint.latitude,c.trackpoint.longitude,altitude,date,location,timespan,trackpts,tracklevels,trackcolor,flickrthumb)
        #return render("/track/minimal_map.html")


