from importlib.resources import path
from operator import imod
from pathlib import Path
from matplotlib import image
import bird_picture
import fake_bird_picture 
import random
from os import walk
from PIL import Image
import numpy as np
import pylab
import matplotlib.pyplot as plt

## Importation des photos d'oiseaux du dataset 
def nofake_list():                      
    bird_list = []
    path = "/home/valentin/Documents/projet_oizam/Oizam/Oizam/bird_picture/OizamFrance/images/"
    for (reperoire, sousRepertoire, fichiers) in walk(path) :
        for rep in sousRepertoire:
            for (repertoireb, sousRepertoireb, fichiersb) in walk(path + rep):
                for file in fichiersb:
                    bird_list.append(path + rep + '/' + file)
    return bird_list

# Importation des photos qui ne sont pas des oiseaux 
def fake_list(): 
    no_bird_list = []
    path = "/home/valentin/Documents/projet_oizam/Oizam/Oizam/fake_bird_picture"
    for (reperoire, sousRepertoire, fichiers) in walk(path) :
        for file in fichiers:
            no_bird_list.append(path + '/' + file)
    return no_bird_list

# Création d'une liste des labels avec un score de crédibilité
def dictionnaire (no_bird_list,bird_list,score): 
    score = 0 
    full_list = no_bird_list + bird_list
    label_score = {full_list,score}

#Création de la matrice de sélection pour l'utilsiateur 
def image_selection(no_bird_list,bird_list, rows = 1, cols=1):
    labelisation_list = []
    i = 7
    for j in range(0,i):
        labelisation_list.append(random.choice(no_bird_list))
    labelisation_list.append(random.choice(bird_list))
    random.shuffle(labelisation_list)

    figure, ax = plt.subplots(nrows=rows,ncols=cols )
    for letter in enumerate(labelisation_list):
        ax.ravel()[letter].imshow(images[title])
        ax.ravel()[letter].set_title(title)
        ax.ravel()[letter].set_axis_off()
    plt.tight_layout()
    plt.show()

total_images = 9

# https://www.delftstack.com/fr/howto/matplotlib/how-to-display-multiple-images-in-one-figure-correctly-in-matplotlib/   

# Labelisation par l'utilisateur 
def labelisation(labelisation_list):
    label = input ('Choissisez la photo d oiseau :')
    if label in bird_picture == True:
        score = score + 1
        return score
    else:
        print('Veuillez choisir une photo d oiseau')

