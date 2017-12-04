from datetime import datetime
import time
from mongo_db_connection import MongoDBConnection
import dateutil.parser
from datetime import datetime, tzinfo, timedelta
from django.utils import timezone, datetime_safe


def OHLCaggregation(ServerTime):
    print('Aggregating.....bzzzzz......'+str(time.time()))
    global HighestValue, endingtime
    global LowestValue
    global LastValue
    global PrevDayValue
    global TimeStamp
    global PairName
    # Комменты завтра. Я ща сдохну.
    print(ServerTime)
    b = MongoDBConnection().start_db()
    db = b.PiedPiperStock
    exchlist = ['Bittrex']
    for inner in range(0, len(exchlist)):
        exchname = exchlist[inner]
        pairlist = db[exchname].distinct('PairName')
        # Подобная штука не работает, он тщательно отказывается видеть вложенный цикл.
        #for secinner in range(0, len(pairlist)):
        #
        for secinner in pairlist:
            #print(secinner)
            # All Matches in DB
            timerDelay = db[exchname].find({'PairName': secinner, 'Mod': False}, {'TimeStamp': True}).limit(1)
            #
            delayActivation = timedelta(minutes=5)
            for subinto in timerDelay:
                startingtime = dateutil.parser.parse(str(subinto['TimeStamp']))
            #
            mergingtime = startingtime + delayActivation
            while 1:
                if mergingtime < ServerTime:
                    tempdel = timedelta(minutes=2, seconds=30)
                    # High Работа с глобальными переменными. Переприсвоится дальше.
                    HighestValue = 0
                    endingtime = startingtime + delayActivation
                    # Low Записываем значение из одномерного словаря (Это можно отрефакторить - WELCOME!)
                    LowValDict = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp': {'$gte': startingtime, '$lt': endingtime}}, {'Low': True}).limit(1)
                    # Last Пишем первый объект из коллекции. Так и не разобрались с полем.
                    # Поиск по паре, полю Mod - Modified/ TimeStamp в разрезе от startingtime до endingtime
                    LastValDict = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp': {'$gte': startingtime, '$lt': endingtime}}, {'Last': True}).limit(1)
                    #
                    pairmatcher = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp': {'$gte': startingtime, '$lt': endingtime}})
                    #
                    PrevDayDict = db[exchname].find({'PairName': secinner, 'Mod': False, 'TimeStamp': {'$gte': startingtime, '$lt': endingtime}}, {'PrevDay': True})
                    for subinLow in LowValDict:
                        LowestValue = subinLow['Low']
                    # Last
                    for subinLast in LastValDict:
                        LastValue = subinLast['Last']
                    # PrevDay
                    for subinPrevDay in PrevDayDict:
                        PrevDayValue = subinPrevDay['PrevDay']
                    #
                    for trdinner in pairmatcher:
                        if trdinner['High'] > HighestValue:
                            HighestValue = trdinner['High']
                        if trdinner['Low'] < LowestValue:
                            LowestValue = trdinner['Low']
                    tempdict = {'PairName': secinner, 'High': HighestValue,
                                'Low': LowestValue, 'TimeStamp': startingtime + tempdel, 'Last': LastValue,
                                'PrevDay': PrevDayValue, 'Aggregated': True}
                    db[exchname].insert(tempdict)
                    db[exchname].update({'PairName': secinner, 'Mod': False, 'TimeStamp':
                                        {'$gte': startingtime, '$lt': endingtime}}, {'$set':{'Mod': True}}, multi=True)
                    # Конец работы с циклом, переход на следующие 5 минут времени

                    startingtime = startingtime + delayActivation
                    mergingtime = mergingtime + delayActivation
                    print('if again')
                else:
                    print('Not enough data')
                    break
    print('Check DB....'+str(time.time()))


def Volumeaggregation():
    return None


def Tickaggregation():
    return None
