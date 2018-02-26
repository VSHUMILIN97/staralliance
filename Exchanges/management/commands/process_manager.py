from django.core.management.base import BaseCommand, CommandError
import logging
import atexit
import time
import os
from process_manager import children_kill, proc_start


# Here, I tried to make my logs better and better
#
class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.info(u'Server started')

        try:
            # Uncomment this block to launch this app on production server.
            logging.info(u'Threads"re successfully started')
            parent_pipe, child_pipe = os.pipe()
            """pid = os.fork()
            if pid == 0:
                os.close(child_pipe)
                sys.stdin.close()
                sys.stdout.close()
                sys.stderr.close()"""
            proc_start()
            while True:
                time.sleep(0.1)
            #else:
               # os._exit(0)

        except():
            logging.critical(u'Threads were not started')

        atexit.register(children_kill)
