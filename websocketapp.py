import asyncio
import json
import logging
import websockets
import Exchanges.TimeAggregator
from mongo_db_connection import MongoDBConnection


# Метод, который осуществляет постоянный коннект с портом и IP
async def arbitration_socket(websocket, path):
    # Вмазанная часть коннекта и постоянной пары
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    while 1:
        # Довольно простая реализация через arbitration aggregate, собираем данные в JSON пакет и передаем на сервер.
        db.temporaryTick.drop()
        Exchanges.TimeAggregator.arbitration_aggregate()
        ttc = db.temporaryTick.find()
        ticks = list(ttc)
        cnames = db.temporaryTick.distinct('Exch')
        rnames = db.temporaryTick.distinct('PairName')
        from bson.json_util import dumps as dss
        websocket_arbitration = {'ticks': dss(ticks), 'cnames': sorted(cnames),
                                 'rnames': sorted(rnames)}
        websocket_arbitration = json.dumps(websocket_arbitration)
        await websocket.send(websocket_arbitration)
        ttc.close()
        await asyncio.sleep(30)

# На данный момент блок кода ничего не отлавливает.
try:
    if asyncio.get_event_loop().is_running():
        asyncio.get_event_loop().close()
except ():
    logging.info(u'non crit')

logging.info(u'Arbitartion websocket started')
# Отлавливаем наш While 1 event, т.е arbitration_socket и заставляем сокет слушать его бегать бесконечно.
asyncio.get_event_loop().run_until_complete(websockets.serve(arbitration_socket, '127.0.0.1', 8090))
asyncio.get_event_loop().run_forever()



