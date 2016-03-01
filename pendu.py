#pendu

import random

mots = ['cybersecurite', 'chien', 'chat', 'souris', 'grenouille']
vies_restantes = 14
lettres_devinees = ''

def jouer():
    mot = choisir_un_mot()
    while True:
        supposition = obtenir_supposition(mot)
        if traiter_supposition(supposition, mot):
            print('Vous avez gagne ! Bravo !')
            break
        if vies_restantes == 0:
            print('Vous etes pendu !')
            print('Le mot etait : ' + mot)
            break

def choisir_un_mot():
    mot_position = random.randint(0, len(mots) - 1)
    return mots[mot_position]

def obtenir_supposition(mot):
    afficher_mot_avec_tirets(mot)
    print('Vies restantes : ' + str(vies_restantes))
    supposition = raw_input(' Devinez une lettre ou le mot entier ? ')
    return supposition
    
def traiter_supposition(supposition, mot):
    global vies_restantes
    global lettres_devinees
    vies_restantes = vies_restantes -1
    lettres_devinees = lettres_devinees + supposition
    return False
    
def afficher_mot_avec_tirets(mot):
    afficher_mot = ''
    for lettre in mot:
        if lettres_devinees.find(lettre) > -1:
            # lettre trouvee
            afficher_mot = afficher_mot + lettre
        else:
            # lettre non trouvee
            afficher_mot = afficher_mot + '-'
    print(afficher_mot)

jouer()
