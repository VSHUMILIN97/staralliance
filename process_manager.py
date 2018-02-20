
# В качестве подпроцесса child выбираем скрипт websocketapp.py
# В качестве аргументов для начала работы подпроцесса передаем команду execute и указываем на потомка
import os
import subprocess
import sys
import signal
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


def proc_start():
    global data_parse_pid, agtion_pid, arbitartion_ws_pid, ws_charts_pid, agtion_tick_pid, agtion_vol_pid
    # Далее открываем субпроцесс, в качестве "входа" используем PIPE.
    arbitration_ws = os.path.join(os.path.dirname(__file__), "websocketapp.py")
    arbitration_ws_command = [sys.executable, arbitration_ws]
    arbitartion_ws_pipe = subprocess.Popen(arbitration_ws_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # Charts 8070 port Web-Socket subprocess
    ws_charts = os.path.join(os.path.dirname(__file__), "websocketcharts.py")
    ws_charts_command = [sys.executable, ws_charts]
    ws_charts_pipe = subprocess.Popen(ws_charts_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # Data parse subprocess
    data_parse = os.path.join(os.path.dirname(__file__), "data_parser.py")
    data_parse_command = [sys.executable, data_parse]
    data_parse_pipe = subprocess.Popen(data_parse_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # OHLC aggregation subprocess
    agtion_ohlc = os.path.join(os.path.dirname(__file__), "aggregation_OHLC.py")
    agtion_ohlc_command = [sys.executable, agtion_ohlc]
    agtion_ohlc_pipe = subprocess.Popen(agtion_ohlc_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # Tick aggregation subprocess  / Uncomment if needed
    # agtion_tick = os.path.join(os.path.dirname(__file__), "aggregation_Tick.py")
    # agtion_tick_command = [sys.executable, agtion_tick]
    # agtion_tick_pipe = subprocess.Popen(agtion_tick_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # Volume aggregation subprocess
    agtion_vol = os.path.join(os.path.dirname(__file__), "aggregation_Vol.py")
    agtion_vol_command = [sys.executable, agtion_vol]
    agtion_vol_pipe = subprocess.Popen(agtion_vol_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # Process ID's
    data_parse_pid = data_parse_pipe.pid
    agtion_pid = agtion_ohlc_pipe.pid
    arbitartion_ws_pid = arbitartion_ws_pipe.pid
    ws_charts_pid = ws_charts_pipe.pid
    # agtion_tick_pid = agtion_tick_pipe.pid  # Uncomment if needed
    agtion_vol_pid = agtion_vol_pipe.pid


def children_kill():
    if agtion_pid is None:
        pass
    else:
        os.kill(arbitartion_ws_pid, signal.SIGTERM)
        os.kill(ws_charts_pid, signal.SIGTERM)
        os.kill(agtion_pid, signal.SIGTERM)
        # os.kill(agtion_tick_pid, signal.SIGTERM)  # Uncomment if needed
        os.kill(data_parse_pid, signal.SIGTERM)
        os.kill(agtion_vol_pid, signal.SIGTERM)
        logging.info(u'WebSocket rundown')
