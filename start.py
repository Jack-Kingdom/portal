import sys
import logging
from tornado.ioloop import IOLoop
from config import CONFIG
from api.v1 import make_app

logger = logging.getLogger()
logger.setLevel('DEBUG' if CONFIG['DEBUG'] else 'INFO')
logger.addHandler(logging.StreamHandler(sys.stdout))

if __name__ == "__main__":
    app = make_app()
    app.listen(CONFIG['LISTENING_PORT'], address=CONFIG['LISTENING_ADDRESS'])

    try:
        logger.info('started at {address}:{port}'
                    .format(address=CONFIG['LISTENING_ADDRESS'], port=CONFIG['LISTENING_PORT']))
        IOLoop.current().start()
    except KeyboardInterrupt:
        logger.info('KeyboardInterrupt received, server stopped.')
