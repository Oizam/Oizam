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
from PIL import Image
from matplotlib import pyplot as plt

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

#Création d'une selection d'image 
def image_selection(no_bird_list,bird_list, rows = 1, cols=1):
    labelisation_list = []
    i = 8
    for j in range(0,i):
        labelisation_list.append(random.choice(no_bird_list))
    labelisation_list.append(random.choice(bird_list))
    random.shuffle(labelisation_list)
    return labelisation_list

#Création d'une matrice d'image 
def matrice(images, rows = 1, cols=1, figsize=(15,15)):
        figure, ax = plt.subplots(nrows=rows,ncols=cols,figsize=figsize)
        for ind,title in enumerate(images):
            ax.ravel()[ind].imshow(images[title])
            ax.ravel()[ind].set_axis_off()
        plt.tight_layout()
        plt.show()

def create_list_images_from_path(image_paths_list):
    images = []
    for image_path in image_paths_list:
        images.append(Image.open(image_path))
    return images

def image_grid(imgs, rows, cols):
    assert len(imgs) == rows*cols

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid

def resize_image(image_paths, height, width):
    resized_images = []
    for image_path in image_paths:
        new_size = (width, height)
        resized_images.append(np.asarray(Image.open(image_path).resize(new_size)))
    return resized_images

total_images = 9
labelisation_list = image_selection(fake_list(),nofake_list())
resized_images = resize_image(labelisation_list, 300, 300)
images = {'Image'+str(i): image_oiseau for i, image_oiseau in enumerate(resized_images)}
matrice(images, 3,3)
matrice_selection = matrice(images, 3,3)

# Labelisation par l'utilisateur 
def labelisation(labelisation_list):
    label = input ('Choissisez la photo d oiseau :')
    if label in bird_picture == True:
        score = score + 1
        return score
    else:
        print('Veuillez choisir une photo d oiseau')
