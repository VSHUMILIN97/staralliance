import asyncio
import time
import json
import logging
import websockets
from mongo_db_connection import MongoDBConnection


logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

# Initial
# Метод, который осуществляет постоянный коннект с портом и IP
async def arbitration_socket(websocket, path):
    # Вмазанная часть коннекта и постоянной пары
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    while 1:
        # Довольно простая реализация через arbitration aggregate, собираем данные в JSON пакет и передаем на сервер.
        # db.temporaryTick.drop()
        # Exchanges.TimeAggregator.arbitration_aggregate()
        # ttc = db.temporaryTick.find()
        # ticks = list(ttc)
        sttime = time.time()
        cnames = db.PoorArb.distinct('Value.Exchange')
        rnames = db.Arbnames.distinct('Value')
        arbitary_data = db.PoorArb.find({}, {"_id": False}).limit(1)
        if arbitary_data.count() == 0:
            time.sleep(1)
            arbitary_data = db.PoorArb.find({}, {"_id": False})
        from bson.json_util import dumps as dss
        # ExchangeModel.whole_data
        websocket_arbitration = {'ticks': dss(arbitary_data), 'cnames': sorted(cnames),
                                 'rnames': sorted(rnames)}
        websocket_arbitration = json.dumps(websocket_arbitration)
        await websocket.send(websocket_arbitration)
        arbitary_data.close()
        mttime = time.time() - sttime
        await asyncio.sleep(22 - mttime)

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



