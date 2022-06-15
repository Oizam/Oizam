
from unicodedata import name
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import requests
import numpy as np
from fastapi import UploadFile
import json
from json import JSONEncoder


Config.set('graphics', 'width', '340')
Config.set('graphics', 'height', '700')
Builder.load_file('app.kv')
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
        img = image.load_img(img_path, target_size=(299, 299))
        progress.value = 0.25
        img_array = image.img_to_array(img)
        img_batch = np.expand_dims(img_array, axis=0)
        progress.value = 0.50
        preprocessed_image = tf.keras.applications.xception.preprocess_input(img_batch)
        body = {"Image":preprocessed_image}
        progress.value = 0.75
        encodedNumpyData = json.dumps(body, cls=NumpyArrayEncoder)
        request = requests.get("http://127.0.0.1:8000/predict/", json=encodedNumpyData)
        progress.value = 1
        response = eval(request.text)
        sm.current = "birdcard" 
   
class Picture(Screen):
    pass

class CameraView(Screen):

    def capture(self):
        # camera = self.ids['camera']
        # camera.export_to_png("IMG.png")
        self.manager.get_screen("picture").ids.image.reload()
        sm.current = "picture"   

class Home(Screen):
    pass
        
    
class App(App):
    

    def build(self):
        sm.add_widget(Home(name='home'))
        sm.add_widget(CameraView(name='cameraview'))
        sm.add_widget(Loading(name='loading'))
        sm.add_widget(Picture(name="picture"))
        sm.add_widget(BirdCard(name="birdcard"))
        return sm

app =  App()
app.run()