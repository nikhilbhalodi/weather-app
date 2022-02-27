from tkinter import E
from django.shortcuts import render, HttpResponse
import pandas as pd
import numpy as np, pandas as pd
import requests
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64

def rainfall_data(request):
    url = 'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Rainfall/date/UK.txt'
    headers={'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    data = r.text
    new = {}
    last_list = []
    
    postString = data.split("\n",5)[5]
    new_list = postString.split()
    data = slice_per(new_list, 18)
    for i in data:
        new[i[0]] = [float(x.replace("-","0")) for x in i[1:]]
    
    year = new.pop('year')
    win = new.pop('win')
    spr = new.pop('spr')
    sum = new.pop('sum')
    aut = new.pop('aut')
    ann = new.pop('ann')
    A = new['jan']
    B = new['feb']
    C = new['mar']
    D = new['apr']
    E = new['may']
    F = new['jun']
    G = new['jul']
    H = new['aug']
    I = new['sep']
    J = new['oct']
    K = new['nov']
    L = new['dec']
    arrays = [year, A, B, C, D, E, F, G, H, I, J, K, L]
    max_length = 0
    for array in arrays:
        max_length = max(max_length, len(array))

    for array in arrays:
        array += [0] * (max_length - len(array))
    columns=['year','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    dfn = pd.DataFrame()
    same_size_dict = {}
    for i in range(len(arrays)):
        dfn[columns[i]] = np.array(arrays[i])
        same_size_dict[columns[i]] = arrays[i]
    df = pd.DataFrame(same_size_dict)
    df_last_5 = df.tail(5)
    dfn = df_last_5.set_index('year').T.to_dict('list')
    plt.plot(df.iloc[-3:])
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    

    return render(request,'rainfall.html',{'plot':graphic,'data':dfn})

def slice_per(source, step):
    return [source[i::step] for i in range(step)]