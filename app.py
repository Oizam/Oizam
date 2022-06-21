from unicodedata import name
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import requests
import numpy as np
import json
import os
from json import JSONEncoder
import shutil
import re

Config.set('graphics', 'width', '340')
Config.set('graphics', 'height', '700')
Builder.load_file('kivy/app.kv')
Builder.load_file('kivy/camera.kv')
Builder.load_file('kivy/explorer.kv')
sm = ScreenManager()
global response

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

class BirdCard(Screen):
    def on_enter(self):
        global response
        self.ids['bird_name'].text = response['result']

class Loading(Screen):

    def on_enter(self):
        global response
        progress = self.ids['progress']
        img_path = "oiseau.jpg"
        img = image.load_img(img_path, target_size=(150, 150))
        progress.value = 0.25
        img_array = image.img_to_array(img)
        img_batch = np.expand_dims(img_array, axis=0)
        progress.value = 0.50
        preprocessed_image = tf.keras.applications.xception.preprocess_input(img_batch)
        body = {"Image":preprocessed_image}
        progress.value = 0.75
        encodedNumpyData = json.dumps(body, cls=NumpyArrayEncoder)
        try:
            request = requests.get("https://oizam-api.herokuapp.com/predict/", json=encodedNumpyData)
        except:
            sm.current = "home" 
        progress.value = 1
        response = eval(request.text)
        
        
        
        sm.current = "birdcard" 
   
class PictureCamera(Screen):
    pass

class PictureFileChooser(Screen):
    pass

class CameraView(Screen):

    def capture(self):
        # camera = self.ids['camera']
        # camera.export_to_png("IMG.png")
        self.manager.get_screen("picturecamera").ids.image.reload()
        sm.current = "picturecamera"   

class Home(Screen):
    pass

class FileChooser(Screen):
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