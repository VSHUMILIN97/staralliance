from pymongo import MongoClient
import logging
from PiedPiper.settings import MONGODB_DEFAULT_PORT, LOCAL_SERVICE_HOST, STARALLIANS_HOST

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


# Functional class for connection to MongoDB
# This wrapper is not yet completed
class MongoDBConnection:

    # Start connection for opening cursors
    def start_local(self):
        connect = MongoClient(LOCAL_SERVICE_HOST, MONGODB_DEFAULT_PORT)
        logging.info(u'Connection to the MONGODB has been established')
        return connect

    # Interrupting connection for releasing MongoDB resources
    def stop_connect(self):
        self.start_local().close()

    def start_remote(self):
        connect = MongoClient(STARALLIANS_HOST, MONGODB_DEFAULT_PORT)
        return connect
