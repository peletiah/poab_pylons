import logging


from poab.lib.base import *
from sqlalchemy import asc, desc, and_, or_

import time, datetime
import re
from decimal import Decimal, ROUND_HALF_UP

log = logging.getLogger(__name__)

class LogController(BaseController):

    def index(self,startfromlog):
        try:
            #selection by date-range
            daterange=request.params['viewbydate']
            lastdate=daterange.split()[2]
            time_format = "%Y-%m-%d"
            lastdate = time.strptime(lastdate,time_format)
            lastdate=datetime.datetime(*lastdate[:6])
            delta = datetime.timedelta(days=1)
            q = model.Session.query(model.log).filter(and_(model.log.createdate > daterange.split()[0],model.log.createdate <= lastdate+delta,model.log.id >= startfromlog))
            c.logs = q.order_by(desc(model.log.createdate)).all()
            if c.logs:
                pass
            else:
                #nothing found in the specified date-range
                q = model.Session.query(model.log)
                c.logs = q.order_by(desc(model.log.createdate)).limit(5)
                c.error = 'no results for selected date(s)!'
        except KeyError:
            try:
                #selection by country
                country=request.params['viewbycountry']
                q = model.Session.query(model.country).filter(model.country.iso_countryname==country)
                try:
                    countrydetails = q.one()
                    q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.country_id==countrydetails.iso_numcode,model.trackpoint.infomarker==True,model.log.id >= startfromlog))
                    infomarkers = q.all()
                    c.logs=list()
                    for infomarker in infomarkers:
                        q = model.Session.query(model.log).filter(model.log.infomarker_id==infomarker.id)
                        logs = q.all()
                        for log in logs:
                            c.logs.append(log)
                    if c.logs:
                        pass
                    else:
                        #nothing found for the specified country
                        q = model.Session.query(model.log).filter(model.log.id >= startfromlog)
                        c.logs = q.order_by(desc(model.log.createdate)).limit(5)
                        c.error = 'no results for selected country!'
                except:
                    #nothing found for the specified country
                    q = model.Session.query(model.log).filter(model.log.id >= startfromlog)
                    c.logs = q.order_by(desc(model.log.createdate)).limit(5)
                    c.error = 'Country not found!'
            except KeyError:
                #find lowestlogid
                q = model.Session.query(model.log)
                c.lowestlogid = q.order_by(asc(model.log.id)).first().id
                #find highestlogid
                c.highestlogid = q.order_by(desc(model.log.id)).first().id
                #logs starting from startfromlog(show 5 newest logs if startfromlog=0)
                if int(startfromlog) == 0:
                    c.logs = q.order_by(desc(model.log.id)).limit(5)
                    logsplusone = q.order_by(desc(model.log.id)).limit(6)
                    c.startfromlog = int(c.highestlogid)
                else:
                    q = model.Session.query(model.log).filter(model.log.id <= startfromlog)
                    c.logs = q.order_by(desc(model.log.id)).limit(5)
                    logsplusone = q.order_by(desc(model.log.id)).limit(6)
                    c.startfromlog = int(startfromlog)
                for log in logsplusone:
                    c.startlogprevpage = log.id
                #lowestlogid on current page
                for log in c.logs:
                    c.lowestlogonpage = log.id
                #the current page is not full so we need to add the missing pages to the next page to keep up with the correct pagecount
                logsonpage=q.limit(5).count()
                if logsonpage < 5:
                    addtonext=logsonpage
                else:
                    addtonext=0
                #startlogid on next page
                if int(startfromlog) < c.highestlogid:
                    q = model.Session.query(model.log).filter(model.log.id > startfromlog)
                    logsnextpage = q.order_by(asc(model.log.id)).limit(5)
                    for log in logsnextpage:
                        c.startlognextpage = log.id
                else:
                    c.startlognextpage = c.highestlogid
        c.logdetails=list()       
        for c.log in c.logs:
            # ###query for infomarker
            q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==c.log.infomarker_id)
            c.infomarker=q.one()
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
            # ###convert 'imgid'-tags to embedded images
            imgidtags=re.findall('\[imgid[0-9]*\]',c.log.content)
            for imgidtag in imgidtags:
                imageinfo_id=imgidtag[6:-1]
                q = model.Session.query(model.imageinfo).filter(model.imageinfo.id==imageinfo_id)
                imageinfo = q.one()
                if imageinfo.flickrdescription==None:
                    inlineimage='''<div id="log_inlineimage"> <div class="imagecontainer"><a href="%s" title="%s" rel="image_colorbox"><img id="inlineimage" src="http://farm%s.static.flickr.com/%s/%s_%s.jpg"></a><div class="caption">
        <span>&#8594;</span>
            <a href="http://www.flickr.com/peletiah/%s" target="_blank">www.flickr.com</a>
    </div></div></div>''' % (imageinfo.imgname,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrphotoid)
                else:
                    inlineimage='''<div id="log_inlineimage"><div class="imagecontainer"><a href="%s" title="%s" rel="image_colorbox" ><img id="inlineimage" src="http://farm%s.static.flickr.com/%s/%s_%s.jpg"></a><div class="caption">
        <span>&#8594;</span>
            <a href="http://www.flickr.com/peletiah/%s" target="_blank">www.flickr.com</a>
    </div></div><span class="imagedescription">%s</span></div>''' % (imageinfo.imgname,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrphotoid,imageinfo.flickrdescription)
                c.log.content=c.log.content.replace(imgidtag,inlineimage)
            # ###create logdetails-class
            class logdetails:
                topic=c.log.topic
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
                location=c.infomarker.location
                infomarkerid=c.infomarker.id
                gallerylink=c.gallerylink
            c.logdetails.append(logdetails)
        return render("/log/index.html")


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
                    inlineimage='''<div id="log_inlineimage"> <div class="imagecontainer"><a href="%s" title="%s" rel="image_colorbox"><img id="inlineimage" src="http://farm%s.static.flickr.com/%s/%s_%s_m.jpg"></a><div class="caption">
        <span>&#8594;</span>
            <a href="http://www.flickr.com/peletiah/%s" target="_blank">www.flickr.com</a>
    </div></div></div>''' % (imageinfo.imgname,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrphotoid)
            else:
                inlineimage='''<div id="log_inlineimage"><div class="imagecontainer"><a href="%s" title="%s" rel="image_colorbox" ><img id="inlineimage" src="http://farm%s.static.flickr.com/%s/%s_%s_m.jpg"></a><div class="caption">
        <span>&#8594;</span>
            <a href="http://www.flickr.com/peletiah/%s" target="_blank">www.flickr.com</a>
    </div></div><span class="imagedescription">%s</span></div>''' % (imageinfo.imgname,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrphotoid,imageinfo.flickrdescription)
