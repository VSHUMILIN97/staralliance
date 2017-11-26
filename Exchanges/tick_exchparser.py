# from Exchanges.BittrexObjCreate import api_get_getmarkethistory, api_get_getticker, api_get_getmarketsummaries
# from Exchanges.models import BittrexOHLC
# from Exchanges.models import BittrexTick
# from Exchanges.models import BittrexVolume
# django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet. ??? Не работает
import random
import time
import asyncio
import django


#Реально работает, но вызывает ошибку если пытаться вызывать методы =) Ошибка выше
async def RandomSeed():
    while 1:
        try:
            timeTemp = random.uniform(5, 8.5) #Значения можно менять
            print(timeTemp)
            #api_get_getmarketsummaries()
            #api_get_getmarkethistory()
            #api_get_getticker()
            await asyncio.sleep(timeTemp)
        except:
          print('Overflow error in tick_exchparser')

def SeedCall():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(RandomSeed())
