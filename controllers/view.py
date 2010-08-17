import logging

from poab.lib.base import *
import poab.lib.timediff as timediff

from sqlalchemy import asc, desc, and_, or_
import time,datetime

log = logging.getLogger(__name__)

class ViewController(BaseController):

    def index(self):
        redirect_to(action='c')
        c.country_id=0
        q = model.Session.query(model.imageinfo)
        image_count=q.count()
        page_fract=float(h.Fraction(str(image_count)+'/10'))
        if int(str(page_fract).split('.')[1])==0:
            #if we have a "full" page(10 image entries), 
            #the "current" page is "full-page"-fraction minus 1
            c.page=int(str(page_fract).split('.')[0])-1
        else:
            c.page=str(page_fract).split('.')[0]
        c.navstring='''<li id="navigation"><a href="#" title="Show all entries" onclick="resetContent();">All</a></li>'''
        return render("/view/index.html")


    def c(self,id1,page):
        c.country_id=int(id1)
        if c.country_id==0 and page==None:
            q = model.Session.query(model.imageinfo)
            image_count=q.count()
            page_fract=float(h.Fraction(str(image_count)+'/10'))
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
        if c.country_id==0:
            q = model.Session.query(model.trackpoint).filter(model.trackpoint.country_id != None)
        else:
            q = model.Session.query(model.trackpoint).filter(model.trackpoint.country_id==c.country_id)
        trackpoints = q.all()
        trkpt_list=list()
        for trackpoint in trackpoints:
            trkpt_list.append(trackpoint.id)
        q = model.Session.query(model.imageinfo).filter(model.imageinfo.trackpoint_id.in_(trkpt_list))
        images= q.order_by(asc(model.imageinfo.flickrdatetaken)).all()
        c.page=list()
        c.pages=list()
        i=0
        for image in images:
            c.page.append(image)
            i=i+1
            if i==10:
                c.page.reverse()
                c.pages.append(c.page)
                c.page=list()
                i=0
        if i<10 and i>0:
            c.page.reverse()
            c.pages.append(c.page)
        c.viewlist=list()
        for image in c.pages[c.curr_page]:
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


    def infomarker(self,id1,page):
        c.infomarker=int(id1)
        c.curr_page=int(page)
    #    c.navstring=h.countryDetails(model,c.country_id)
        q = model.Session.query(model.imageinfo).filter(and_(model.imageinfo.online==True,model.imageinfo.infomarker_id==c.infomarker))
        images=q.order_by(asc(model.imageinfo.flickrdatetaken)).all()

        c.page=list()
        c.pages=list()
        i=0
        for image in images:
            c.page.append(image)
            i=i+1
            if i==10:
                c.page.reverse()
                c.pages.append(c.page)
                c.page=list()
                i=0
        if i<10 and i>0:
            c.page.reverse()
            c.pages.append(c.page)
        c.viewlist=list()
        for image in c.pages[c.curr_page]:
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

    def id(self,id):
        q = model.Session.query(model.imageinfo).filter(and_(model.imageinfo.online==True,model.imageinfo.id==id))
        image=q.one()
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
        c.viewlist=list()
        c.viewlist.append(viewdetail)
        c.navstring='''<li class="navigation"><ul><li class="navli"><a href="#" title="Journal-entries for all countries" onclick="resetContent\(\);">All</a>&#8594; Id &#8594;<a href="/view/id/%s" title="View image %s alone">%s</a></li></ul></li>''' % (id,id,id)
        return render("/view/id.html")
            

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
            #getting the lat-lng position of the infomarker
            return render("/view/gallery.html")

