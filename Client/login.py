from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton , QWidget , QGridLayout , QLabel , QLineEdit , QCheckBox , QMessageBox , QDialog , QComboBox
from PyQt5.QtGui import *
import sys
import time
import socket
import main_gui

sayi = 0

class odaSec(QWidget):
    def __init__(self , odaName="plevne ,  4444 , deneme , 5555 , sanalSunucu , 1111 , demir , 3691" , username="userCharon"):
        super().__init__()

        
        self.ku_ismi = username

        File = open("stil.qss" , "r")
        with File:
            qss = File.read()
            self.setStyleSheet(qss)

        self.roomsName = [] # oda ismi 
        self.roomsPort = [] # oda port numarası
        self.odaName(odaName)

        self.setWindowTitle("Odalar")
        self.setFixedSize(400,200)

        self.layout = QGridLayout()
        self.odalar = QComboBox()
        for i in self.roomsName:
            self.odalar.addItem(i)

        self.btnKatil = QPushButton("Katıl")
        self.btnKatil.clicked.connect(self.katil)

        self.layout.addWidget(QLabel("Katılmak istediğiniz \nodayı seçin") , 0 , 0)
        self.layout.addWidget(self.odalar , 1 , 0 )
        self.layout.addWidget(self.btnKatil, 1 , 1)

        self.setLayout(self.layout)

    def katil(self):
        index = self.odalar.currentIndex()
        #print(index)
        print(self.roomsPort[index])
        self.AnaPencere = main_gui.sayfa(port=self.roomsPort[index] , nameD=self.ku_ismi , oda_ismi=self.odalar.currentText())
        self.AnaPencere.show()
        self.hide()


    def odaName(self , odalar):
        # oda isimleri sunucudan 1 mesaj olarak geliyor bunu parse etmeliyim 
        # gelen mesaj : [odaismi,port][odaismi,port]
        liste = odalar.split(",")
        for i in range(len(liste)):
            if(i %2 == 0):
                self.roomsName.append(liste[i].strip())
            else:
                self.roomsPort.append(liste[i].strip())


class ekran(QWidget):
  def __init__(self , isim , sifre):
    super().__init__()
    File = open("stil.qss" , "r")
    with File:
        qss = File.read()
        self.setStyleSheet(qss)

    self.setWindowTitle("Kayıt ol")
    self.setFixedSize(500,200)

    self.layout = QGridLayout()

    self.lbl2 = QLabel("Yeni Kullancı\nOluştur")
    self.lbl2.setStyleSheet("font-size:14pt; color:red;")

    self.kul = QLabel("Kullanıcı Adı:")
    self.kul.setStyleSheet("font-size:10pt;")
    self.lbl0 = QLineEdit(isim)
    self.lbl0.setStyleSheet("font-size:10pt;")

    self.pas = QLabel("Parola :")
    self.pas.setStyleSheet("font-size:10pt;")
    self.lbl1 = QLineEdit(sifre)
    self.lbl1.setStyleSheet("font-size:10pt;")
    self.btnKayit = QPushButton("Kayıt ol")
    self.btnKayit.setStyleSheet("font-size:10pt;")
    self.btnKayit.clicked.connect(self.yeniKayit)

    self.layout.addWidget(self.lbl0 , 1 , 1)
    self.layout.addWidget(self.kul , 1, 0)
    self.layout.addWidget(self.lbl1 , 2 , 1)
    self.layout.addWidget(self.pas , 2, 0)
    self.layout.addWidget(self.lbl2 , 0 , 1)
    self.layout.addWidget(self.btnKayit , 3 , 2)

    self.setLayout(self.layout)

  def yeniKayit(self):
      isim = self.lbl0.text().strip(); sifre = self.lbl1.text().strip()
      self.w1 = AnaEkran()
      if(isim == "" or sifre == ""):
          self.w1.mesajKutusu("e" , "HATA" , "Lüften boş alan bırakmayınız !")
          pass
      elif(len(sifre) < 8):
          self.w1.mesajKutusu("w" , "HATA" , "Şifreniz en az 8 karakter olmalıdır !")
          pass
      baglanti = socket.socket()
      baglanti.connect(("2.59.117.44" , 5566))
      s1 = "#"+isim+"@"+sifre
      baglanti.send(str.encode(s1))
      gelen0 = baglanti.recv(1024) # demirin sunucusun ahoşgeldin mesajı 
      #print(gelen0.decode('utf-8'))
      gelen = baglanti.recv(1024)
      gelen = gelen.decode("utf-8")
      print(gelen)
      if(gelen[0] == "~"):
          self.w1.mesajKutusu("e" , "HATA" , "Bu kullanıcı adını kullanamazsınız !")
      elif(gelen[0] == "$"):
          self.w1.mesajKutusu("i" , "BAŞARILI" , "Başarı ile kaydoldunuz . ")
      pass

# SOME PROBLEMS

