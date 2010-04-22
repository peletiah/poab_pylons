import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import types
from sqlalchemy import ForeignKey
import datetime


def now():
    return datetime.datetime.now()

def init_model(bind):
    """Call me at the beginning of the application.
       'bind' is a SQLAlchemy engine or connection, as returned by
       sa.create_engine, sa.engine_from_config, or engine.connect().
    """
    global engine, Session
    engine = bind
    Session = orm.scoped_session(
        orm.sessionmaker(transactional=True, autoflush=True, bind=bind))
    orm.mapper(log, log_table,
        order_by=[log_table.c.id.desc()])

    orm.mapper(country, country_table,
        order_by=[country_table.c.iso_numcode.desc()])
    
    orm.mapper(continent, continent_table,
        order_by=[continent_table.c.id.desc()])
    
    orm.mapper(comments, comment_table,
        order_by=[comment_table.c.id.desc()])
    
    orm.mapper(imageinfo, imageinfo_table,
        order_by=[imageinfo_table.c.id.desc()])
    
    orm.mapper(photosets, photoset_table,
        order_by=[photoset_table.c.id.desc()])
    
    orm.mapper(track, track_table,
        order_by=[track_table.c.id.desc()])

    orm.mapper(trackpoint, trackpoint_table,
        order_by=[trackpoint_table.c.id.desc()])

    orm.mapper(timezone, timezone_table,
        order_by=[timezone_table.c.id.desc()])



meta = sa.MetaData()

log_table = sa.Table("log", meta,
    sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
    sa.Column("infomarker_id", types.Integer, ForeignKey('trackpoint.id')),
    sa.Column("topic", types.UnicodeText),
    sa.Column("content", types.UnicodeText), 
    sa.Column("createdate", types.TIMESTAMP(timezone=True),default=now()),
    )

class log(object):
    def __str(self):
        return self.title

country_table = sa.Table("country", meta,
    sa.Column("iso_numcode", types.Integer, primary_key=True),
    sa.Column("continent_id", types.Integer, ForeignKey('continent.id')),
    sa.Column("iso_countryname",types.VARCHAR(128)),
    sa.Column("iso3_nationalcode",types.VARCHAR(3)),
    sa.Column("flickr_countryname",types.VARCHAR(128))
    )

class country(object):
    def __str(self):
        return self.title

continent_table = sa.Table("continent", meta,
    sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
    sa.Column("name",types.VARCHAR(128))
    )

class continent(object):
    def __str(self):
        return self.title

comment_table = sa.Table("comments", meta,
    sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
    sa.Column("log_id", types.Integer, ForeignKey('log.id')),
    sa.Column("alias", types.VARCHAR(128)),
    sa.Column("date", types.TIMESTAMP(timezone=True)),
    sa.Column("email", types.VARCHAR(128)),
    sa.Column("region", types.UnicodeText),
    sa.Column("comment", types.UnicodeText),
    )

class comments(object):
    def __str(self):
        return self.title

imageinfo_table = sa.Table("imageinfo", meta,
    sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
    sa.Column("log_id", types.Integer, ForeignKey('log.id')),
    sa.Column("photoset_id", types.Integer, ForeignKey('photosets.id')),
    sa.Column("infomarker_id", types.Integer, ForeignKey('trackpoint.id')),
    sa.Column("trackpoint_id", types.Integer, ForeignKey('trackpoint.id')),
    sa.Column("flickrfarm", types.VARCHAR(256)),
    sa.Column("flickrserver", types.VARCHAR(256)),
    sa.Column("flickrphotoid", types.VARCHAR(256)),
    sa.Column("flickrsecret", types.VARCHAR(256)),
    sa.Column("flickrdatetaken", types.TIMESTAMP(timezone=True)),
    sa.Column("flickrtitle", types.VARCHAR(256)),
    sa.Column("flickrdescription", types.UnicodeText),
    sa.Column("photohash", types.VARCHAR(256)),
    sa.Column("photohash_990", types.VARCHAR(256)),
    sa.Column("imgname", types.VARCHAR(64)),
    )

class imageinfo(object):
    def __str(self):
        return self.title

photoset_table = sa.Table("photosets", meta,
    sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
    sa.Column("flickrsetid", types.VARCHAR(256)),
    sa.Column("flickrowner", types.VARCHAR(256)),
    sa.Column("flickrprimary", types.VARCHAR(256)),
    sa.Column("flickrphotocount", types.Integer),
    sa.Column("flickrtitle", types.VARCHAR(256)),
    sa.Column("flickrdescription", types.UnicodeText),
    )

class photosets(object):
    def __str(self):
        return self.title

trackpoint_table = sa.Table("trackpoint", meta,
    sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
    sa.Column("track_id", types.Integer, ForeignKey('track.id')),
    sa.Column("timezone_id", types.Integer, ForeignKey('timezone.id')),
    sa.Column("country_id", types.Integer, ForeignKey('country.iso_numcode')),
    sa.Column("latitude", types.Numeric(9,7)),
    sa.Column("longitude", types.Numeric(10,7)),
    sa.Column("altitude", types.Integer),
    sa.Column("velocity", types.Integer),
    sa.Column("temperature", types.Integer),
    sa.Column("direction", types.Integer),
    sa.Column("pressure", types.Integer),
    sa.Column("timestamp", types.TIMESTAMP(timezone=True)),
    sa.Column("infomarker", types.Boolean, default=False, nullable=False),
    sa.Column("location", types.VARCHAR(256)),
    )

class trackpoint(object):
    def __str(self):
        return self.title


track_table = sa.Table("track", meta,
    sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
    sa.Column("date", types.TIMESTAMP(timezone=True)),
    sa.Column("trkptnum", types.Integer),
    sa.Column("distance", types.Numeric(11,4)),
    sa.Column("timespan", types.Interval),
    sa.Column("gencpoly_pts", types.UnicodeText),
    sa.Column("gencpoly_levels", types.UnicodeText),
    sa.Column("color", types.CHAR(6), default='FF0000'),
    )

class track(object):
    def __str(self):
        return self.title

timezone_table = sa.Table("timezone", meta,
    sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
    sa.Column("utcoffset", types.Interval),
    sa.Column("abbreviation", types.VARCHAR(256)),
    sa.Column("description", types.VARCHAR(256)),
    sa.Column("region", types.VARCHAR(256)),
    )

class timezone(object):
    def __str(self):
        return self.title

image2tag_table = sa.Table("image2tag", meta,
    sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
    sa.Column("imageinfo_id", types.Integer, ForeignKey('imageinfo.id')),
    sa.Column("phototag_id", types.Integer, ForeignKey('phototag.id')),
   )

class image2tag(object):
    def __str(self):
        return self.title

phototag_table = sa.Table("phototag", meta,
    sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
    sa.Column("tag", types.VARCHAR(256)),
    sa.Column("flickrtagid", types.VARCHAR(256)),
    )

class phototag(object):
    def __str(self):
        return self.title