#            if imageinfo.flickrdescription==None:
#                inlineimage='''<div id="log_inlineimage"> <div class="imagecontainer"><a href="http://farm%s.static.flickr.com/%s/%s_%s_b.jpg" title="%s" rel="image_colorbox"><img id="inlineimage" src="http://farm%s.static.flickr.com/%s/%s_%s_m.jpg"></a><div class="caption">
#        <span>&#8594;</span>
#            <a href="http://www.flickr.com/peletiah/%s" target="_blank">www.flickr.com</a>
#    </div></div></div>''' % (imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrphotoid)
#            else:
#                inlineimage='''<div id="log_inlineimage"><div class="imagecontainer"><a href="http://farm%s.static.flickr.com/%s/%s_%s_b.jpg" title="%s" rel="image_colorbox" ><img id="inlineimage" src="http://farm%s.static.flickr.com/%s/%s_%s_m.jpg"></a><div class="caption">
#        <span>&#8594;</span>
#            <a href="http://www.flickr.com/peletiah/%s" target="_blank">www.flickr.com</a>
#    </div></div><span class="imagedescription">%s</span></div>''' % (imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrphotoid,imageinfo.flickrdescription)
            c.log.content=c.log.content.replace(imgidtag,inlineimage)
        return render("/log/minimal_log.html")
