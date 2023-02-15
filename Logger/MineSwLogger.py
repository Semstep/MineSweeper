"""DEBUG, INFO, WARNING, ERROR и CRITICAL"""
import logging
import logging.config
import yaml

DEBUG = True

DEFNAME = 'slave'

def config():
    with open(r'Logger\logging_config.yml', 'r') as cf:
        LOG_CONF = yaml.safe_load(cf.read())

    logging.config.dictConfig(LOG_CONF)
    lgr = logging.getLogger('slave.' + __name__)
    lgr.setLevel(logging.DEBUG)
    lgr.info(f'Logger was configured')


if __name__ == '__main__':
    # lgr.debug('Debug mess')
    # lgr.info('Some info')
    # lgr.warning('Stay warned!')
    # lgr.error('Some error occured!!')
    # lgr.critical('We dropped everything at all, Natasha'.upper())
    ...