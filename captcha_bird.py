import bird_picture
import fake_bird_picture 
import random
from PIL import Image
from os import walk

## Importation des photos d'oiseaux du dataset 
def nofake_list():                      
    bird_list = []
    path = "./Oizam/Oizam/bird_picture/OizamFrance/images/"
    for (reperoire, sousRepertoire, fichiers) in walk(path) :
        for rep in sousRepertoire:
            for (repertoireb, sousRepertoireb, fichiersb) in walk(path + rep):
                for file in fichiersb:
                    #bird_list.append(file)
                    im = Image.open(bird_list.append(file))
                    bird_list.append(im)
    return bird_list

# Importation des photos qui ne sont pas des oiseaux 
def fake_list(): 
    no_bird_list = []
    for n in fake_bird_picture:
        no_bird_list.append(n)
    return no_bird_list

# Création d'une liste des labels avec un score de crédibilité
def dictionnaire (no_bird_list,bird_list,score): 
    score = 0 
    full_list = no_bird_list + bird_list
    label_score = {full_list,score}

#Création de la matrice de sélection pour l'utilsiateur 
def image_selection():
    labelisation_list = []
    i = 6
    for i in labelisation_list:
        labelisation_list.append(random.choice(fake_bird_picture))
    labelisation_true_image = random.choice(bird_picture)
    labelisation_list.append(labelisation_true_image)
    random.shuffle(labelisation_list)

# Labelisation par l'utilisateur 
def labelisation(image_selection):
    label = input ('Choissisez la photo d oiseau :')
    if label in bird_picture == True:
        score = score + 1
        return score
    else:
        print('Veuillez choisir une photo d oiseau')

print(nofake_list())