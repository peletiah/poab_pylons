import logging


from poab.lib.base import *
from sqlalchemy import asc, desc, and_, or_

import time, datetime
import re
from decimal import Decimal, ROUND_HALF_UP

log = logging.getLogger(__name__)

class LogController(BaseController):

    def index(self):
        redirect_to(action='c')
        c.country_id=0
        q = model.Session.query(model.log)
        log_count = q.count()
        c.navstring=h.countryDetails(model,c.country_id)
        page_fract=float(h.Fraction(str(log_count)+'/3'))
        if int(str(page_fract).split('.')[1])==0:
            #if we have a "full" page(3 log entries), 
            #the "current" page is "full-page"-fraction minus 1
            c.page=int(str(page_fract).split('.')[0])-1
        else:
            c.page=str(page_fract).split('.')[0]
        c.navstring='''<li id="navigation"><a href="#" title="Show all entries" onclick="resetContent();">All</a></li>'''
        return render("/log/index.html")

    def c(self,id1,page):
        older_createdate='2008-02-01'
        c.country_id=int(id1)
        if c.country_id==0 and page==None:
            q = model.Session.query(model.log).filter(model.log.createdate>older_createdate)
            log_count = q.count()
            page_fract=float(h.Fraction(str(log_count)+'/3'))
            if int(str(page_fract).split('.')[1])==0:
                c.page=int(str(page_fract).split('.')[0])-1
            else:               
                c.page=str(page_fract).split('.')[0]
        elif page==None:
            c.page=0
        else:
            c.page=page
        c.navstring=h.countryDetails(model,c.country_id)
        c.curr_page=int(c.page)
        c.navstring=h.countryDetails(model,c.country_id)
        if c.country_id==0:
            q = model.Session.query(model.trackpoint).filter(model.trackpoint.infomarker==True)
        else:
            q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.country_id==c.country_id,model.trackpoint.infomarker==True))
        trackpoints = q.all()
        trkpt_list=list()
        for trackpoint in trackpoints:
            trkpt_list.append(trackpoint.id)
        q = model.Session.query(model.log).filter(and_(model.log.infomarker_id.in_(trkpt_list),model.log.createdate>older_createdate))
        logs = q.order_by(asc(model.log.createdate)).all()
        c.page=list()
        c.pages=list()
        i=0
        for log in logs:
            c.page.append(log)
            i=i+1
            if i==3:
                c.page.reverse()
                c.pages.append(c.page)
                c.page=list()
                i=0
        if i<3 and i>0:
            c.page.reverse()
            c.pages.append(c.page)
        #c.pages.reverse()
        c.logdetails=list()       
        for c.log in c.pages[c.curr_page]:
            c.twitter=False
            c.guid=None
            # ###query for infomarker
            q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==c.log.infomarker_id)
            c.infomarker=q.one()
            # ###query for last trackpoint
            q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.track_id==c.infomarker.track_id,model.trackpoint.id==c.infomarker.id)).order_by(asc(model.trackpoint.timestamp))
            c.lasttrkpt=q.first()
            # ###query if images exist for the log
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.id)
            if q.count() > 0:
                #creates the infomarker-image_icon-and-ajax-link(fancy escaping for js needed):
                c.gallerylink="""<span class="image_icon"><a title="Show large images related to this entry" href="/view/infomarker/%s/0"></a></span>""" % (c.infomarker.id)
            else:
                c.gallerylink=''
            # ###query for track
            q = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
            if q.count() == 1:
                c.track=q.one()
                # ###calculate duration from track-info
                total_mins = c.track.timespan.seconds / 60
                mins = total_mins % 60
                hours = total_mins / 60
                c.timespan = str(hours)+'h '+str(mins)+'min'
                rounded_distance=str(c.track.distance.quantize(Decimal("0.01"), ROUND_HALF_UP))+'km'
            else:
                rounded_distance=None
                c.timespan=None
            # ###query for timezone and calculate localtime
            q = model.Session.query(model.timezone).filter(model.timezone.id==c.infomarker.timezone_id)
            try:
                c.timezone = q.one()
                localtime=c.log.createdate+c.timezone.utcoffset
            except:
                localtime=c.log.createdate
            # ###query for country and continent
            q = model.Session.query(model.country).filter(model.country.iso_numcode==c.infomarker.country_id)
            c.country=q.one()
            q = model.Session.query(model.continent).filter(model.continent.id==c.country.continent_id)
            c.continent=q.one()
            # ###set flag for irregular posts(like tweets)
            p=re.compile("http://twitter.com/derreisende/statuses/(?P<guid>\d{1,})")
            if p.search(c.log.topic):
                c.guid=p.search(c.log.topic).group("guid")
                c.twitter=True
            # ###convert 'imgid'-tags to embedded images
            imgidtags=re.findall('\[imgid[0-9]*\]',c.log.content)
            for imgidtag in imgidtags:
                imageinfo_id=imgidtag[6:-1]
                q = model.Session.query(model.imageinfo).filter(model.imageinfo.id==imageinfo_id)
                imageinfo = q.one()
                if imageinfo.flickrdescription==None:
                    inlineimage='''<div class="log_inlineimage"> <div class="imagecontainer"><a href="%s" title="%s" rel="image_colorbox"><img class="inlineimage" src="http://farm%s.static.flickr.com/%s/%s_%s.jpg" alt="%s" /></a><div class="caption">
        <span>&#8594;</span>
            <a href="http://www.flickr.com/peletiah/%s" target="_blank">www.flickr.com</a>
    </div></div></div>''' % (imageinfo.imgname,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrtitle,imageinfo.flickrphotoid)
                else:
                    inlineimage='''<div class="log_inlineimage"><div class="imagecontainer"><a href="%s" title="%s" rel="image_colorbox" ><img class="inlineimage" src="http://farm%s.static.flickr.com/%s/%s_%s.jpg" alt="%s" /></a><div class="caption">
        <span>&#8594;</span>
            <a href="http://www.flickr.com/peletiah/%s" target="_blank">www.flickr.com</a>
    </div></div><span class="imagedescription">%s</span></div>''' % (imageinfo.imgname,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrtitle,imageinfo.flickrphotoid,imageinfo.flickrdescription)
                c.log.content=c.log.content.replace(imgidtag,inlineimage)
            # ###create logdetails-class
            class logdetails:
                topic=c.log.topic
                twitter=c.twitter
                guid=c.guid
                createdate=localtime.strftime('%B %d, %Y')
                content=c.log.content
                try:
                    distance=rounded_distance
                except NameError:
                    distance='-'
                timezoneabbriv=c.timezone.abbreviation
                if c.timespan:
                    timespan=c.timespan
                else:
                    timespan=None
                country=c.country.iso_countryname
                continent=c.continent.name
                location=c.lasttrkpt.location
                infomarkerid=c.infomarker.id
                id=c.log.id
                gallerylink=c.gallerylink
            c.logdetails.append(logdetails)
        return render("/log/index.html")

    def id(self,log_id):
        c.logdetails=list()
        q = model.Session.query(model.log).filter(model.log.id==int(log_id))
        c.curr_page=0
        logs = q.order_by(asc(model.log.createdate)).all()
        c.page=list()
        c.pages=list()
        i=0
        c.twitter=False
        c.guid=None
        for log in logs:
            c.page.append(log)
            i=i+1
            if i==3:
                c.page.reverse()
                c.pages.append(c.page)
                c.page=list()
                i=0
        if i<3 and i>0:
            c.page.reverse()
            c.pages.append(c.page)
        c.log=q.one()
        c.logdetails=list()       
        # ###query for infomarker
        q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==c.log.infomarker_id)
        c.infomarker=q.one()
        # ###query for infomarker
        q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==c.log.infomarker_id)
        c.infomarker=q.one()
        # ###query for last trackpoint
        q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.track_id==c.infomarker.track_id,model.trackpoint.id==c.infomarker.id)).order_by(asc(model.trackpoint.timestamp))
        c.lasttrkpt=q.first()
        # ###query for startfromimg
        q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.id)
        if q.count() > 0:
            #creates the infomarker-image_icon-and-ajax-link(fancy escaping for js needed):
            c.gallerylink="""<span class="image_icon"><a title="Show large images of this day" href="/view/infomarker/%s/0"></a></span>""" % (c.infomarker.id)
        else:
            c.gallerylink=''
        # ###query for track
        q = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
        if q.count() == 1:
            c.track=q.one()
            # ###calculate duration from track-info
            total_mins = c.track.timespan.seconds / 60
            mins = total_mins % 60
            hours = total_mins / 60
            c.timespan = str(hours)+'h '+str(mins)+'min'
            rounded_distance=str(c.track.distance.quantize(Decimal("0.01"), ROUND_HALF_UP))+'km'
        else:
            rounded_distance=None
            c.timespan=None
        # ###query for timezone and calculate localtime
        q = model.Session.query(model.timezone).filter(model.timezone.id==c.infomarker.timezone_id)
        try:
            c.timezone = q.one()
            localtime=c.log.createdate+c.timezone.utcoffset
        except:
            localtime=c.log.createdate
        # ###query for country and continent
        q = model.Session.query(model.country).filter(model.country.iso_numcode==c.infomarker.country_id)
        c.country=q.one()
        q = model.Session.query(model.continent).filter(model.continent.id==c.country.continent_id)
        c.continent=q.one()
        # ###set flag for irregular posts(like tweets)
        p=re.compile("http://twitter.com/derreisende/statuses/(?P<guid>\d{1,})")
        if p.search(c.log.topic):
            c.guid=p.search(c.log.topic).group("guid")
            c.twitter=True
        # ###convert 'imgid'-tags to embedded images
        imgidtags=re.findall('\[imgid[0-9]*\]',c.log.content)
        for imgidtag in imgidtags:
            imageinfo_id=imgidtag[6:-1]
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.id==imageinfo_id)
            imageinfo = q.one()
            if imageinfo.flickrdescription==None:
                inlineimage='''<div class="log_inlineimage"> <div class="imagecontainer"><a href="%s" title="%s" rel="image_colorbox"><img class="inlineimage" src="http://farm%s.static.flickr.com/%s/%s_%s.jpg" alt="%s" /></a><div class="caption">
        <span>&#8594;</span>
            <a href="http://www.flickr.com/peletiah/%s" target="_blank">www.flickr.com</a>
    </div></div></div>''' % (imageinfo.imgname,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrtitle,imageinfo.flickrphotoid)
            else:
                inlineimage='''<div class="log_inlineimage"><div class="imagecontainer"><a href="%s" title="%s" rel="image_colorbox" ><img class="inlineimage" src="http://farm%s.static.flickr.com/%s/%s_%s.jpg" alt="%s" /></a><div class="caption">
        <span>&#8594;</span>
            <a href="http://www.flickr.com/peletiah/%s" target="_blank">www.flickr.com</a>
    </div></div><span class="imagedescription">%s</span></div>''' % (imageinfo.imgname,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrtitle,imageinfo.flickrphotoid,imageinfo.flickrdescription)
            c.log.content=c.log.content.replace(imgidtag,inlineimage)
        # ###create logdetails-class
        class logdetails:
            topic=c.log.topic
            createdate=localtime.strftime('%B %d, %Y')
            content=c.log.content
            twitter=c.twitter
            guid=c.guid
            try:
                distance=rounded_distance
            except NameError:
                distance='-'
            timezoneabbriv=c.timezone.abbreviation
            if c.timespan:
                timespan=c.timespan
            else:
                timespan=None
            country=c.country.iso_countryname
            continent=c.continent.name
            location=c.lasttrkpt.location
            infomarkerid=c.infomarker.id
            gallerylink=c.gallerylink
            id=c.log.id
        c.logdetails.append(logdetails)
        c.navstring='''<li class="navigation"><ul><li class="navli"><a href="#" title="Journal-entries for all countries" onclick="resetContent\(\);">All</a>&#8594; Id &#8594;<a href="/log/id/%s" title="Content for log-id %s">%s</a></li></ul></li>''' % (c.log.id,c.log.id,c.log.id)
        return render("/log/infomarker.html")

    def minimal(self,id):
        q = model.Session.query(model.log).filter(model.log.infomarker_id==id)
        c.log=q.one() 
        # ###convert 'imgid'-tags to embedded images
        imgidtags=re.findall('\[imgid[0-9]*\]',c.log.content)
        for imgidtag in imgidtags:
            imageinfo_id=imgidtag[6:-1]
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.id==imageinfo_id)
            imageinfo = q.one()
            if imageinfo.flickrdescription==None:
                    inlineimage='''<div class="log_inlineimage"> <div class="imagecontainer"><a href="%s" title="%s" rel="image_colorbox"><img class="inlineimage" src="http://farm%s.static.flickr.com/%s/%s_%s_m.jpg" /></a><div class="caption">
        <span>&#8594;</span>
            <a href="http://www.flickr.com/peletiah/%s" target="_blank">www.flickr.com</a>
    </div></div></div>''' % (imageinfo.imgname,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrphotoid)
            else:
                inlineimage='''<div class="log_inlineimage"><div class="imagecontainer"><a href="%s" title="%s" rel="image_colorbox" ><img class="inlineimage" src="http://farm%s.static.flickr.com/%s/%s_%s_m.jpg" /></a><div class="caption">
        <span>&#8594;</span>
            <a href="http://www.flickr.com/peletiah/%s" target="_blank">www.flickr.com</a>
    </div></div><span class="imagedescription">%s</span></div>''' % (imageinfo.imgname,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrphotoid,imageinfo.flickrdescription)
            c.log.content=c.log.content.replace(imgidtag,inlineimage)
        return render("/log/minimal_log.html")



