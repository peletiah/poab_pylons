"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *
import math


def countryDetails(model,country_id):
    if country_id==0:
        navstring='''<li class="navigation"><ul><li class="navli"><a href="#" title="Show all entries" onclick="resetContent();">All</a></li></ul></li>'''
        return navstring
    q = model.Session.query(model.country).filter(model.country.iso_numcode==country_id)
    country=q.one()
    navstring='''<li class="navigation"><ul><li class="navli"><a href="#" title="Journal-entries for all countries" onclick="resetContent\(\);">All</a>&#8594;<a href="#" title="Content for %s" onclick="showContent(\\'%s\\');">%s</a></li></ul></li>''' % (country.iso_countryname,country.iso_numcode,country.iso_countryname)
    return navstring
    
    

def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc
