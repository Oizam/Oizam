from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
import requests
import os
from operator import itemgetter

Builder.load_file('App/kivy/dex.kv')

class Dex(Screen):
    def on_enter(self):
        dex = self.ids["dex"]
        dex.clear_widgets()
        response  = requests.get("https://oizam.herokuapp.com/OiseauxDex/"+str(os.environ["ID"]))
        if response.status_code == 200:
            birds_list = sorted(response.json()[0]["birds"], key=itemgetter('id')) 
            for bird in birds_list:
                dex.add_widget(AsyncImage(source=bird["image"]))
                dex.add_widget(Label(text=bird['french_name'], font_size=10))
                dex.add_widget(Label(text=str(bird['id']), font_size=10))