class AnaEkran(QWidget):

  def __init__(self):
    super().__init__()

    File = open("stil.qss" , "r")
    with File:
        qss = File.read()
        self.setStyleSheet(qss)

    self.setWindowTitle("Giriş yap / Kayıt ol")
    self.setFixedSize(500,200)
    self.Alayout = QGridLayout()
    self.nicklbl = QLabel("Kullanıcı Adı : ")
    self.nicklbl.setStyleSheet("font-size:12pt;")
    self.passlbl = QLabel("Parola  : ")
    self.passlbl.setStyleSheet("font-size:12pt;")
    self.remember = QCheckBox("Beni Hatırla")
    self.remember.setStyleSheet("font-size:12pt;")

    self.namelbl = QLineEdit()
    self.namelbl.setStyleSheet("font-size:12pt;")
    self.paswlbl = QLineEdit()
    self.paswlbl.setEchoMode(QLineEdit.Password)
    self.paswlbl.setStyleSheet("font-size:12pt;")
    self.btnkayit = QPushButton("Gönder")
    self.btnkayit.setStyleSheet("font-size:12pt;")
    self.btnkayit.clicked.connect(self.kayit)

    self.Alayout.addWidget(self.nicklbl , 1 , 0)
    self.Alayout.addWidget(self.passlbl , 2 , 0)
    self.Alayout.addWidget(self.remember , 3 , 1)
    self.Alayout.addWidget(self.namelbl , 1 , 1)
    self.Alayout.addWidget(self.paswlbl , 2 , 1)
    self.Alayout.addWidget(self.btnkayit , 3 , 2)

    self.oku()
    self.setLayout(self.Alayout)

  def kayit(self):
    b1 = True
    isim = self.namelbl.text(); sifre = self.paswlbl.text()
    if(isim == "" or sifre == ""):
        self.mesajKutusu("e", "HATA" , "Lütfen boş alan bırakmayınız !")
        b1 = False
    elif(len(sifre) < 8):
        self.mesajKutusu("w" , "HATA" , "Şifreniz en az 8 karakter olmalıdır !")
        b1 = False
    try:
        f = open("set.txt" , "w" , encoding='utf-8')
        f.write(isim.strip())
        f.write("\n")
        f.write(sifre.strip())
        f.write("\n")
        if(self.remember.isChecked() == True):
            f.write("1")
        else:
            f.write("0")
        f.close()
    except:
        pass
        # dosya yazma kısmında hata olursa programın kapanmaması için 
    s1 = isim.strip()+"@"+sifre.strip()
    if(b1):
        # bağlanalım ...
        baglanti = socket.socket()
        try:
            baglanti.connect(("2.59.117.44", 5566))
        except:
            # bağlantı hatası
            self.mesajKutusu("e","HATA","Şu anda sunucuya ulaşılamıyor \nDaha sonra tekrar deneyin .")
            return 0
        baglanti.send(str.encode(s1)) # isim ve şifreyi gönder
        resp1 = baglanti.recv(1024)
        msg1 = resp1.decode("utf-8") # demirin sunucusuna hoşgeldin 
        print("1. gelen : ",msg1)
        resp2 = baglanti.recv(1024)
        msg2 = resp2.decode("utf-8")
        print("2. gelen : ",msg2)
        if(msg2 == "True"):
            # oturum açma başarılı
            # sunucu oda ismini göndermeli 
            #baglanti.send(str.encode("p"))
            resp3 = baglanti.recv(1024)
            msg3 = resp3.decode("utf-8")
            print("3. gelen : ",msg3)
            #self.mesajKutusu("i" , isim.strip() , "Oturum açma başarılı .")
            self.w2 = odaSec(msg3 , isim)
            self.w2.show()
            global pencere
            pencere.hide()
        elif(msg2 == "Şifre hatalı"):
            self.mesajKutusu("w" , "HATA" , "Girdiğiniz şifre yanlıştı , lütfen tekrar deneyin .")
        elif(msg2 == "Kullanıcı bulunamadı ."):
            self.mesajKutusu("e" , isim.strip() , "Bu isimde bir kullancı yok ! \nYeni kullanıcı oluşturmak ister misin ?" , "yn")


  def mesajKutusu(self , tip , baslik , icerik , buton=None):
    msg = QMessageBox()
    if(tip == "w"):
        msg.setIcon(QMessageBox.Warning) # uyarı 
    elif(tip == "e"):
        msg.setIcon(QMessageBox.Critical) # hata 
    elif(tip == "i"):
        msg.setIcon(QMessageBox.Information) # bilgi 
    msg.setText(icerik)
    msg.setWindowTitle(baslik)
    msg.setStandardButtons(QMessageBox.Ok)
    if(buton == "yn"):
        isim = self.namelbl.text(); sifre = self.paswlbl.text()
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No )
    retval = msg.exec()
    if(retval == QMessageBox.Yes):
        self.w1 = ekran(isim.strip() , sifre.strip())
        self.w1.show()
    if(retval == QMessageBox.No):
        pass


  def oku(self):
    try:
        f = open("set.txt" , "r" , encoding='utf-8')
    except:
        # dosyayı oluşturalım 
        f = open("set.txt" , "x" , encoding='utf-8')
        return None
    content = []
    for line in f:
        content.append(line.strip())
    f.close()
    try:
        if(int(content[2]) == 1):
            self.remember.setChecked(True)
            self.namelbl.setText(content[0]); self.paswlbl.setText(content[1])
    except:
        # dosya istenilen formatta değilse  
        pass

# ana ekranı kodla
app = QApplication(sys.argv)
pencere = AnaEkran()
pencere.show()
app.exec_()
