import socket 
from _thread import *

userlist = [] # username
passlist = []

host = "2.59.117.44"
port = 5566 
s = socket.socket()

try:
	s.bind((host , port))
	s.listen()
except:
	pass
	# muhtemelen port adresi başka bir uygulama tarafından kullanılıyordur 

# dinleme işlemini başlattık 

def parser(kelime):
	isim = ""; sifre = ""
	sayac = 0
	for i in kelime:
		if(i != "@"):
			sayac += 1
			isim += i
		if(i == "@"):
			sifre = kelime[sayac+1 : len(kelime)]
			break
	return isim , sifre 

def yeniKayit(kelime):
	isim = ""; sifre=""
	sayac = 0
	for i in kelime:
		if(i == "#"):
			continue
		if(i != "@"):
			sayac += 1
			isim += i
		if(i == "@"):
			sifre = kelime[sayac+2 : len(kelime)]
			break 
	tut = 0
	for i in userlist:
		if(i != isim):
			tut += 1
		if(i == isim):
			return "~" # bu kullanıcı adını kullanamazsınız
	if(tut == len(userlist)):
		f = open(r"users/user.txt" , "a" , encoding="utf-8")
		f.write(isim.strip())
		f.write("\n"); f.close()
		w = open(r"users/passwd.txt" , "a" , encoding="utf-8")
		w.write(sifre.strip())
		w.write("\n"); w.close()
		userlist.append(isim.strip())
		passlist.append(sifre.strip())
		return "$" # kullanıcı başarıyla oluşturuldu  

def broadCast(kullanici , number):
	kullanici.send(str.encode("Demirin Sunucusuna Hoşgeldin . "))
	gelen1 = kullanici.recv(1024) # isim@sifre geldi 
	gelen1 = gelen1.decode("utf-8")
	ilk = gelen1[0]
	if(ilk != "#"):
		name1 , pass1 = parser(gelen1)
	elif(ilk == "#"):
		msg = yeniKayit(gelen1)
		kullanici.send(str.encode(msg))
		return 0
	# isim ve şifre kontrolü 
	ifade = ""; b_sayac = 0

	for i in range(len(userlist)):
		if(userlist[i] == name1 and passlist[i] == pass1):
			#oturum açma başarılı
			ifade = "True"
			break
		elif(userlist[i] == name1 and passlist[i] != pass1):
			# şifre hatalı 
			ifade = "Şifre hatalı"
			break
		elif(userlist[i] != name1):
			# kullanıcı yok 
			b_sayac += 1
	if(b_sayac == len(userlist)):
		# kullanıcı yok 
		ifade = "Kullanıcı bulunamadı ."
	kullanici.send(str.encode(ifade))
	# mesaj gönderildi 
	odalar = []
	oda = ""
	try:
		f = open(r"rooms/rooms.txt" , "r" , encoding="utf-8")
		for line in f:
			odalar.append(line.strip())
		f.close()
		for i in range(len(odalar)):
			oda += odalar[i]
			if(i == len(odalar)-1):
				break
			oda += ","
	except:
		# dosyayı bulamıyor
		print("hata aldım")
		pass
	# oturum açma başarılıysa oda portlarını gönder 
	if(ifade == "True"):
		kullanici.send(str.encode(oda))



# fonksiyonun sonu 

f = open(r"users/user.txt" , "r" , encoding="utf-8")
for line in f:
	userlist.append(line.strip())
f.close()
w = open(r"users/passwd.txt" , "r" , encoding="utf-8")
for line in w:
	passlist.append(line.strip())
w.close()



while True:
	istemci , iport = s.accept() # bağlantı isteği kabul edildi 
	print(iport[1] , " bağlandı .")
	start_new_thread(broadCast , (istemci , iport[1] , ))


# https://github.com/daddydemir
