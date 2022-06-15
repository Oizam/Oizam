import bird_picture
import random

## Importation des photos d'oiseaux du dataset 
def nofake_list():                      
    bird_list = []
    for n in bird_picture : 
        bird_list.append(n)
    return bird_list

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