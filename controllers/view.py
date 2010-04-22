import logging

from poab.lib.base import *

from sqlalchemy import asc, desc, and_, or_
import time,datetime

log = logging.getLogger(__name__)

class ViewController(BaseController):

    def index(self,startfromimage):
        #preparing the pagecontrol
        q = model.Session.query(model.imageinfo)
        c.lowestimageid = q.order_by(asc(model.imageinfo.id)).first().id
        #find highestimageid
        c.highestimageid = q.order_by(desc(model.imageinfo.id)).first().id
        #images starting from startfromimage(show 5 newest images if startfromimage=0)
        if int(startfromimage) == 0:
            c.images = q.order_by(desc(model.imageinfo.id)).limit(10)
            imagesplusone = q.order_by(desc(model.imageinfo.id)).limit(11)
            c.startfromimage = int(c.highestimageid)
        else:
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.id <= startfromimage)
            c.images = q.order_by(desc(model.imageinfo.id)).limit(10)
            imagesplusone = q.order_by(desc(model.imageinfo.id)).limit(11)
            c.startfromimage = int(startfromimage)
        for image in imagesplusone:
            c.startimageprevpage = image.id
        #lowestimageid on current page
        for image in c.images:
            c.lowestimageonpage = image.id
        #the current page is not full so we need to add 
        #the missing pages to the next page to keep up with the correct pagecount
        imagesonpage=q.limit(10).count()
        if imagesonpage < 10:
            addtonext=imagesonpage
        else:
            addtonext=0
        #startimageid on next page
        if int(startfromimage) < c.highestimageid:
            q = model.Session.query(model.imageinfo).filter(model.imageinfo.id > startfromimage)
            imagesnextpage = q.order_by(asc(model.imageinfo.id)).limit(10)
            for image in imagesnextpage:
                c.startimagenextpage = image.id
        else:
            c.startimagenextpage = c.highestimageid

        c.viewlist=list()
        for image in c.images:
            q = model.Session.query(model.log).filter(model.log.id==image.log_id)
            c.loginfo=q.one()
            class viewdetail:
                flickrfarm=image.flickrfarm
                flickrserver=image.flickrserver
                flickrphotoid=image.flickrphotoid
                flickrsecret=image.flickrsecret
                title=image.flickrtitle
                description=image.flickrdescription
                datetaken=image.flickrdatetaken
                imgname=image.imgname
                logdate=c.loginfo.createdate.strftime('%Y-%m-%d')
            c.viewlist.append(viewdetail)
        return render("/view/index.html")
