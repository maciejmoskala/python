import logging
import traceback
from stock_synchronizer.core.input_event import JsonInputEvent
from stock_synchronizer.core.event_processor import process_event

logger = logging.getLogger(__name__)


class EventWorker:

    def process_message(self, message):
        logger.info('Received event: {}'.format(message))

        try:
            event = JsonInputEvent.from_json(message)
        except Exception as exc:
            logger.error(traceback.format_exc())
            return

        try:
            process_event(event)
        except Exception as exc:
            logger.error(traceback.format_exc())
