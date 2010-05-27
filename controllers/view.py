import logging

from poab.lib.base import *
import poab.lib.timediff as timediff

from sqlalchemy import asc, desc, and_, or_
import time,datetime

log = logging.getLogger(__name__)

class ViewController(BaseController):

    def index(self,startfromimage):
        #preparing the pagecontrol
        q = model.Session.query(model.imageinfo).filter(and_(model.imageinfo.online==True,model.imageinfo.online==True))
        c.lowestimageid = q.order_by(asc(model.imageinfo.id)).first().id
        #find highestimageid
        c.highestimageid = q.order_by(desc(model.imageinfo.id)).first().id
        #images starting from startfromimage(show 5 newest images if startfromimage=0)
        if int(startfromimage) == 0:
            c.images = q.order_by(desc(model.imageinfo.id)).limit(10)
            imagesplusone = q.order_by(desc(model.imageinfo.id)).limit(11)
            c.startfromimage = int(c.highestimageid)
        else:
            q = model.Session.query(model.imageinfo).filter(and_(model.imageinfo.id <= startfromimage,model.imageinfo.online==True,model.imageinfo.online==True))
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
            q = model.Session.query(model.imageinfo).filter(and_(model.imageinfo.id > startfromimage,model.imageinfo.online==True))
            imagesnextpage = q.order_by(asc(model.imageinfo.id)).limit(10)
            for image in imagesnextpage:
                c.startimagenextpage = image.id
        else:
            c.startimagenextpage = c.highestimageid

        c.viewlist=list()
        for image in c.images:
            #get info from related logentry
            #q = model.Session.query(model.log).filter(model.log.id==image.log_id)
            #c.loginfo=q.one()
            #get info from related trackpoint or infomarker
            if image.trackpoint_id:
                trackpoint_id=image.trackpoint_id
            else:
                trackpoint_id=image.infomarker_id
                c.prefix='near '
            q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==trackpoint_id)
            c.trackpointinfo=q.one()
            #get timezone
            q = model.Session.query(model.timezone).filter(model.timezone.id==c.trackpointinfo.timezone_id)
            c.timezone = q.one()
            c.localtime=image.flickrdatetaken+c.timezone.utcoffset
            deltaseconds=round(c.timezone.utcoffset.days*86400+c.timezone.utcoffset.seconds)
            class viewdetail:
                photoid=image.id
                flickrfarm=image.flickrfarm
                flickrserver=image.flickrserver
                flickrphotoid=image.flickrphotoid
                flickrsecret=image.flickrsecret
                title=image.flickrtitle
                description=image.flickrdescription
                log_id=image.log_id
                imgname=image.imgname
                aperture=image.aperture
                shutter=image.shutter
                focal_length=image.focal_length
                iso=image.iso
                #logdate=c.loginfo.createdate.strftime('%Y-%m-%d') #needed for the imagepath
                trackpointinfo=c.trackpointinfo
                localtime=c.localtime.strftime('%Y-%m-%d %H:%M:%S')
                timezone=c.timezone
                #calculate the offset in seconds
                utcoffset=timediff.timediff(deltaseconds)
            c.viewlist.append(viewdetail)
        return render("/view/index.html")


    def infomarker(self,infomarker,startfromimage):
        #preparing the pagecontrol
        q = model.Session.query(model.imageinfo).filter(and_(model.imageinfo.infomarker_id==infomarker,model.imageinfo.online==True))
        c.lowestimageid = q.order_by(asc(model.imageinfo.id)).first().id
        #find highestimageid
        c.highestimageid = q.order_by(desc(model.imageinfo.id)).first().id
        #images starting from startfromimage(show 5 newest images if startfromimage=0)
        if int(startfromimage) == 0:
            c.images = q.order_by(desc(model.imageinfo.id)).limit(10)
            imagesplusone = q.order_by(desc(model.imageinfo.id)).limit(11)
            c.startfromimage = int(c.highestimageid)
        else:
            q = model.Session.query(model.imageinfo).filter(and_(model.imageinfo.id <= startfromimage,model.imageinfo.infomarker_id==infomarker,model.imageinfo.online==True))
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
            q = model.Session.query(model.imageinfo).filter(and_(model.imageinfo.id > startfromimage,model.imageinfo.infomarker_id==infomarker,model.imageinfo.online==True))
            imagesnextpage = q.order_by(asc(model.imageinfo.id)).limit(10)
            for image in imagesnextpage:
                c.startimagenextpage = image.id
        else:
            c.startimagenextpage = c.highestimageid

        c.viewlist=list()
        c.infomarker_id=infomarker
        for image in c.images:
            #get info from related logentry
            #q = model.Session.query(model.log).filter(model.log.id==image.log_id)
            #c.loginfo=q.one()
            #get info from related trackpoint or infomarker
            if image.trackpoint_id:
                trackpoint_id=image.trackpoint_id
            else:
                trackpoint_id=image.infomarker_id
                c.prefix='near '
            q = model.Session.query(model.trackpoint).filter(model.trackpoint.id==trackpoint_id)
            c.trackpointinfo=q.one()
            #get timezone
            q = model.Session.query(model.timezone).filter(model.timezone.id==c.trackpointinfo.timezone_id)
            c.timezone = q.one()
            c.localtime=image.flickrdatetaken+c.timezone.utcoffset
            deltaseconds=round(c.timezone.utcoffset.days*86400+c.timezone.utcoffset.seconds)
            class viewdetail:
                photoid=image.id
                flickrfarm=image.flickrfarm
                flickrserver=image.flickrserver
                flickrphotoid=image.flickrphotoid
                flickrsecret=image.flickrsecret
                title=image.flickrtitle
                description=image.flickrdescription
                imgname=image.imgname
                aperture=image.aperture
                shutter=image.shutter
                focal_length=image.focal_length
                iso=image.iso
                log_id=image.log_id
                #logdate=c.loginfo.createdate.strftime('%Y-%m-%d') #needed for the imagepath
                trackpointinfo=c.trackpointinfo
                localtime=c.localtime.strftime('%Y-%m-%d %H:%M:%S')
                timezone=c.timezone
                #calculate the offset in seconds
                utcoffset=timediff.timediff(deltaseconds)
            c.viewlist.append(viewdetail)
        return render("/view/infomarker.html")


    def gallery(self,infomarker,startfromimg):
            #first imageid
            q = model.Session.query(model.imageinfo).filter(and_(model.imageinfo.infomarker_id==infomarker,model.imageinfo.online==True))
            firstimage = q.order_by(asc(model.imageinfo.id)).limit(1)
            for image in firstimage:
                c.firstimageid=image.id
            #last imageid
            lastimage = q.order_by(desc(model.imageinfo.id)).limit(1)
            for image in lastimage:
                c.lastimageid=image.id
            #imagedetails for the current page
            q = model.Session.query(model.imageinfo).filter(and_(model.imageinfo.infomarker_id==infomarker,model.imageinfo.id >= startfromimg,model.imageinfo.online==True))
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
            q = model.Session.query(model.imageinfo).filter(and_(model.imageinfo.infomarker_id==infomarker,model.imageinfo.id < c.startfromimg,model.imageinfo.online==True))
            if c.imagecount==24:
                imagesprevpage = q.order_by(desc(model.imageinfo.id)).limit(48)
            else:
                #there are less than 24 images on the page, so imagesprevpage is not 2x24 pictures away
                imagesprevpage = q.order_by(desc(model.imageinfo.id)).limit(23+c.imagecount)
            for image in imagesprevpage:
                    c.prevstartfromimg=image.id
            return render("/view/gallery.html")

