"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *


def countryDetails(model,country_id):
    if country_id==0:
        navstring='''<li id="navigation"><a href="#" title="Show all entries" onclick="resetContent();">All</a></li>'''
        return navstring
    q = model.Session.query(model.country).filter(model.country.iso_numcode==country_id)
    country=q.one()
    navstring='''<li id="navigation"><a href="#" title="Journal-entries for all countries" onclick="resetContent();">All</a>&#8594;<a href="#" title="Content for %s" onclick="showContent(\\'%s\\');">%s</a></li>''' % (country.iso_countryname,country.iso_numcode,country.iso_countryname)
    return navstring
    
    
