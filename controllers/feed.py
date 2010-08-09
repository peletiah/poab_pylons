import logging

from poab.lib.base import *

from poab.lib.base import *
from sqlalchemy import asc, desc, and_, or_

import time, datetime
import re
from decimal import Decimal, ROUND_HALF_UP

log = logging.getLogger(__name__)

class FeedController(BaseController):

    def index(self):
        q = model.Session.query(model.log)
        logs = q.order_by(desc(model.log.createdate)).all()
        c.logdetails=list()
        for c.log in logs:
            # ###query for infomarker
            q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==c.log.infomarker_id)
            c.infomarker=q.one()
            # ###query for last trackpoint
            q = model.Session.query(model.trackpoint).filter(model.trackpoint.track_id==c.infomarker.track_id).order_by(asc(model.trackpoint.timestamp))
            c.lasttrkpt=q.first()
            # ###query for startfromimg
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.infomarker_id==c.infomarker.id)
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
                    inlineimage='''<br /><div><a href="%s" title="%s"><img src="http://farm%s.static.flickr.com/%s/%s_%s.jpg" alt="%s" /></a><br /><br />
    </div>''' % (imageinfo.imgname,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrtitle)
                else:
                    inlineimage='''<div><div><a href="%s" title="%s"><img src="http://farm%s.static.flickr.com/%s/%s_%s.jpg" alt="%s" /></a>
    </div><span>%s</span><br /><br /></div>''' % (imageinfo.imgname,imageinfo.flickrtitle,imageinfo.flickrfarm,imageinfo.flickrserver,imageinfo.flickrphotoid,imageinfo.flickrsecret,imageinfo.flickrtitle,imageinfo.flickrdescription)
                c.log.content=c.log.content.replace(imgidtag,inlineimage)
            # ###create logdetails-class
            class logdetails:
                topic=c.log.topic
                createdate=localtime.strftime('%Y-%m-%dT%H:%M:%SZ%Z')
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
                gallerylink=c.gallerylink
            c.logdetails.append(logdetails)
        return render("/feed/index.html")
