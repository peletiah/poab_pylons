import logging


from poab.lib.base import *
from sqlalchemy import asc, desc, and_, or_

import time, datetime
from decimal import Decimal, ROUND_HALF_UP

log = logging.getLogger(__name__)

class LogController(BaseController):

    def index(self):
        q = model.Session.query(model.log)
        logs = q.all()
        #provides menu-template with a comma-separated string(c.countries) of all countries
        countrylist=list()
        for log in logs:
            q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==log.infomarker_id)
            infomarkers=q.all()
            for infomarker in infomarkers:
                q = model.Session.query(model.country).filter(model.country.iso_numcode==infomarker.country_id)
                country=q.one()
                if country.iso_countryname in countrylist:
                    pass
                else:
                    countrylist.append(country.iso_countryname)
        c.countries=''
        for element in countrylist:
            c.countries=c.countries+','+str(element)
        #from here we really start fetching the content for the log-view
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
                c.logs = q.order_by(desc(model.log.createdate)).limit(5)
                c.error = 'no results for selected date(s)!'
        except KeyError:
            try:
                #selection by country
                country=request.params['viewbycountry']
                q = model.Session.query(model.country).filter(model.country.iso_countryname==country)
                try:
                    countrydetails = q.one()
                    q = model.Session.query(model.trackpoint).filter(and_(model.trackpoint.country_id==countrydetails.iso_numcode,model.trackpoint.infomarker==True))
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
                        q = model.Session.query(model.log)
                        c.logs = q.order_by(desc(model.log.createdate)).limit(5)
                        c.error = 'no results for selected country!'
                except:
                    #nothing found for the specified country
                    q = model.Session.query(model.log)
                    c.logs = q.order_by(desc(model.log.createdate)).limit(5)
                    c.error = 'Country not found!'
            except KeyError:
                #select of all entries
                q = model.Session.query(model.log)
                c.logs = q.order_by(desc(model.log.createdate)).limit(5)
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
                    #inlineimage='<div id=\'log_inlineimage\'><a href="http://benko.login.cxi:8080/flickr/%s/%s/%s/%s/_b" title="%s" rel="image_colorbox"><img src="http://benko.login.cx:8080/flickr/%s/%s/%s/%s/"></a></div>' % (image.flickrfarm,image.flickrserver,image.flickrphotoid,image.flickrsecret,image.flickrtitle,image.flickrfarm,image.flickrserver,image.flickrphotoid,image.flickrsecret)
                    inlineimage='<div id=\'log_inlineimage\'><a href="http://farm%s.static.flickr.com/%s/%s_%s_b.jpg" title="%s" rel="image_colorbox"><img src="http://farm%s.static.flickr.com/%s/%s_%s.jpg"></a></div>' % (image.flickrfarm,image.flickrserver,image.flickrphotoid,image.flickrsecret,image.flickrtitle,image.flickrfarm,image.flickrserver,image.flickrphotoid,image.flickrsecret)
                else:
                    inlineimage='<div id=\'log_inlineimage\'><a href="http://farm%s.static.flickr.com/%s/%s_%s_b.jpg" title="%s" rel="image_colorbox"><img src="http://farm%s.static.flickr.com/%s/%s_%s.jpg"></a><br>%s</div>' % (image.flickrfarm,image.flickrserver,image.flickrphotoid,image.flickrsecret,image.flickrtitle,image.flickrfarm,image.flickrserver,image.flickrphotoid,image.flickrsecret,image.flickrdescription)
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
                location=c.infomarker.location
                infomarkerid=c.infomarker.id
            c.logdetails.append(logdetails)
        return render("/log/index.html")


