import logging

from poab.lib.base import *

from sqlalchemy import asc, desc, and_, or_

log = logging.getLogger(__name__)

class ViewController(BaseController):

    def index(self):
        q = model.Session.query(model.imageinfo).filter(model.imageinfo.log_id!=None)
        images=q.order_by(desc(model.imageinfo.flickrdatetaken)).limit(10)
        c.imagelist=list()
        for image in images:
            c.imagelist.append(image)
        return render("/view/index.html")
