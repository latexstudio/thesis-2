#!/usr/bin/env python3.6

import logging
import subprocess
import sys
import time

from datetime import datetime


from pync import Notifier
from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEvent, FileSystemEventHandler
)


# Make will be triggered every time a file changed.
# But it will wait at least specified seconds.
MAKE_MIN_PERIOD = 120


logging.basicConfig(
    format='%(asctime)s: %(levelname)s: %(message)s',
    level=logging.DEBUG,
)
log = logging.getLogger(__name__)


def main():
    folders = (
        '/Users/kai/Sync/Master/mes.wiki',
        '/Users/kai/Sync/Master/thesis',
        '/Users/kai/Library/Mobile Documents/27N4MQEA55~pro~writer/Documents/mes.wiki',
        '/Users/kai/Library/Mobile Documents/27N4MQEA55~pro~writer/Documents/thesis',
    )

    handler = Maker()
    observer = Observer()
    for folder in folders:
        log.info(f'Watching {folder}...')
        observer.schedule(handler, folder, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


class Maker(FileSystemEventHandler):
    def __init__(self, *args, **kwargs):
        super(Maker, self).__init__()
        self.last_run = datetime.min

    def on_any_event(self, event: FileSystemEvent):
        """
        Events are queued.
        """
        log.debug(event)

        secs_since_last_run = abs((self.last_run - datetime.now()).total_seconds())
        if secs_since_last_run < MAKE_MIN_PERIOD:
            log.info(f'Waiting at least {MAKE_MIN_PERIOD} seconds to start next run...')
            try:
                time.sleep(MAKE_MIN_PERIOD)
            except KeyboardInterrupt:
                sys.exit(0)

        self.last_run = datetime.now()
        try:
            subprocess.check_call(['make'])
            Notifier.notify('😎😎😎😎😎😎', title='Build succeeded')
        except subprocess.CalledProcessError:
            Notifier.notify('😡😡😡😡😡😡', title='Build failed')
            sys.exit(1)


if __name__ == '__main__':
    main()
