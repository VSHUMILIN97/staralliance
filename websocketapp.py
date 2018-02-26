import asyncio
import time
import json
import logging
import websockets
from mongo_db_connection import MongoDBConnection


logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


# Function, that provides connect between client and server.
# Works with async to prevent interrupting main thread.
async def arbitration_socket(websocket, path):
    # After the connect with client was established open connect to MongoDB
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    while 1:
        # Checking for the initial time
        sttime = time.time()
        # Checking for the distinct Exchange and Pair names.
        cnames = db.PoorArb.distinct('Value.Exchange')
        rnames = db.Arbnames.distinct('Value')
        arbitage_data = db.PoorArb.find({}, {"_id": False}).limit(1)
        # Checking for the current data after it was inserted.
        if arbitage_data.count() == 0:
            time.sleep(1)
            arbitage_data = db.PoorArb.find({}, {"_id": False})
        # Importing library to transform data to JSON format
        from bson.json_util import dumps as dss
        # Creating dict to pass it through socket transport
        websocket_arbitration = {'ticks': dss(arbitage_data), 'cnames': sorted(cnames),
                                 'rnames': sorted(rnames)}
        websocket_arbitration = json.dumps(websocket_arbitration)
        # Creating a co-routine for pass data
        await websocket.send(websocket_arbitration)
        # Closing the cursor
        arbitage_data.close()
        # Checking for the ending time
        mttime = time.time() - sttime
        # Creating a co-routine. Sending a subprocess to sleep.
        await asyncio.sleep(25 - mttime)

logging.info(u'Arbitartion websocket started')
# Initialise websocket connection on host 127.0.0.1 and port 8090
asyncio.get_event_loop().run_until_complete(websockets.serve(arbitration_socket, '127.0.0.1', 8090))
asyncio.get_event_loop().run_forever()



