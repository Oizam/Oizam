from unicodedata import name
from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage
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
        self.ids['bird_name'].text = response['title']
        # icon = AsyncImage(source=response['image'])
        # self.ids['image'].source = str(icon)
        # self.ids['image'].reload()
        self.ids['taille'].text = response['taille']
        self.ids['genre'].text = response['genre']
        self.ids['disparition'].text = response['disparition']
        self.ids['text'].text = response['text']

class Loading(Screen):

    def on_enter(self):
        global response
        response = {'french_name': 'Colibri thalassin', 'class_bird': '070.Green_Violetear', 'title': 'Colibri thalassin', 'taille': '12 cm', 'ordre': 'Apodiformes', 'image': 'https://www.oiseaux.net/photos/serge.nicolle/images/colibri.thalassin.seni.1p.jpg', 'famille': '\n ', 'descripteur': 'Swainson, 1827', 'espece': 'thalassinus', 'id': 70, 'english_name': 'Mexican Violetear', 'text': "Le dessus du plumage est vert bleuâtre avec une bande subterminale bleu-noir sur la queue. Ces oiseaux multicolores, de taille moyenne, varient de 10,5 à 11,5 centimètres. La queue exhibe une large bande violette sur la partie centrale des rectrices. Les décorations faciales et auriculaires exposent de remarquables brillances jaunes et dorées qui se poursuivent jusqu'aux taches vertes de la poitrine. \nChez la femelle (seulement 9 g), les décorations de la face et de la poitrine sont légèrement plus visibles. Chez les juvéniles, les rémiges sont brun-ardoise ou avec une nuance de bronze foncé sur la nuque et le croupion. La race nominale se distingue très nettement des autres sous-espèces par son évidente tache bleu-violet. La race cyanotus, plus décrite dans l'encyclopédie du Venezuela par Kiliti comme un colibri montagnard, a un dessous plus pâle et plus remarquable.", 'poids': '', 'localisation': 'https://www.oiseaux.net/maps/images/colibri.thalassin.1.200.w.png', 'genre': 'Trochilidés', 'disparition': 'LC', 'envergure': '-'}
        # progress = self.ids['progress']
        # img_path = "oiseau.jpg"
        # img = image.load_img(img_path, target_size=(160, 160))
        # progress.value = 0.25
        # img_array = image.img_to_array(img)
        # img_batch = np.expand_dims(img_array, axis=0)
        # progress.value = 0.50
        # preprocessed_image = tf.keras.applications.xception.preprocess_input(img_batch)
        # body = {"Image":preprocessed_image}
        # progress.value = 0.75
        # encodedNumpyData = json.dumps(body, cls=NumpyArrayEncoder)
        # try:
        #     request = requests.get("http://127.0.0.1:5000/predict/", json=encodedNumpyData)
        #     # request = requests.get("https://oizam-api.herokuapp.com/predict/", json=encodedNumpyData)
        # except:
        #     sm.current = "home" 
        # progress.value = 1
        # req = request.text
        # req = req.replace("null", "''")
        # response = eval(req)
        # print(response)
        
        
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