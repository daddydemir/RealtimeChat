from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject , QThread , pyqtSignal
from PyQt5.Qt import Qt
import sys
import time
import socket
from _thread import * 
#import threading

sayi = 10


class sayfa(QWidget):
	def __init__(self , port=7777 , nameD="demir" , oda_ismi="room"):
		super().__init__()
		self.bt = True
		self.port1 = int(port); self.n1 =nameD
		#aktifListe = []
		self.odaName = ["Plevne" , "GOP" , "Software"]
		self.odaPort = [7777 , 8888 , 9999]

		self.liste = QListWidget()
		self.listeMesaj = QListWidget()

		self.s = socket.socket()
		try:
			self.s.connect(("2.59.117.44" , self.port1))
			self.s.send(str.encode(self.n1)) # isim gönderiliyor 
			print(port , "'a bağlandı ")
			start_new_thread(self.metot , ())
		except socket.error as e:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setText("Sunucuya bağlanamadı . \nLütfen daha sonra tekrar deneyiniz .")
			msg.setWindowTitle("Error 404")
			msg.exec_()
			pass

		File = open("stil.qss" , "r")
		with File:
			qss = File.read()
			self.setStyleSheet(qss)

		self.setWindowTitle("daddydemir")
		self.setMinimumSize(900,500)
		self.anaLayout = QVBoxLayout()

		self.layoutUst = QHBoxLayout()
		self.name = QLabel("@user")
		self.room = QLabel(oda_ismi)
		self.combo = QComboBox()
		
		for i in self.odaName:
			self.combo.addItem(i)


		self.layoutUst.addWidget(self.name , 1)
		self.layoutUst.addWidget(self.room , 1)
		self.layoutUst.addWidget(self.combo)

		self.anaLayout.addLayout(self.layoutUst)
		
		# ilk layout tamamlandı 

		self.layout2 = QHBoxLayout() # mesaj alanı ve aktif kullanıcılar bölümünü tutacak 
		self.layoutMesaj = QVBoxLayout() #mesajları ve mesaj gönderme kısmını tutacak 
		#self.listeMesaj = QListWidget()

		self.layoutMesaj.addWidget(self.listeMesaj)
		print()

		# mesaj alma kısmı bitti 
		

		self.layoutAlt = QHBoxLayout()
		self.mesajYaz = QLineEdit()
		self.mesajYaz.setPlaceholderText("Mesaj Yaz :)")
		self.layoutAlt.addWidget(self.mesajYaz , 1)
		self.mesajYaz.setFixedHeight(50)

		self.mesajGonder = QPushButton("GÖNDER")

		self.mesajGonder.clicked.connect(self.sendMessage)
		self.layoutAlt.addWidget(self.mesajGonder)
		self.mesajGonder.setFixedHeight(50)

		self.layoutMesaj.addLayout(self.layoutAlt)
		self.layout2.addLayout(self.layoutMesaj,1)

		# Mesaj alanı tamamen bitti 

		self.layoutSol = QVBoxLayout() # aktif kullanıcılar burada olacak 


		self.layoutSol.addWidget(QLabel("AKTİF KULLANICILAR"))
		self.layoutSol.addWidget(self.liste)
		self.layout2.addLayout(self.layoutSol)
		self.anaLayout.addLayout(self.layout2)

		self.setLayout(self.anaLayout)
		self.combo.currentIndexChanged.connect(self.odaSec)
		
		

		#start_new_thread(self.metot , ())
		k="@"+nameD
		self.name.setText(k)


	def metot(self):
		while True:
			try:
				gelenMsg = self.s.recv(2048)
				gelenMsg = gelenMsg.decode("utf-8")
				if(gelenMsg[0] == "~"):
					self.liste.clear()
					self.aktifListe = []
					tut = ""
					for i in gelenMsg:
					    if(i == "~"):
					        if(tut != ""):
					            self.aktifListe.append(tut)
					        tut = ""
					        continue
					    tut += i
					for i in self.aktifListe:
					    QListWidgetItem(i , self.liste)
					continue

				QListWidgetItem(gelenMsg , self.listeMesaj)
				self.listeMesaj.scrollToBottom()
			except socket.error as e:
				#print(e)
				msg = QMessageBox()
				msg.setText("Mesaj içeriği")
				msg.setWindowTitle("HATA 404")

				pass
			
	def odaSec(self , odaNumarasi):
		#self.liste.clear()
		print("ok ")
		'''
		if(self.bt):
			self.bt = False
			return 0
		'''
		self.s = socket.socket()
		
		print("1 kez çalıştı : ", self.odaPort[odaNumarasi])
		try:
			self.s.connect(("2.59.117.44" , self.odaPort[odaNumarasi]))
			self.s.send(str.encode(self.n1)) # isim gönderiliyor 
		except socket.error as e:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setText("<strong>Bu oda şu anda kullanılamıyor .</strong><br><strong>Daha sonra tekrar deneyebilrsiniz .</strong> <br>İlerişim adresleri <br><a style='text-decoration:none; color:#921cb1;' href='mailto:mehmetcakmaktasi47@gmail.com'>mail</a> <br> <a style='text-decoration:none; color:#921cb1;' href='https://t.me/demiron'> telegram </a> ")
			msg.setWindowTitle("Error 404")
			msg.exec_()
			print("hata 141")
			self.combo.setCurrentIndex(0)
			return 0
		self.listeMesaj.clear()
		#print(odaNumarasi)
		self.room.setText(self.odaName[odaNumarasi])
		
		start_new_thread(self.metot , ())
		#
	# Thread function 

	def sendMessage(self):
		mesaj = self.mesajYaz.text()
		mesaj = mesaj.strip()
		if(mesaj == "/clear"):
			self.listeMesaj.clear()
			self.mesajYaz.setText("")
			return 0
		if(mesaj == "/clear_user"):
			self.liste.clear()
			for i in self.aktifListe:
				QListWidgetItem(i , self.liste)
			self.mesajYaz.setText("")
			return 0
		self.mesajYaz.setText("")
		tempMesaj = ""
		for i in mesaj:
			if(i == "~"):
				return 0

		try:
			self.s.send(str.encode(mesaj))
		except socket.error as e:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText("Sunucu bağlantısında hata var . ")
			msg.setWindowTitle("Error 404")
			#msg.setStandardButtons(QMessageBox.Ok)
			retval = msg.exec_()

	def keyPressEvent(self , event):
		#print(event.key())
		if(event.key() == 16777220 ):
			self.sendMessage()




#app = QApplication(sys.argv)
#pencere = sayfa()
#pencere.show()
#app.exec_()


