# -*- coding: utf-8 -*-
import random
import cv2
import numpy as np
from PIL import ImageTk, Image
from zhconv import convert

import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from ttkthemes import ThemedStyle
import tkinter.font as tkFont
from styleframe import StyleFrame, Styler

from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def s():
    global b
    b = tk.Label(root,text='')
    textExample.delete('1.0','end')
    f = [
        # 嘉義二間
        '4356631','1341116',
        # 基隆
        '1848064','1255518','5624512','2322910','1585209',
        # 宜蘭
        '71327915','1255974','974151','45834481','9240454',
        # 臺北
        '939406','987369','701275','735549','28474150','700650',
        # 新北
        '21928385','918259','4615249','52989876'
        # 桃園
        '45833283','5499753','1005671','1053774','1232994','1589935','3399433',
        # 新竹
        '1503986','890675',
        # 苗栗
        '970907','2987666','79449019','38935092','71418429','23157545','23695327',
        # 臺中
        '14797669','848364','1873433','19832813','36455990',
        # 彰化
        '50595268','48960316','6390139','1184104','6344585','41592658',
        # 南投
        '29966592','5996121','992741','1553364','19831026',
        # 雲林
        '983277','52759512','19832924',
        # 臺南
        '6903221','60937917','1185174','1284357',
        # 高雄
        '6485010','701684',
        # 臺東
        '4374352','64025693','7591713','5622467','1049551',
        # 花蓮八間
        '52971182','975470','3988492','1005221','64172625','5381766','3728533','29830472',
        # 屏東
        '57033211','6477235','4691193','5006764','3053980','5894633','3784159','1431968',
        # 金門
        '995191','1232669',
        # 澎湖六間
        '977831','15227150','5297733','41409315','77299688','5074044',
        ]
    # 使用內建的 urllib.request ，裡面有 urlopen 這個功能來送出網址
    no = str(random.choice(f))
    response = urlopen('https://hotels.ctrip.com/hotels/detail/?hotelId='+no)
    print(no)
    # 使用 beautuful soup 來解析網站回傳的 html response
    html = BeautifulSoup(response.read(),'lxml')
    '''
    讀取網路照片
    '''
    try:
        item = html.find('img',class_="detail-headalbum_bigpicImg").get('src')
        print('待處理網址： '+str(item))
        i="https:"+item
        print('正確網址： '+str(i))
        p = requests.get(i)
        print('狀態： '+str(p))
        print('\n')
        img = cv2.imdecode(np.frombuffer(p.content, np.uint8), 1)
        img = cv2.resize(img, (500, 250), interpolation=cv2.INTER_AREA)
        # cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        btc=Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=btc)
        b = tk.Label(image=imgtk,text='')
        b.pack()
        b.imgtk = imgtk
        b.configure(image = imgtk)
    except:
        b.configure(text = '暫無照片')
    name = html.find("h1", class_="detail-headline_name")
    name = name.get_text()
    name = convert(name, 'zh-tw')
    adr = html.find("span", class_="detail-headline_position_text").get_text()
    adr = convert(adr, 'zh-tw')
    nam_label.configure(text = name)
    adr_label.configure(text = adr)
    try:
        score = html.find("p", class_="detail-headreview_score")
        scor = score.get_text()
        scor_label.configure(text = scor)
    except:
        scor_label.configure(text = '暫無評分')
    try:
        c = html.find("span","detail-headreview_keyword")
        comme = c.get_text()
        comme = convert(comme, 'zh-tw')
        textExample.insert('end',comme)
    except:
        textExample.insert('end','暫無評論')
def op():
    b.destroy()
def oand():
    op()
    s()
def main():
    global root
    root = tk.Tk()
    onbutton = ttk.Button(root, text = "隨機投放",command = oand).pack(side=tk.TOP)

    name_frame = ttk.Frame(root)
    name_frame.pack(side=tk.TOP)
    name_label = ttk.Label(name_frame, text='旅店名稱：',font=(24))
    name_label.pack(side=tk.LEFT)
    global nam_label
    nam_label = ttk.Label(name_frame, text='',font=(24))
    nam_label.pack(side=tk.LEFT)
    
    adrr_frame = ttk.Frame(root)
    adrr_frame.pack(side=tk.TOP)
    adrr_label = ttk.Label(adrr_frame, text='旅店地址：',font=(24))
    adrr_label.pack(side=tk.LEFT)
    global adr_label
    adr_label = ttk.Label(adrr_frame, text='',font=(24))
    adr_label.pack(side=tk.LEFT)

    score_frame = ttk.Frame(root)
    score_frame.pack(side=tk.TOP)
    score_label = ttk.Label(score_frame, text='平均評分：',font=(24))
    score_label.pack(side=tk.LEFT)
    global scor_label
    scor_label = ttk.Label(score_frame, text='',font=(24))
    scor_label.pack(side=tk.LEFT)

    comment_frame = ttk.Frame(root)
    comment_frame.pack(side=tk.TOP)
    comment_label = ttk.Label(comment_frame, text='最具代表評論：',font=(24))
    comment_label.pack(side=tk.LEFT)

    global textExample
    textExample=tk.Text(root, height=18)
    textExample.configure(font=('',16,"bold"))
    textExample.pack()
    
    global b
    b = tk.Label(root)

    root.mainloop()
if __name__=='__main__':
    main()