
import select, socket, sys, Queue
import socket
import time
count = 0
HOST = 'localhost'    # The remote host
PORT = 5001              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
inputs = [s, sys.stdin]
inputs = [s, sys.stdin]
newData = 0
user = " "
#provides the user with possible login options
print "Type login followed by your username and password if you have a"
print "exsisting account. Otherwise type register"
print "followed by your desired username and password"
while inputs:
    readable, writable, exceptional = select.select(inputs, inputs, inputs)
    for socket in readable:
		#Recieved something from the server to be delt with
		if socket is s:
		    data = s.recv(1024)
		    data2 = data.split()
		    if data2[0] == "failed" and data2[1] =="1":#Username doesn't exsist
			print "No registered user with that name"

		    elif data2[0] == "failed" and data2[1] == "2":# Username is taken
			print "Username is taken try again"
		    elif data2[0] == "failed" and data2[1] == "3": #incorect credential
			print "incorrect username or password"
		    elif data2[0] == "connected": #succsesful connection
			print "Login succsesful"
			print "To message type in command line msg resipient message"
			print "To see all online users type list"
			print "To logout just type logout"  
		    elif data2[0] == "msg":#Recieved a message from the server
			print "Recieved a message from : " + data2[1]
			print "message: " + data2[2]
		    else: 
			print data

		elif socket is sys.stdin:
		    command = raw_input()
		    words = command.split()
		    for i, word in enumerate(words):#Users options 
			if word=="list":
				combo = word + " " + user
				s.sendall(combo)
				print "Current online users: "
			elif word == "logout":
				s.sendall(word+ " " + user)
			elif word == "msg":
				s.sendall(command + " " + user)
			elif word == "login" or word == "register":
				user = words[1]
				s.sendall(command)
s.close()





