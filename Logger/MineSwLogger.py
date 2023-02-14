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
    logger = logging.getLogger('slave.'+__name__)
    logger.setLevel(logging.DEBUG)
    logger.info(f'Logger was configured')


if __name__ == '__main__':
    # logger.debug('Debug mess')
    # logger.info('Some info')
    # logger.warning('Stay warned!')
    # logger.error('Some error occured!!')
    # logger.critical('We dropped everything at all, Natasha'.upper())
    ...