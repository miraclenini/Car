import requests
import re
import pandas as pd
import pygal

def htmlget(url):

    r = requests.get(url,timeout = 30)
    r.raise_for_status()
    r.encoding = r.apparent_encoding




    name = re.findall('<img alt="(.*?)" ',r.text,re.S)
    money = re.findall('class="col1">(.*?)</a></p>',r.text,re.S)
    paizi = re.findall('<p>品　牌：<a href="//www.58che.com/brand/(.*?)/" class="col2">(.*?)</a></p>',r.text,re.S)
    Enname = []
    Chname = []
    for pai in paizi:

        Enname.append(pai[0])
        Chname.append(pai[1])


    level = re.findall('<p>级　别：<a href="/series/l9.html">(.*?)</a></p>',r.text,re.S)
    fouce = re.findall('<p><strong>(.*?)</strong><span>人关注该车</span></p>',r.text,re.S)


    _data = pd.DataFrame()


    _data['名字'] = name
    _data['指导价'] = money
    _data['品牌名(英文)'] = Enname
    _data['品牌名(中文)'] = Chname

    _data['级别'] = level
    _data['关注人数'] = fouce


    data = pd.concat([_data]).reset_index(drop=True)
    data.to_csv('che',index=False,encoding = 'utf-8')

    data = pd.read_csv(r'C:\Users\Administrator\PycharmProjects\untitled1\che')
    dates = data['名字']

    lows = data['品牌名(中文)']

    hist = pygal.Bar()

    hist.title = '高级轿车关注人数'
    hist.x_labels = name
    hist.x_title = '名字'
    hist.y_title = '关注人数'

    numbers = [int(x) for x in fouce]

    hist.add('Car', numbers)
    hist.render_to_file('diee.svg')

htmlget("https://car.58che.com/level/9.html")