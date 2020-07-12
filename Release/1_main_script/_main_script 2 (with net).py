from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import matplotlib.patches as patches
from torchvision import transforms
from pycocotools.coco import COCO
import matplotlib.pyplot as plt
import matplotlib.image as im
import torch.utils.data
from PIL import Image
import pandas as pd
import numpy as np
import torchvision
import threading
import socket
import torch
import time
import json
import os


imageTransfering = False
noData = False
ready = True

LISTEN_TO_PC_PORT = 5005
LISTEN_TO_USER_PORT = 5006
ANSWER_TO_PC_PORT = 5007
ANSWER_TO_USER_PORT = 5008

default_min_score = 0
default_min_box_width = 10
default_min_box_height = 10
default_max_box_width = 300
default_max_box_height = 300
default_left_border = 0
default_right_border = 0
default_bottom_border = 0
default_top_border = 0

min_score = 0
min_box_width = 10
min_box_height = 10
max_box_width = 300
max_box_height = 300
left_border = 0
right_border = 0
bottom_border = 0
top_border = 0



def UDP_PC_2_PC():
	global ready

	TCP_IP = "127.0.0.1"
	TCP_PORT = LISTEN_TO_PC_PORT
	import socket

	# Задаем адрес сервера
	SERVER_ADDRESS = (TCP_IP, TCP_PORT)

	# Настраиваем сокет
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(SERVER_ADDRESS)
	server_socket.listen(1)
	print('server is running, please, press ctrl+c to stop')

	# Слушаем запросы
	while True:
	    connection, address = server_socket.accept()
	    print("new connection from {address}".format(address=address))
	    data = connection.recv(1024)
	    dataParse = str(data)[2:len(str(data)) - 1]

	    if dataParse == "stop":
	    	break

	    elif dataParse == "reboot":
	    	print("Wait a minute")

	    elif dataParse == "ping":
	    	connection.send(bytes('pong', encoding='UTF-8'))

	    elif dataParse == "next":
	    	if ready:
	    		connection.send(bytes('yes', encoding='UTF-8'))
	    		ready = False
	    		dataP = connection.recv(1024)
	    		with open('image.jpg', 'wb') as f:
	    			print('file opened')
	    			while dataP:
	    				f.write(dataP)
	    				dataP = connection.recv(1024)
	    			f.close()

	    		# print("Have an image")

	    		data_transforms = transforms.Compose([transforms.ToTensor()])
	    		img = Image.open("image.jpg").convert("RGB")
	    		imgTensor = data_transforms(img)
	    		prediction = m([imgTensor.cuda()])

	    		lent = len(prediction[1][0]['boxes'])
	    		predListBoxes = prediction[1][0]['boxes'].tolist()
	    		predListScores = prediction[1][0]['scores'].tolist()
	    		predListLabels = prediction[1][0]['labels'].tolist()

	    		# print("Have a prediction")

	    		outputDict = {}

	    		for i in range(lent):
	    			# print("score: " + str(predListScores[i]))
		    		# print("box width: " + str(abs(predListBoxes[i][0] - predListBoxes[i][2])))
		    		# print("box height: " + str(abs(predListBoxes[i][1] - predListBoxes[i][3])))
		    		# print("left border: " + str(predListBoxes[i][0]))
		    		# print("right border: " + str(abs(imgTensor.shape[2] - predListBoxes[i][2])))
		    		# print("top border: " + str(predListBoxes[i][1]))
		    		# print("bottom border: " + str(abs(imgTensor.shape[1] - predListBoxes[i][3])))

	    			if min_score <= predListScores[i]\
	    			and min_box_width <= abs(predListBoxes[i][0] - predListBoxes[i][2])\
	    			and min_box_height <= abs(predListBoxes[i][1] - predListBoxes[i][3])\
	    			and max_box_width >= abs(predListBoxes[i][0] - predListBoxes[i][2])\
	    			and max_box_height >= abs(predListBoxes[i][1] - predListBoxes[i][3])\
	    			and left_border <= predListBoxes[i][0]\
	    			and right_border <= abs(imgTensor.shape[2] - predListBoxes[i][2])\
	    			and top_border <= predListBoxes[i][1]\
	    			and bottom_border <= abs(imgTensor.shape[1] - predListBoxes[i][3]):

		    			outputDict[str(i)] = {
		    			"bbox": predListBoxes[i],
		    			"score": predListScores[i],
		    			"label": predListLabels[i]}

		    		# l = json.dumps(outputDict).encode()
		    		# print("Have a file")
		    		# connection.send(l)

		    		with open('last.json', 'w') as f:
		    			json.dump(outputDict, f)

		    		ready = True

		    	# 	# f = open("last.json", "rb")
		    	# 	# l = f.read(1024)
		    	# 	# while(l):
		    	# 	# 	connection.send(l)
		    	# 	# 	l = f.read(1024)
		    	# 	# f.close()
	    	else:
	    		connection.send(bytes('no', encoding='UTF-8'))

	    elif dataParse == "last":
	    	try:
	    		f = open("last.json", "rb")
	    		l = f.read(1024)
	    		while(l):
	    			connection.send(l)
	    			l = f.read(1024)
	    		f.close()
	    	except:
	    		jsonF = {"test":101}
	    		with open("last.json", "w") as write_file:
	    			json.dump(jsonF, write_file)

	    		f = open("last.json", "rb")
	    		l = f.read(1024)
	    		while(l):
	    			connection.send(l)
	    			l = f.read(1024)
	    		f.close()

	    connection.close()


