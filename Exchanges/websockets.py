import asyncio
import datetime
import random
import websockets
from .TimeAggregator import arbitration_aggregate
from mongo_db_connection import MongoDBConnection


async def arbitration(websocket, path):
    while True:
        arbitration_aggregate()
        b = MongoDBConnection().start_db()
        db = b.PiedPiperStock
        db.temporaryTick.drop()
        ticks = list(db.temporaryTick.find())
        columns = len(db.temporaryTick.distinct('Exch'))
        rows = len(db.temporaryTick.distinct('PairName'))
        cnames = db.temporaryTick.distinct('Exch')
        rnames = db.temporaryTick.distinct('PairName')
        await websocket.send(ticks, columns, rows, cnames, rnames)
        await asyncio.sleep(300)

def returner():
    start_server = websockets.serve(arbitration, '127.0.0.1', 5678)
    return start_server

asyncio.get_event_loop().run_until_complete(returner())
asyncio.get_event_loop().run_forever()
