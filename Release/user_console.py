import socket
import threading
import sys
import time
import os

timerVar = False
ex = False

def timerFunc():
	global timerVar

	time.sleep(1)
	if not timerVar:
		print("")
		print(" The device is not responding!")
		timerVar = True


def UDPS():
	global ex
	global timerVar

	while not ex:
		print('')
		msg = input(' >  ')
		timerVar = False
		if msg == "close the console":
			ex = True
			os.abort()
			break
		else:
			UDP_IP = "127.0.0.1"
			UDP_PORT = 5006
			sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			sock.connect((UDP_IP, UDP_PORT))
			sock.send(str.encode(msg))
			sock.close()
			timer = threading.Thread(target=timerFunc, args=())
			timer.start()
			timer.join()
			while not timerVar:
				a = 1


def UDPL():
	global ex
	global timerVar

	UDP_PORT = 5008
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.bind(('', UDP_PORT))

	while not ex:
		data = sock.recv(1024)
		timerVar = True
		if "*" in str(data)[2:len(str(data)) - 1]:
			spl = str(data)[2:len(str(data)) - 1].split("*")
			stt = ""
			for i in range(len(spl)):
				stt = stt + "\n" + spl[i]

			print(stt)			
		else:
			print("")
			print(str(data)[2:len(str(data)) - 1])

print('')
print(' "close the console" - to close the console')

udpSender = threading.Thread(target=UDPS, args=())
udpListener = threading.Thread(target=UDPL, args=())
# timer = threading.Thread(target=timerFunc, args=())

udpSender.start()
udpListener.start()
udpSender.join()
udpListener.join()