def UDP_USER_2_PC():
	UDP_PORT = LISTEN_TO_USER_PORT
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.bind(('', UDP_PORT))

	while True:
		data = sock.recv(1024)

		global min_score
		global min_box_width
		global min_box_height
		global max_box_width
		global max_box_height
		global left_border
		global right_border
		global bottom_border
		global top_border

		dataParse = str(data)[2:len(str(data)) - 1]
		print(dataParse)

		if dataParse == "stop":
			os.abort()

		elif dataParse == "params_list":
			stt = "Filtering parametres:* *Minimum score: " + str(min_score)\
			+ "*Minimum box width: " + str(min_box_width)\
			+ "*Minimum box hieght: " + str(min_box_height)\
			+ "*Maximum box width: " + str(max_box_width)\
			+ "*Maximum box hieght: " + str(max_box_height)\
			+ "*Left border: " + str(left_border)\
			+ "*Right border: " + str(right_border)\
			+ "*Bottom border: " + str(bottom_border)\
			+ "*Top border: " + str(top_border)
			ansverUSER(stt)

		elif dataParse == "help":
			ansverUSER('List of commands:*'\
				+'*"close the console" - to close the console*'\
				+'*"reboot" - reboot the system'\
				+'*"params_list" - show the list of filtering parametres'\
				+'*"params_default" - set default parametres'\
				+'*"min_score <value>" - set score threshold'\
				+'*"min_box_height <value>"'\
				+'*"min_box_width <value>"'\
				+'*"max_box_height <value>"'\
				+'*"max_box_width <value>"'\
				+'*"left_border <value>"'\
				+'*"right_border <value>"'\
				+'*"bottom_border <value>"'\
				+'*"top_border <value>"')

		elif dataParse == "turn_off":
			ansverUSER("Bye!")

		elif dataParse == "reboot":
			ansverUSER("See u")

		elif dataParse == "params_default":
			min_score = default_min_score
			min_box_width = default_min_box_width
			min_box_height = default_min_box_height
			max_box_width = default_max_box_width
			max_box_height = default_max_box_height
			left_border = default_left_border
			right_border = default_right_border
			bottom_border = default_bottom_border
			top_border = default_top_border
			saveParams();
			ansverUSER("Done")

		elif " " in dataParse:
			try:
				if dataParse.split(" ")[0] == "min_score":
					min_score = float(dataParse.split(" ")[1])
					ansverUSER("Done")

				elif dataParse.split(" ")[0] == "min_box_width":
					min_box_width = int(dataParse.split(" ")[1])
					ansverUSER("Done")

				elif dataParse.split(" ")[0] == "min_box_height":
					min_box_height = int(dataParse.split(" ")[1])
					ansverUSER("Done")

				elif dataParse.split(" ")[0] == "max_box_width":
					max_box_width = int(dataParse.split(" ")[1])
					ansverUSER("Done")

				elif dataParse.split(" ")[0] == "max_box_height":
					max_box_height = int(dataParse.split(" ")[1])
					ansverUSER("Done")

				elif dataParse.split(" ")[0] == "left_border":
					left_border = int(dataParse.split(" ")[1])
					ansverUSER("Done")

				elif dataParse.split(" ")[0] == "right_border":
					right_border = int(dataParse.split(" ")[1])
					ansverUSER("Done")

				elif dataParse.split(" ")[0] == "bottom_border":
					bottom_border = int(dataParse.split(" ")[1])
					ansverUSER("Done")

				elif dataParse.split(" ")[0] == "top_border":
					top_border = int(dataParse.split(" ")[1])
					ansverUSER("Done")
				else:
					ansverUSER("Incorrect command!")

				saveParams();

			except:
				ansverUSER("Incorrect value!")

		else:
			ansverUSER("Incorrect command!")
		# elif str(data) == "b'params list'":



