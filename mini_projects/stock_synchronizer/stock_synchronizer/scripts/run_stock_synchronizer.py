import ujson
from stock_synchronizer import settings
from stock_synchronizer.startup import startup
from stock_synchronizer.event_sourcing.worker import EventWorker


WORKER = EventWorker()


def summary():
    dct = {
        'type': 'Summary',
    }
    return ujson.dumps(dct)


def main():
    startup()

    file_dir = settings.get('input_file')
    with open(file_dir, 'r') as file:
        for line in file:
            WORKER.process_message(line.rstrip())
    WORKER.process_message(summary())
