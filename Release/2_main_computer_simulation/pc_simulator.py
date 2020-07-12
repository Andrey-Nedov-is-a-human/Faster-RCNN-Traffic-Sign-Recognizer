import socket
import threading
import sys
import time
import os
import socket

LISTEN_TO_PC_PORT = 5005

TCP_IP = "127.0.0.1"
TCP_PORT = LISTEN_TO_PC_PORT
address_to_server = (TCP_IP, TCP_PORT)

while True:
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(address_to_server)
	a = input()
	client.send(bytes(a, encoding='UTF-8'))

	if a == "stp":
		break

	elif a == "ping":
		data = client.recv(1024)
		dataParse = str(data)[2:len(str(data)) - 1]
		print(dataParse)

	elif a == "last":
		data = client.recv(1024)
		with open('anns.json', 'wb') as f:
		    print('file opened')
		    while data:
		        print('receiving data...')
		        print('data=%s', (data))
		        f.write(data)
		        data = client.recv(1024)

		f.close()
		print('Successfully get the file')
		print('connection closed')

	elif a == "next":
		data = client.recv(1024)
		dataParse = str(data)[2:len(str(data)) - 1]
		print(dataParse)
		if dataParse == "yes":
			print("She sad yes!")
			f = open("image.jpg", "rb")
			l = f.read(1024)
			while(l):
				client.send(l)
				l = f.read(1024)
			f.close()

			# with open('anns.json', 'wb') as f:
			#     print('anns opened')

			#     while data:
			#         print('receiving data...')
			#         print('data=%s', (data))
			#         f.write(data)
			#         data = client.recv(1024)
			#     f.close()
			#     print("recieved")
		else:
			print("I will find enother one!")

	client.close()

# print(str(data))

# timerVar = False
# ex = False
# jsonTransfer = False

# def timerFunc():
# 	global timerVar

# 	time.sleep(1)
# 	if not timerVar:
# 		print("")
# 		print(" The device is not responding!")
# 		timerVar = True


# def UDPS():
# 	global ex
# 	global timerVar

# 	while not ex:
# 		print("")
# 		msg = input(" >  ")
# 		timerVar = False
# 		if msg == "close the console":
# 			ex = True
# 			os.abort()
# 			break
# 		else:
# 			UDP_IP = "127.0.0.1"
# 			UDP_PORT = 5006
# 			sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# 			sock.connect((UDP_IP, UDP_PORT))
# 			sock.send(str.encode(msg))
# 			sock.close()
# 			timer = threading.Thread(target=timerFunc, args=())
# 			timer.start()
# 			timer.join()
# 			while not timerVar:
# 				a = 1


# def UDPL():
# 	global ex
# 	global timerVar

# 	UDP_PORT = 5007
# 	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# 	sock.bind(('', UDP_PORT))

# 	while not ex:
# 		data = sock.recv(1024)
# 		dataParse = str(data)[2:len(str(data)) - 1]
# 		timerVar = True
# 		if len(str(data)) > 100:
# 			print("got file")
# 		elif "*" in dataParse:
# 			spl = dataParse
# 			stt = ""
# 			for i in range(len(spl)):
# 				stt = stt + "\n" + spl[i]

# 			print(stt)			
# 		else:
# 			print("")
# 			print(dataParse)

# print('')
# print(' "close the console" - to close the console')

# udpSender = threading.Thread(target=UDPS, args=())
# udpListener = threading.Thread(target=UDPL, args=())
# # timer = threading.Thread(target=timerFunc, args=())

# udpSender.start()
# udpListener.start()
# udpSender.join()
# udpListener.join()