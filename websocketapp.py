import asyncio
import datetime
import json
import websockets
import Exchanges.TimeAggregator
from mongo_db_connection import MongoDBConnection



async def arbitration_socket(websocket, path):
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    while True:
       db.temporaryTick.drop()
       Exchanges.TimeAggregator.arbitration_aggregate()
       ticks = list(db.temporaryTick.find())
       cnames = db.temporaryTick.distinct('Exch')
       rnames = db.temporaryTick.distinct('PairName')
       from bson.json_util import dumps as dss
       websocket_arbitration = {'ticks': dss(ticks), 'cnames': cnames, 'rnames': rnames}
       websocket_arbitration = json.dumps(websocket_arbitration)
       await websocket.send(websocket_arbitration)
       await asyncio.sleep(30)
#

asyncio.get_event_loop().run_until_complete(websockets.serve(arbitration_socket, '127.0.0.1', 8080))
asyncio.get_event_loop().run_forever()



