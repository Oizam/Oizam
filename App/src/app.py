from tensorflow.keras.preprocessing import image
from kivy.uix.screenmanager import Screen
import numpy as np
from tensorflow import keras
from kivy.lang import Builder
import os
import pandas as pd
import requests

global response
global modelFR
global modelUS
Builder.load_file('App/kivy/app.kv')

class BirdCard(Screen):
    def on_enter(self):
        self.ids['bird_name'].text = response['french_name']
        self.ids['image'].source = response['image']
        self.ids['image'].reload()
        self.ids['taille'].text = "Taille : " + response['taille']
        self.ids['genre'].text =  "Genre : " + response['genre']
        self.ids['text'].text =  "Détail : " + response['text']

class LoadApp(Screen):
    def __init__(self, **kw):
        global modelFR
        global modelUS
        modelFR = keras.models.load_model("App/data/model_fr.h5")
        modelUS = keras.models.load_model("App/data/model_us.h5")
        super().__init__(**kw)

        
            
class Loading(Screen):
  
    def on_enter(self):
        global response
        global modelFR
        global modelUS
        progress = self.ids['progress']
        img_path = "IMG.png"
        img = image.load_img(img_path, target_size=(299, 299))
        img_array = image.img_to_array(img)
        img_batch = np.expand_dims(img_array, axis=0)
        preprocessed_image = keras.applications.xception.preprocess_input(img_batch)
        if (os.environ["mode_model"] == "FR"):
            predict = modelFR.predict(preprocessed_image)
            id = predict.argmax() + 201
        else :
            predict = modelUS.predict(preprocessed_image)
            id = predict.argmax() + 1
        #modification bdd
        response  = requests.get("https://oizam.herokuapp.com/bird/"+str(id))
        if response.status_code == 200:
            body = {"bird_id": str(id), "user_id": str(os.environ["ID"])}
            requests.post("https://oizam.herokuapp.com/OiseauxDex", json=body)
            response = response.json()
            self.manager.current = "birdcard"
        else:
            self.manager.current = "home"
        
class Home(Screen):
    def deconnexion(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login" 
        #supprimer tokker
    
    def check_fr(self):
        os.environ["mode_model"] = "FR"
        
    def check_us(self):
        os.environ["mode_model"] = "US"