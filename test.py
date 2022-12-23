import logging


log = logging.getLogger(__name__)
logging.basicConfig(filename='test.log', format='%(asctime)s:%(levelname)s:%(message)s')

log.setLevel(logging.DEBUG)
log.debug('This is a debug message')
log.info('This is an info message')
log.warning('This is a warning message')
log.error('This is an error message')
log.critical('This is a critical message')
