from imp import reload
from tensorflow.keras.preprocessing import image
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import numpy as np
from tensorflow import keras
import os
import pandas as pd
import requests

global bird
global list_bird
global list_id
global index_bird
global modelFR
global modelUS
Builder.load_file('App/kivy/app.kv')



class BirdCard(Screen):
    def on_enter(self):
        self.ids['bird_name'].text = bird['french_name']
        self.ids['image'].source = bird['image']
        self.ids['image'].reload()
        self.ids['taille'].text = "Taille : " + bird['taille']
        self.ids['genre'].text =  "Genre : " + bird['genre']
        self.ids['text'].text =  "Détail : " + bird['text']

class LoadApp(Screen):
    def __init__(self, **kw):
        global modelFR
        global modelUS
        modelFR = keras.models.load_model("App/data/model_fr.h5")
        modelUS = keras.models.load_model("App/data/model_us.h5")
        super().__init__(**kw)

class BirdChoice(Screen):
    
    def reload(self):
        global index_bird
        global list_bird
        
        self.ids["image_choice"].source = list_bird[index_bird]['image']
        self.ids["image_choice"].reload()
        
    def on_enter(self):
        global index_bird
        index_bird = 0
        self.reload()
    
    def next(self):
        global index_bird
        global list_bird
        
        if (index_bird < len(list_bird)-1):
            index_bird +=1
        else:
            index_bird = 0
        self.reload()
                
    def previous(self):
        global index_bird
        global list_bird
        
        if (index_bird > 0):
            index_bird -=1
        else:
            index_bird = len(list_bird)-1
        self.reload()
    
    def confirm(self):
        global bird
        global list_bird
        global index_bird
        body = {"bird_id": str(id), "user_id": str(os.environ["ID"])}
        requests.post("https://oizam.herokuapp.com/OiseauxDex", json=body)
        bird = list_bird[index_bird]
        self.manager.current = "birdcard"
        
        
            
class Loading(Screen):
  
    def on_enter(self):
        global list_bird
        global list_id
        global modelFR
        global modelUS
        img_path = "IMG.png"
        img = image.load_img(img_path, target_size=(299, 299))
        img_array = image.img_to_array(img)
        img_batch = np.expand_dims(img_array, axis=0)
        preprocessed_image = keras.applications.xception.preprocess_input(img_batch)
        if (os.environ["mode_model"] == "FR"):
            predict = modelFR.predict(preprocessed_image)
            # id = predict.argmax() + 201
        else :
            predict = modelUS.predict(preprocessed_image)
            # id = predict.argmax() + 1
        list_id = {"1": "problable","2":"peu probable", "3":"probable"}
        list_bird = []
        for id in list_id.keys():
            response  = requests.get("https://oizam.herokuapp.com/bird/"+str(id))
            if response.status_code == 200:
                list_bird.append(response.json())
            else:
                self.manager.current = "home"
        self.manager.transition.direction = "left"
        self.manager.current = "birdchoice"
        #modification bdd
        
        
class Home(Screen):
    def deconnexion(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login" 
        #supprimer tokker
    
    def check_fr(self):
        os.environ["mode_model"] = "FR"
        
    def check_us(self):
        os.environ["mode_model"] = "US"