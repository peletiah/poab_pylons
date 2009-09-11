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
            q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==c.log.infomarker_id)
            c.infomarker=q.one()
            q = model.Session.query(model.track).filter(model.track.id==c.infomarker.track_id)
            c.track=q.one()
            total_mins = c.track.timespan.seconds / 60
            mins = total_mins % 60
            hours = total_mins / 60
            c.timespan = str(hours)+'h '+str(mins)+'min'
            q = model.Session.query(model.timezone).filter(model.timezone.id==c.infomarker.timezone_id)
            c.timezone = q.one()
            localtime=c.log.createdate+c.timezone.utcoffset
            q = model.Session.query(model.country).filter(model.country.iso_numcode==c.infomarker.country_id)
            c.country=q.one()
            q = model.Session.query(model.continent).filter(model.continent.id==c.country.continent_id)
            c.continent=q.one()
            class logdetails:
                topic=c.log.topic
                createdate=localtime.strftime('%d-%m-%Y %H:%M:%S')
                content=c.log.content
                distance=c.track.distance.quantize(Decimal("0.01"), ROUND_HALF_UP)
                timezoneabbriv=c.timezone.abbreviation
                timespan=c.timespan
                country=c.country.iso_countryname
                continent=c.continent.name
            c.logdetails.append(logdetails)
        return render("/log/index2.html")
