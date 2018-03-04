import signal
import subprocess
from django.core.management.base import BaseCommand, CommandError
import logging
import atexit
import time
import os
import sys


def livecoin_subprocess():
    try:
        script_path = os.path.join(os.path.dirname(__file__), '../../../Exchanges/ExchangeAPI/livecoinAPI.py')
    except FileNotFoundError:
        logging.error(u'LivecoinAPI process could not be reached. Check File path')
        sys.exit(-1)
    poloniex_command = [sys.executable, script_path]
    try:
        poloniex_pipe = subprocess.Popen(poloniex_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    except OSError:
        logging.error(u'LivecoinAPI process could not be started. Check logs.')
        sys.exit(-1)
    # PID Declaration
    poloniex_pid = poloniex_pipe.pid
    return poloniex_pid


# Log config should be changed
class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.info(u'Process manager started')
        try:
            # windows/mac debug starter
            if sys.platform == 'win32' or 'darwin':
                try:
                    process = livecoin_subprocess()
                    logging.info(u"Process is successfully started")
                    while True:
                        time.sleep(0.1)
                except OSError:
                    logging.error(u'Process was not started\nTerminating command')
                    sys.exit(0)
            else:
                # Production starter
                logging.info(u'Production process starter successfully started')
                parent_pipe, child_pipe = os.pipe()
                try:
                    pid = os.fork()
                    if pid == 0:
                        os.close(child_pipe)
                        sys.stdin.close()
                        sys.stdout.close()
                        sys.stderr.close()
                        process = livecoin_subprocess()
                        while True:
                            time.sleep(0.1)
                    else:
                        os._exit(0)
                except OSError:
                    logging.error(u'Process was not started on production\nTerminating command')
                    sys.exit(-1)
        except OSError:
            logging.critical(u'Process manager is unreachable. Check CODE')
        try:
            atexit.register(os.kill(process, signal.SIGTERM))
        except OSError:
            logging.critical(u'Process manager cannot kill processes\nUse `kill` command in terminal')
