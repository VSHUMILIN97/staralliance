import asyncio
import datetime
import json
import websockets
import Exchanges.TimeAggregator
from mongo_db_connection import MongoDBConnection



async def arbitration_socket(websocket, path):
    while True:
       b = MongoDBConnection().start_db()
       db = b.PiedPiperStock
       db.temporaryTick.drop()
       Exchanges.TimeAggregator.arbitration_aggregate()
       ticks = str(list(db.temporaryTick.find()))
       columns = json.dumps(len(db.temporaryTick.distinct('Exch')), ensure_ascii=False)
       rows = json.dumps(len(db.temporaryTick.distinct('PairName')), ensure_ascii=False)
       cnames = json.dumps(db.temporaryTick.distinct('Exch'), ensure_ascii=False)
       rnames = json.dumps(db.temporaryTick.distinct('PairName'), ensure_ascii=False)
       now = datetime.datetime.utcnow().isoformat() + 'Z'
       await websocket.send(now)
       await websocket.send(str(ticks))
       await websocket.send(str(columns))
       await websocket.send(str(rows))
       await websocket.send(str(cnames))
       await websocket.send(str(rnames))
       await asyncio.sleep(30)


asyncio.get_event_loop().run_until_complete(websockets.serve(arbitration_socket, '127.0.0.1', 8080))
asyncio.get_event_loop().run_forever()



