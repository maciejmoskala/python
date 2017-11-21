import logging
import logging.config
import stock_synchronizer
from stock_synchronizer import settings
from stock_synchronizer.core.rpc import initialize as initialize_rpc

logger = logging.getLogger(__name__)


def configure_logging():
    logging_conf = settings.get('logger')
    logging.config.dictConfig(logging_conf)


def startup():
    settings.load()
    configure_logging()
    initialize_rpc()
    logger.info(
        'Stock synchronizer {} running with config: {}.'.format(
            stock_synchronizer.__version__, settings.get('config')
        )
    )
