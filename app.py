from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage
from tensorflow.keras.preprocessing import image
from tensorflow import keras
import tensorflow as tf
import numpy as np
from json import JSONEncoder
import shutil
import re
import pandas as pd
import os

global response
global mode_model
global bird_dex

Config.set('graphics', 'width', '340')
Config.set('graphics', 'height', '700')
Builder.load_file('App/kivy/app.kv')
Builder.load_file('App/kivy/camera.kv')
Builder.load_file('App/kivy/explorer.kv')
sm = ScreenManager()


modelFR = keras.models.load_model("App/data/complete_model_FR_87.h5")
modelUS = keras.models.load_model("App/data/complete_model_81.h5")


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

class BirdCard(Screen):
    def on_enter(self):
        for i, row in response.iterrows():
            self.ids['bird_name'].text = str(row['french name'])
            self.ids['image'].source = str(row['image'])
            self.ids['image'].reload()
            self.ids['taille'].text = "Taille : " + str(row['taille'])
            self.ids['genre'].text =  "Genre : " + str(row['genre'])
            self.ids['text'].text =  "Détail : " + str(row['text'])

class Loading(Screen):

    def on_enter(self):
        global response
        global bird_dex
        
        progress = self.ids['progress']
        img_path = "oiseau.jpg"
        img = image.load_img(img_path, target_size=(299, 299))
        progress.value = 0.25
        img_array = image.img_to_array(img)
        img_batch = np.expand_dims(img_array, axis=0)
        progress.value = 0.50
        preprocessed_image = tf.keras.applications.xception.preprocess_input(img_batch)
        progress.value = 0.75
        if (mode_model == "FR"):
            predict = modelFR.predict(preprocessed_image)
            id = predict.argmax() + 201
        else :
            predict = modelUS.predict(preprocessed_image)
            id = predict.argmax() + 1
        response = bird_dex[bird_dex["id"] == id]
        progress.value = 1     
        sm.current = "birdcard" 
   
class PictureCamera(Screen):
    pass

class PictureFileChooser(Screen):
    pass

  

class Home(Screen):
    def check_fr(self):
        global mode_model
        mode_model = "FR"
        
    def check_us(self):
        global mode_model
        mode_model = "US"

class FileChooser(Screen):
    def on_enter(self):
        filechooser = self.ids['filechooser']
        filechooser.path = os.path.abspath(os.getcwd())

          
    def save(self, path):
        regex = "([^\\s]+(\\.(?i)(jpe?g|png|gif|bmp))$)"
        p = re.compile(regex)
        if(re.search(p, path)):
            print(path)
            try :
                shutil.copyfile(path, "./IMG.png")
            except:
                pass
            self.manager.get_screen("picturefilechooser").ids.image.reload()
            sm.current = "picturefilechooser"
        else:
            pass        
    
class App(App):
    def build(self):
        global mode_model
        global bird_dex
        
        mode_model = "FR"
        bird_dex = pd.read_csv("App/data/OiseauxFini.csv")
        sm.add_widget(Home(name='home'))
        sm.add_widget(CameraView(name='cameraview'))
        sm.add_widget(Loading(name='loading'))
        sm.add_widget(PictureCamera(name="picturecamera"))
        sm.add_widget(PictureFileChooser(name="picturefilechooser"))
        sm.add_widget(BirdCard(name="birdcard"))
        sm.add_widget(FileChooser(name="filechooser"))
        return sm

app =  App()
app.run()