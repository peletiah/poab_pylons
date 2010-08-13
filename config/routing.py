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

    map.connect('', controller='log', action='index')

    map.connect('feed/', controller='feed', action='index')

    map.connect('log/', controller='log', action='index')
    map.connect('log/s/', controller='log', action='id', log_id=0)
    map.connect('log/s/:log_id', controller='log', action='id', log_id=0)
    map.connect('log/id/', controller='log', action='id', log_id=0)
    map.connect('log/id/:log_id', controller='log', action='id', log_id=0)
    map.connect('log/c/', controller='log', action='c', id1=0, page=None)
    map.connect('log/c/:id1/:page', controller='log', action='c', id1=0, page=None)
    map.connect('track/c/', controller='track', action='c', id1=0)
    map.connect('track/c/:id1', controller='track', action='c', id1=0)
    map.connect('track/simple/:trackpoint/:imageid', controller='track', action='simple',imageid=None)
    map.connect('track/markerbounds/', controller='track', action='markerbounds', country_id=0)
    map.connect('track/markerbounds/:country_id', controller='track', action='markerbounds', country_id=0)    
    
    map.connect('view/', controller='view', action='index')
    map.connect('view/c/', controller='view', action='c', id1=0,page=None)
    map.connect('view/c/:id1/:page', controller='view', action='c', id1=0, page=None)
    map.connect('view/gallery/:infomarker/:startfromimg', controller='view', action='gallery')
    map.connect('view/infomarker/:id1/:page', controller='view', action='infomarker',id1=0,page=0)
    map.connect('view/id', controller='view', action='id',id=0)

    map.connect('misc/navstr/', controller='misc', action='navstring', country_id=0)
    map.connect('misc/navstr/:country_id/', controller='misc', action='navstring', country_id=0)
    
    map.connect('misc/country_svg/', controller='misc', action='country_svg', country_id=0)
    map.connect('misc/country_svg/:country_id/', controller='misc', action='country_svg', country_id=0)
 
    map.connect(':controller/:action/:id')

    return map
