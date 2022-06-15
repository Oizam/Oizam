import bird_picture
import fake_bird_picture 
import numpy as np

def nofake_list(): 
    bird_list = []
    for n in bird_picture : 
        bird_list.append(n)

def fake_list(): 
    no_bird_list = []
    for n in fake_bird_picture:
        no_bird_list.append(n)

def dictionnaire (score): 

association clef (nom fichier) valeur (valeur=score )

def image_selection():
    tableau = np.array([[1,1,1],[1,1,1],[1,1,1]])
    print (tableau)

def labelisation(image_selection):
    label = input ('Choissisez la photo d oiseau :')
    if label = true:
        score = score + 1
        else:
            print('Veuillez choisir une photo d oiseau')