from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import get_color_from_hex
import requests
import os
from operator import itemgetter

Builder.load_file('App/kivy/dex.kv')
global bird
class BirdCardDex(Screen):
    def on_enter(self):
        try:
            self.ids['bird_name'].text = bird['french_name']
        except:
            self.ids['bird_name'].text = ""
            
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
        
class Dex(Screen):
    def infos_bird(self, id, obj):
        global bird
        response  = requests.get("https://oizam.herokuapp.com/bird/"+str(id))
        if response.status_code == 200:
            bird = response.json()
            self.manager.transition.direction = "right"
            self.manager.current = "birdcarddex"
                
    def on_enter(self):
        dex = self.ids["dex"]
        dex.clear_widgets()
        response  = requests.get("https://oizam.herokuapp.com/OiseauxDex/"+str(os.environ["ID"]))
        if response.status_code == 200:
            birds_list = sorted(response.json()[0]["birds"], key=itemgetter('id')) 
            for bird in birds_list:
                dex.add_widget(AsyncImage(source=bird["image"]))
                dex.add_widget(Label(text=bird['french_name'], font_size=10))
                button = Button(text=str(bird['id']), font_size=10, color= get_color_from_hex('#FFFFFF'),background_color = get_color_from_hex('#1C2942'))
                button.fbind('on_press',self.infos_bird, bird['id'])
                dex.add_widget(button)

