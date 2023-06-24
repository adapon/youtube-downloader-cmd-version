import os
import tkinter as tk
import subprocess
from PIL import ImageTk,Image
from tkinter.constants import CENTER
from tkinter.constants import *
from functools import partial
from random import shuffle
window=tk.Tk()
window.title("yt-dlp-gui")
window.resizable(False,False)

##物件事件
def mp3():
    global current_path,url
    lab_text.set("任務進程在此顯示")
    lab_text.set("下載當中...")
    url=ent.get()
    # print(url)
    a=subprocess.Popen(f"cd {current_path}",shell=True)
    url="youtube-dl --extract-audio --audio-format mp3 "+url+' --external-downloader aria2c --external-downloader-args "-x 16 -k 20M"'
    a=subprocess.Popen(url
                       ,shell=True
                       ,stdout=subprocess.PIPE
                       ,stderr=subprocess.STDOUT)
    while True:
        cmd_reg=a.stdout.readline()
        print(cmd_reg.decode("utf-8").strip("b'"))
        if a.poll()==0:
            lab_text.set("下載完畢")
            a.stdout.close()
            break
    
def mp4():
    lab_text.set("任務進程在此顯示")
    lab_text.set("下載當中...")
    url=ent.get()
    a=os.popen(f"cd {current_path}")
    a=os.popen(f"youtube-dl -F {url}")
    cmd_reg=a.read()
    for i in cmd_reg.split("\n"):
        cmd_content.append(i)
    a.close()
    del cmd_content[0:2]
    cmd_content.pop()
    for i in range(0,len(cmd_content)):
        cmd_content[i]=cmd_content[i].split(" ")
    for i in range(len(cmd_content)):##清除空元素
        reg=[]
        reg=cmd_content[i]
        cmd_content[i]=list(filter(None,reg))
    for i in range(len(cmd_content)):
        cmd_content[i][len(cmd_content[i])-1]=cmd_content[i][len(cmd_content[i])-1][:-3]
        if cmd_content[i].count("audio")!=0:##只抓音檔
            audio=cmd_content[i]
        if cmd_content[i].count("video")!=0:
            video=cmd_content[i]
    print(audio)
    print(video)
    for i in range(len(cmd_content)):##輸出
        for j in range(len(cmd_content[i])):
            print(cmd_content[i][j],end="|")
        print()
    url="youtube-dl -f "+video[0]+"+"+audio[0]+"/"+video[1]+"+"+audio[1]+" "+url
    url+=' --external-downloader aria2c --external-downloader-args "-x 16 -k 20M"'
    # print(url)
    a=subprocess.Popen(f"cd {current_path}",shell=True)
    a=subprocess.Popen(url
                       ,shell=True
                       ,stdout=subprocess.PIPE
                       ,stderr=subprocess.STDOUT)
    while True:
        cmd_reg=a.stdout.readline()
        print(cmd_reg.decode("utf-8").strip("b'"))
        if a.poll()==0:
            lab_text.set("下載完畢")
            a.stdout.close()
            break
def sub():
    print()
##

##物件設定
button_list=[]
button_text=["僅下載mp3","下載影片","下載字幕"]
button_event=[mp3,mp4,sub]
ent_text=tk.StringVar()
lab_text=tk.StringVar()
ent_text.set("請在此輸入url")
lab_text.set("任務進程在此顯示")
for i in range(3):
        b=tk.Button(window,text=button_text[i],command=button_event[i])
        button_list.append(b)
        b.grid(row=1,column=i)
ent=tk.Entry(window,textvariable=ent_text,justify=(CENTER))
ent.grid(row=0,column=0,columnspan=3)
lab=tk.Label(window,textvariable=lab_text,font=("Arial",20))
lab.grid(row=2,column=0,columnspan=3)
def ent_click(event):#點擊滑鼠左鍵時移除預設文字
    ent_text.set("")
ent.bind("<Button-1>",ent_click)

##

##main
cmd_content=[]
current_path=os.path.abspath(os.getcwd())

##

window.mainloop()