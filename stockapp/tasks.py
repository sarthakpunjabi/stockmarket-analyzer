from celery import shared_task
from yahoo_fin.stock_info import *
from threading import Thread
import queue

@shared_task(bind = True)
def update_stock(self,stockpicker):
    data = {}
    available_stocker = tickers_nifty50()
    for i in stockpicker:
        if i in available_stocker:
            pass
        else:
            stockpicker.remove(i)
    
    n_threads = len(stockpicker)
    print(n_threads)
    thread_list = []
    que = queue.Queue()
    
    

    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]:get_quote_table(arg1)}),args=(que,stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)
        
    return 'Done'
    

