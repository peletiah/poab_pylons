"""Setup the poab application"""
import logging

from paste.deploy import appconfig
from pylons import config

from poab.config.environment import load_environment
from poab import model

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup poab here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    log.info("Creating database tables")
    model.meta.create_all(bind=model.engine)
    log.info("Finished setting up")
