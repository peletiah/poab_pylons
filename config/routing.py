"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('error/:action/:id', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('', controller='log', action='index', startfromlog=0)
    map.connect('log/', controller='log', action='index', startfromlog=0)
    map.connect('log/:startfromlog', controller='log', action='index', startfromlog=0)
    map.connect('log/index/:startfromlog', controller='log', action='index', startfromlog=0)
    map.connect('log/country/', controller='log', action='country', country_id=0, page=0)
    map.connect('log/country/:country_id/:page', controller='log', action='country', country_id=0, page=0)
    map.connect('log/c/', controller='log', action='c', country_id=0, page=0)
    map.connect('log/c/:country_id/:page', controller='log', action='c', country_id=0, page=0)
    map.connect('track/c/', controller='track', action='c', country_id=0)
    map.connect('track/c/:country_id', controller='track', action='c', country_id=0)
    map.connect('view/c/', controller='view', action='c', country_id=0,page=0)
    map.connect('view/c/:country_id/:page', controller='view', action='c', country_id=0, page=0)
    map.connect('view/country/', controller='view', action='country', country_id=0, page=0)
    map.connect('view/country/:country_id/:page', controller='view', action='country', country_id=0, page=0)
    map.connect('view/', controller='view', action='index')
    map.connect('view/tabbed/:startfromimage', controller='view', action='tabbed', startfromimage=0)
    map.connect('gallery/:infomarker/:startfromimg', controller='view', action='gallery')
    map.connect('view/gallery/:infomarker/:startfromimg', controller='view', action='gallery')
    map.connect('view/infomarker/:infomarker/:startfromimage', controller='view', action='infomarker')
    map.connect('track/simple/:trackpoint/:imageid', controller='track', action='simple')
    map.connect(':controller/:action/:id')

    return map
