from threading import Thread
from django.http import HttpResponse
from django.shortcuts import render
from yahoo_fin.stock_info import *
import time
import queue
# Create your views here.
def stockPicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request,'main/stockpicker.html',context={'stockpicker':stock_picker })

def stockTracker(request):
    stockpicker = request.GET.getlist('stockpicker')
    print(stockpicker)
    data = {}
    available_stocker = tickers_nifty50()
    for i in stockpicker:
        if i in available_stocker:
            pass
        else:
            return HttpResponse('Error')
    
    n_threads = len(stockpicker)
    print(n_threads)
    thread_list = []
    que = queue.Queue()
    start = time.time()
    print(start)

    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]:get_quote_table(arg1)}),args=(que,stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)

    # for i in stockpicker:
    #     details = get_quote_table(i)
    #     data.update({i:details})    
    
    end=time.time()
    print(end)
    print("Time taken",end-start)
    print(data)
    return render(request,'main/stocktracker.html',context={'data':data})