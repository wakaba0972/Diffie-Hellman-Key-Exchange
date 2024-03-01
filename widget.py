import tkinter as tk
from time import time
from big_prime import *
from threading import Thread
from random import randint, getrandbits

class XOR:
    def Encrypt(self,message):
        secret= self.secret% 0x110000
        cipher=''
        for char in message: cipher+=chr(ord(char)^secret)
        self.write('\n'+self.string+'共同金鑰 mod 0x10FFFF為 '+str(secret)+'\n'+
                   self.name+'發送密文，對每個字元 XOR '+str(secret)+' 加密後得:\n>>>> '+cipher+'\n')
        return cipher
        
    def Decrypt(self,cipher):
        secret= self.secret% 0x110000
        message=''
        for char in cipher: message+=chr(ord(char)^secret)
        self.write('\n'+self.string+'共同金鑰 mod 0x10FFFF為 '+str(secret)+'\n'+
                   self.name+'接收密文，對每個字元 XOR '+str(secret)+' 解密後得:\n>>>> '+message+'\n')
        return message
    
class People(XOR):
    def __init__(self,master,name,**grid):
        self.frame= tk.LabelFrame(master.frame,text=name,font=("Arial",25))
        self.frame.grid(**grid)
        self.master= master
        self.string=''
        self.name= name
        self.key=None
        self.secret= None
        self.message_box= tk.Text(self.frame,
                              width=70,
                              height=30,
                              font=("Courier",15,"italic"))
        
        self.Input_box= tk.Text(self.frame,
                            state='disabled',
                            width=70,
                            height=5,
                            font=("Courier",15,"italic"))
       
        self.message_box.grid(row=0,column=0)
        self.Input_box.grid(row=1,column=0)
        self.Input_box.bind('<Return>',self.send)

    def materal(self):
        return pow(self.master.num,self.key,self.master.prime)

    def send(self,event):
        message= self.Input_box.get('1.0','end-1c').strip()
        self.Input_box.delete('1.0','end+1c')
        if len(message)>150: self.write('\n訊息長度不得超過150!\n'); return
        self.master.send(self.name,message)

    def receive(self,cipher):
        message= self.Decrypt(cipher)

    def write(self,string):
        self.index=0
        self.string=string
        self.length=len(string)
        self.s= self.message_box.after(5,self.anime)

    def anime(self):
        if self.index==self.length:
            self.message_box.after_cancel(self.s)
            return
        self.message_box.insert(tk.END,self.string[self.index])
        self.index+=1; self.s= self.message_box.after(3,self.anime)
        self.message_box.see('end')
        
class Cauculate_box:
    def __init__(self,master,**grid):
        self.frame= tk.LabelFrame(master)
        self.frame.grid(**grid)
        self.prime= None
        self.num= None
        self.Alice= People(self,'Alice',row=0,column=0)
        self.Bob= People(self,'Bob',row=0,column=1)

    def start(self):
        gen= Thread(target=self.DH_exchange)
        gen.start()

    def DH_exchange(self):
        self.Alice.message_box.delete('1.0','end')
        self.Bob.message_box.delete('1.0','end')
        self.Alice.message_box.insert('end','生成金鑰中... ')
        self.Bob.message_box.insert('end','生成金鑰中...  ')
        start= time()
        self.Alice.key= getrandbits(1024)
        self.Bob.key= getrandbits(1024)
        self.num= getrandbits(1024)
        self.prime= Bprime(1024)
        t= time()-start
        am=self.Alice.materal()
        bm=self.Bob.materal()
        self.Alice.secret=pow(bm, self.Alice.key, self.prime)
        self.Bob.secret=pow(am, self.Bob.key, self.prime)

        self.Alice.write('約耗時'+str(int(t))+'秒\nAlice取得公鑰p:\n>>>> '+str(self.prime)+'\n\n'+
                         'Alice取得公鑰g:\n>>>> '+str(self.num)+'\n\n'+
                         'Alice生成私鑰x:\n>>>> '+str(self.Alice.key)+'\n\n'+
                         'Alice計算g^x mod p:\n>>>> '+str(am)+'\n\n'+
                         'Alice計算(g^y mod p)^x得出共同金鑰:\n>>>> '+str(self.Alice.secret)+'\n\n'+
                         '請輸入訊息')

        self.Bob.write('約耗時'+str(int(t))+'秒\nBob取得公鑰p:\n>>>> '+str(self.prime)+'\n\n'+
                       'Bob取得公鑰g:\n>>>> '+str(self.num)+'\n\n'+
                       'Bob生成私鑰y:\n>>>> '+str(self.Bob.key)+'\n\n'+
                       'Bob計算g^y mod p:\n>>>> '+str(bm)+'\n\n'+
                       'Bob計算(g^x mod p)^y得出共同金鑰:\n>>>> '+str(self.Bob.secret)+'\n\n'+
                       '請輸入訊息')
        
        self.Alice.Input_box['state']=tk.NORMAL
        self.Bob.Input_box['state']=tk.NORMAL
    
    def send(self,sender,message):
        
        self.Alice.string=self.Bob.string=''
        self.Alice.message_box.delete('1.0','end')
        self.Bob.message_box.delete('1.0','end')
        
        if sender=='Alice':
            cipher= self.Alice.Encrypt(message)
            self.Bob.receive(cipher)
        else:
            cipher= self.Bob.Encrypt(message)
            self.Alice.receive(cipher)

        
        
        
        
 
