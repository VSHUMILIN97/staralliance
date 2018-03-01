from django.core.management.base import BaseCommand, CommandError
import logging
import atexit
import time
import os
import sys
from process_manager import children_kill, proc_start


# Log config should be changed
class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.info(u'Process manager started')
        try:
            # windows/mac debug starter
            if sys.platform == 'win32' or 'darwin':
                try:
                    proc_start()
                    logging.info(u"Processes're successfully started")
                    while True:
                        time.sleep(0.1)
                except OSError:
                    logging.error(u'Processes were not started\nTerminating command')
                    sys.exit(0)
            else:
                # Production starter
                logging.info(u'Threads"re successfully started')
                parent_pipe, child_pipe = os.pipe()
                try:
                    pid = os.fork()
                    if pid == 0:
                        os.close(child_pipe)
                        sys.stdin.close()
                        sys.stdout.close()
                        sys.stderr.close()
                        proc_start()
                        while True:
                            time.sleep(0.1)
                    else:
                        os._exit(0)
                except OSError:
                    logging.error(u'Processes were not started on production\nTerminating command')
                    sys.exit(-1)
        except OSError:
            logging.critical(u'Process manager is unreachable. Check CODE')
        try:
            atexit.register(children_kill)
        except OSError:
            logging.critical(u'Process manager cannot kill processes\nUse `kill` command in terminal')