def ansverPC(ans):
	UDP_IP = "127.0.0.1"  
	UDP_PORT = ANSWER_TO_PC_PORT
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.connect((UDP_IP, UDP_PORT))
	sock.send(str.encode(ans))

def ansverUSER(ans):
	UDP_IP = "127.0.0.1"  
	UDP_PORT = ANSWER_TO_USER_PORT
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.connect((UDP_IP, UDP_PORT))
	sock.send(str.encode(ans))

def saveParams():
	global min_score
	global min_box_width
	global min_box_height
	global max_box_width
	global max_box_height
	global left_border
	global right_border
	global bottom_border
	global top_border

	dictV = {'min_score': min_score,
	'min_box_width': min_box_width,
	'min_box_height': min_box_height,
	'max_box_width': max_box_width,
	'max_box_height': max_box_height,
	'left_border': left_border,
	'right_border': right_border,
	'bottom_border': bottom_border,
	'top_border': top_border}

	with open("params.json", "w") as write_file:
		json.dump(dictV, write_file)

####################### Program #######################
try:
	with open("params.json", "r") as read_file:
	    data = json.load(read_file)

	    min_score = data["min_score"]
	    min_box_width = data["min_box_width"]
	    min_box_height = data["min_box_height"]
	    max_box_width = data["max_box_width"]
	    max_box_height = data["max_box_height"]
	    left_border = data["left_border"]
	    right_border = data["right_border"]
	    bottom_border = data["bottom_border"]
	    top_border = data["top_border"]

	pc2pcThread = threading.Thread(target=UDP_PC_2_PC, args=())
	user2pcThread = threading.Thread(target=UDP_USER_2_PC, args=())
	pc2pcThread.start()
	user2pcThread.start()
	print("")
	print("--- System is running ---")
	print("")
except:
	saveParams()

	with open("params.json", "r") as read_file:
	    data = json.load(read_file)

	    min_score = data["min_score"]
	    min_box_width = data["min_box_width"]
	    min_box_height = data["min_box_height"]
	    max_box_width = data["max_box_width"]
	    max_box_height = data["max_box_height"]
	    left_border = data["left_border"]
	    right_border = data["right_border"]
	    bottom_border = data["bottom_border"]
	    top_border = data["top_border"]

	pc2pcThread = threading.Thread(target=UDP_PC_2_PC, args=())
	user2pcThread = threading.Thread(target=UDP_USER_2_PC, args=())
	pc2pcThread.start()
	user2pcThread.start()
	print("")
	print("--- System is running ---")
	print("")

device = torch.device('cpu')
m = torch.jit.load('model.pt')
m = m.eval()
