import logging
from stock_synchronizer import settings

logger = logging.getLogger(__name__)


class EventPublisher:

    def __init__(self):
        self.file_dir = settings.get('output_file')
        with open(self.file_dir, 'w'):
            logger.info('Creating empty output file {}'.format(self.file_dir))

    def publish(self, message):
        with open(self.file_dir, 'a') as file:
            file.write(message + '\n')
            logger.info('Sent event: {}'.format(message))
