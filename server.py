
import select, socket, sys, Queue
user_name = []
socket_list = []
online_list = []
registered_users=[]
passwords = {}
connections = 0
user_connection = {}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('localhost', 5001))
server.listen(5)
inputs = [server, sys.stdin]
newData = 0
history = open("history.txt","rw+")#Reads in the user history into the registered data structure
for line in history:
	parts = line.split()
	user = parts[0]
	password = parts[1]
	registered_users.append(user)
	passwords[user] = password
while inputs:
    readable, writable, exceptional = select.select(
        inputs, inputs, inputs)
    for s in readable:
        # this stanza handles connection requests. 
        if s is server:
            print "received a connect requst from a client "
            print
            connection, client_address = s.accept()
            if connections == 0:
                connections = 1
                connection1 = connection
            else:
                connection2 = connection
            print "connection is {}".format (connection)
            connection.setblocking(0)
            inputs.append(connection)
        elif s is sys.stdin:
            newData = 1;
            command_string = raw_input()
            print "received:::: " + command_string
	    if(command_string == "end"):
		history.close()
		os.kill()
        else:
            # this stanza handles already connected sockets (data from clients)
            data = s.recv(1024)
            if data:
                print "read " + data
                words = data.split()
                print "received '" + data + "'"
                for i,word in enumerate(words):#decides what action to take based on the first word recieved which is the key word
                    if word == "login":
                        userID = words[i+1]
                        password = words[i+2]
                        print "userid {} and password {} ".format(userID, password)
			
			if userID in registered_users and passwords[userID] == password:
		                user_connection[userID] = s
				online_list.append(userID)
				s.send("connected")
			elif userID not in registered_users:
				s.send("failed 1")
			else:
				s.send("failed 3")

                    elif word == "msg":
                        userID = words[i+1]
                        msg = words[i+2]
			sender = words[i+3]
                        send_sock = user_connection[userID]
                        send_sock.send ("msg" + " " + sender + " " +msg)
		    elif word == "logout": 
			userID = words[i+1] 
			print userID + " has logged out"
			msg = "good bye" 
			send_sock = user_connection[userID]
                        send_sock.send (msg)
			online_list.remove(userID)
		    elif word == "list": 
			userID = words[i+1]
			msg=""
			for x in online_list:
				msg = msg + " " +x +", " 


			send_sock = user_connection[userID]
                        send_sock.send (msg)
		    elif word =="register":
			userID = words[i+1]
                        password = words[i+2]
                        print "userid {} and password {} ".format(userID, password)
			if userID not in registered_users:
		                user_connection[userID] = s
				online_list.append(userID)
				registered_users.append(userID)
				passwords[userID] = password
				history.write(userID + " " + password+"\n")
				s.send("connected")
			else:
				s.send("failed 2")
			
                if newData == 1:
                    data = command_string
                    newData = 0
                print "user-connection"
                print (user_connection)
    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()






Annotations
