# -*- coding: utf-8 -*-
import socket
from _thread import *
import time

userList  = {} # ip adresi : isim
clientLis = [] # client
aktifKullanicilar = [] # name
aktifler = ""

host = "2.59.117.44"
port = 7777

s = socket.socket()

try:
    s.bind((host,port))
    s.listen()
except:
    print("hata - line 12")


def multicast(k1 , numara):
    global aktifler
    name = k1.recv(1024)
    userList[numara] = name.decode("utf-8")
    aktifKullanicilar.append(name.decode("utf-8"))
    aktifler = ""
    for i in aktifKullanicilar:
        aktifler += "~"+i
    aktifler += "~"
    for i in clientLis:
        i.send(aktifler.encode())

    while True:
        try:
            gelenMesaj = k1.recv(2048)
            gelenMesaj = gelenMesaj.decode('utf-8')
            if(gelenMesaj == "/list"):
                for i in aktifKullanicilar:
                    i = "@"+i
                    k1.send(i.encode())
                time.sleep(2)
                for i in clientLis:
                    i.send(aktifler.encode())
                continue

            gelenMesaj = userList[numara] +" >>> " + gelenMesaj

            for i in clientLis:
                i.send(gelenMesaj.encode())
        except:
            clientLis.remove(k1)
            aktifKullanicilar.remove(userList[numara])
            aktifler = ""
            for i in aktifKullanicilar:
                aktifler += "~"+i
            aktifler += "~"
            for i in clientLis:
                i.send(aktifler.encode())
            break


while True:
    kullanici , portNo = s.accept() # bağlantı istekleri kabul ediliyor
    clientLis.append(kullanici)
    print("Kim bağlandı : " , portNo[1])
    start_new_thread(multicast , (kullanici , portNo[1] , ))
