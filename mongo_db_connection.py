from pymongo import MongoClient
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)


# Functional class for connection to MongoDB
# This wrapper is not yet completed
class MongoDBConnection:
    # Start connection for opening cursors
    def start_db(self):
        connect = MongoClient('localhost', 27017)
        logging.info(u'Connection to the MONGODB has been established')
        return connect

    # Interrupting connection for releasing MongoDB resources
    def stop_connect(self):
        self.start_db().close()
