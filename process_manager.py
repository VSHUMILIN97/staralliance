# В качестве подпроцесса child выбираем скрипт websocketapp.py
# В качестве аргументов для начала работы подпроцесса передаем команду execute и указываем на потомка
import os
import subprocess
import sys
import signal
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)
"""
#
#
# IN WORK, BUT NOTHING SHOULD BE CHANGED
#
#
"""


def proc_start():
    global agtion_pid, arbitration_ws_pid, ws_charts_pid, agtion_tick_pid, agtion_vol_pid
    # Далее открываем субпроцесс, в качестве "входа" используем PIPE.
    # Arbitration 8090 port Web-socket subprocess
    try:
        arbitration_ws = os.path.join(os.path.dirname(__file__), "websocketapp.py")
    except FileNotFoundError:
        logging.error(u'Web-socket process could not be reached. Check File path')
        sys.exit(-1)
    arbitration_ws_command = [sys.executable, arbitration_ws]
    try:
        arbitartion_ws_pipe = subprocess.Popen(arbitration_ws_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    except OSError:
        logging.error(u'Web-socket process could not be started. Check logs.')
        sys.exit(-1)
    # PID Declaration
    arbitration_ws_pid = arbitartion_ws_pipe.pid
    #
    # Charts 8070 port Web-Socket subprocess
    # try:
    #     ws_charts = os.path.join(os.path.dirname(__file__), "websocketcharts.py")
    # except FileNotFoundError:
    #     logging.error(u'Web-socket_charts process could not be reached. Check File path')
    #     sys.exit(-1)
    # ws_charts_command = [sys.executable, ws_charts]
    # try:
    #     ws_charts_pipe = subprocess.Popen(ws_charts_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # except OSError:
    #     logging.error(u'Web-socket_charts process could not be started. Check logs.')
    #     os.kill(arbitration_ws_pid, signal.SIGTERM)
    #     sys.exit(-1)
    # # PID Declaration
    # ws_charts_pid = ws_charts_pipe.pid
    # #
    # # OHLC aggregation subprocess
    # try:
    #     agtion_ohlc = os.path.join(os.path.dirname(__file__), "aggregation_OHLC.py")
    # except FileNotFoundError:
    #     logging.error(u'AggregationOHLC process could not be reached. Check File path')
    #     sys.exit(-1)
    # agtion_ohlc_command = [sys.executable, agtion_ohlc]
    # try:
    #     agtion_ohlc_pipe = subprocess.Popen(agtion_ohlc_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # except OSError:
    #     logging.error(u'AggregationOHLC process could not be started. Check logs.')
    #     os.kill(arbitration_ws_pid, signal.SIGTERM)
    #     os.kill(ws_charts_pid, signal.SIGTERM)
    #     sys.exit(-1)
    # PID Declaration
    # agtion_pid = agtion_ohlc_pipe.pid
    # """       This block should be uncommented when the time will come        """
    # Tick aggregation subprocess  / Uncomment if needed
    # try:
    #     agtion_tick = os.path.join(os.path.dirname(__file__), "aggregation_Tick.py")
    # except FileNotFoundError:
    #     logging.error(u'Aggregation_Tick process could not be reached. Check File path')
    #     sys.exit(-1)
    # agtion_tick_command = [sys.executable, agtion_tick]
    # try:
    #     agtion_tick_pipe = subprocess.Popen(agtion_tick_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # except OSError:
    #     logging.error(u'AggregationOHLC process could not be started. Check logs.')
    #     os.kill(arbitration_ws_pid, signal.SIGTERM)
    #     os.kill(ws_charts_pid, signal.SIGTERM)
    #     os.kill(agtion_pid, signal.SIGTERM)
    #     sys.exit(-1)
    # # PID Declaration
    # agtion_tick_pid = agtion_tick_pipe.pid
    # #
    # # Volume aggregation subprocess
    # try:
    #     agtion_vol = os.path.join(os.path.dirname(__file__), "aggregation_Vol.py")
    # except FileNotFoundError:
    #     logging.error(u'Aggregation_Volume process could not be reached. Check File path')
    #     sys.exit(-1)
    # agtion_vol_command = [sys.executable, agtion_vol]
    # try:
    #     agtion_vol_pipe = subprocess.Popen(agtion_vol_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # except OSError:
    #     logging.error(u'AggregationOHLC process could not be started. Check logs.')
    #     os.kill(arbitration_ws_pid, signal.SIGTERM)
    #     os.kill(ws_charts_pid, signal.SIGTERM)
    #     os.kill(agtion_pid, signal.SIGTERM)
    #     os.kill(agtion_tick_pid, signal.SIGTERM)
    #     sys.exit(-1)
    # # PID Declaration
    # agtion_vol_pid = agtion_vol_pipe.pid


def children_kill():
    if agtion_pid is None:
        pass
    else:
        try:
            os.kill(arbitration_ws_pid, signal.SIGTERM)
            # os.kill(ws_charts_pid, signal.SIGTERM)
            # os.kill(agtion_pid, signal.SIGTERM)
            # os.kill(agtion_tick_pid, signal.SIGTERM)
            # os.kill(agtion_vol_pid, signal.SIGTERM)
        except OSError:
            logging.critical(u'Process manager cannot kill processes\nUse `kill` command in terminal')
            logging.info(u'Web-Socket rundown')
            sys.exit(-1)
