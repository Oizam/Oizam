from App.src.proba_pred import n_most_probable, prediction, min_trust_level
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from tensorflow import keras
import os
import requests


global bird
global list_bird
global list_id
global index_bird
global modelFR
global modelUS
global trust
Builder.load_file('App/kivy/app.kv')

class BirdCard(Screen):
    def on_enter(self):
        self.ids['bird_name'].text = bird['french_name']
        try:
            self.ids['image'].source = bird['image']
            self.ids['image'].reload()
        except:
            self.ids['image'].source = "logo.jpeg"
            self.ids['image'].reload()
            
        try:
            self.ids['taille'].text = "Taille : " + bird['taille']
        except:
            self.ids['taille'].text = "Taille : Inconnu"
        try:
            self.ids['genre'].text =  "Genre : " + bird['genre']
        except:
            self.ids['genre'].text =  "Genre : Inconnu" 
        try:
            self.ids['text'].text =  "Détail : " + bird['text']
        except:
            self.ids['text'].text =  "Détail : Inconnu"

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
        
        self.ids["bird_name_choice"].text = list_bird[index_bird]['french_name']
        try:
            self.ids['taille_choice'].text = "Taille : " + list_bird[index_bird]['taille']
        except:
            self.ids['taille_choice'].text = "Taille : Inconnu"
        try:
            self.ids['envergure_choice'].text = "Envergure : " + list_bird[index_bird]['envergure']
        except:
            self.ids['envergure_choice'].text = "Envergure : Inconnu"
        try:
            self.ids["image_choice"].source = list_bird[index_bird]['image']
            self.ids["image_choice"].reload()
        except:
            self.ids['image'].source = "logo.jpeg"
            self.ids['image'].reload()
            
    def on_enter(self):
        global index_bird
        index_bird = 0
        self.reload()
    
    def next(self):
        global index_bird
        global list_bird
        global list_id
        
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
        body = {"bird_id": str(list_id[index_bird]) , "user_id": str(os.environ["ID"])}
        requests.post("https://oizam.herokuapp.com/OiseauxDex", json=body)
        bird = list_bird[index_bird]
        self.manager.current = "birdcard"
        
        
            
class Loading(Screen):
  
    def on_enter(self):
        global list_bird
        global list_id
        global modelFR
        global modelUS
        global trust
        if (os.environ["mode_model"] == "FR"):
            predict = prediction(modelFR)
            trust = min_trust_level(predict)
            list_id = n_most_probable(predict)
            for i in range(0, len(list_id)):
                list_id[i] += 201
        else :
            predict = prediction(modelUS)
            trust = min_trust_level(predict)
            list_id = n_most_probable(predict)
            for i in range(0, len(list_id)):
                list_id[i] += 1
        list_bird = []
        print(trust)
        for id in list_id:
            response  = requests.get("https://oizam.herokuapp.com/bird/"+str(id))
            if response.status_code == 200:
                list_bird.append(response.json())
            else:
                self.manager.current = "home"
        self.manager.transition.direction = "left"
        self.manager.current = "birdchoice"
        
        
class Home(Screen):
    def deconnexion(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login" 
        #supprimer tokker
    
    def check_fr(self):
        os.environ["mode_model"] = "FR"
        
    def check_us(self):
        os.environ["mode_model"] = "US"