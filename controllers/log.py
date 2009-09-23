import logging


from poab.lib.base import *
from sqlalchemy import asc, desc, and_, or_

import time, datetime
from decimal import Decimal, ROUND_HALF_UP

log = logging.getLogger(__name__)

class LogController(BaseController):

    def index(self):
        try:
            #selection by date-range
            daterange=request.params['viewbydate']
            lastdate=daterange.split()[2]
            time_format = "%Y-%m-%d"
            lastdate = time.strptime(lastdate,time_format)
            lastdate=datetime.datetime(*lastdate[:6])
            delta = datetime.timedelta(days=1)
            q = model.Session.query(model.log).filter(and_(model.log.createdate > daterange.split()[0],model.log.createdate <= lastdate+delta))
            c.logs = q.order_by(desc(model.log.createdate)).all()
            if c.logs:
                pass
            else:
                #nothing found in the specified date-range
                q = model.Session.query(model.log)
                c.logs = q.order_by(desc(model.log.createdate)).all()
                c.error = 'no results for selected date(s)!'
        except KeyError:
            #select of all entries
                q = model.Session.query(model.log)
                c.logs = q.order_by(desc(model.log.createdate)).all()
        c.logdetails=list()        
        for c.log in c.logs:
            # ###query for infomarker
            q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==c.log.infomarker_id)
            c.infomarker=q.one()
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
            c.timezone = q.one()
            localtime=c.log.createdate+c.timezone.utcoffset
            # ###query for country and continent
            q = model.Session.query(model.country).filter(model.country.iso_numcode==c.infomarker.country_id)
            c.country=q.one()
            q = model.Session.query(model.continent).filter(model.continent.id==c.country.continent_id)
            c.continent=q.one()
            # ###query for related images and convert 'imgid'-tags to embedded images
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.log_id==c.log.id)
            c.images = q.all()
            for image in c.images:
                if image.flickrdescription==None:
                    inlineimage='<div id=\'log_inlineimage\'><a rel="lightbox-MyGroup" href="http://benko.login.cx:8080/flickr/%s/%s/%s/%s/_b" title="%s"><img src="http://benko.login.cx:8080/flickr/%s/%s/%s/%s/"></a></div>' % (image.flickrfarm,image.flickrserver,image.flickrphotoid,image.flickrsecret,image.flickrtitle,image.flickrfarm,image.flickrserver,image.flickrphotoid,image.flickrsecret)
                else:
                    inlineimage='<div id=\'log_inlineimage\'><a rel="lightbox-MyGroup" href="http://benko.login.cx:8080/flickr/%s/%s/%s/%s/_b" title="%s"><img src="http://benko.login.cx:8080/flickr/%s/%s/%s/%s/"></a><br>%s</div>' % (image.flickrfarm,image.flickrserver,image.flickrphotoid,image.flickrsecret,image.flickrtitle,image.flickrfarm,image.flickrserver,image.flickrphotoid,image.flickrsecret,image.flickrdescription)
                c.log.content=c.log.content.replace('[imgid'+str(image.id)+']',inlineimage)
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
                infomarkerid=c.infomarker.id
            c.logdetails.append(logdetails)
        return render("/log/index.html")
