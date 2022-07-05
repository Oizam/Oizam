from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import requests
import os

Builder.load_file('App/kivy/dex.kv')

class Dex(Screen):
    def on_enter(self):
        scroll_view = self.ids["scroll"]
        scroll_view.clear_widgets()
        response  = requests.post("https://oizam.herokuapp.com/user/get_user_view/")
        if response.status_code == 200:
            os.environ["TOKEN"] =  response.json()["access token"]
            os.environ["ID"] = str(response.json()["user_connected"])
            self.manager.transition.direction = "left"
            self.manager.current = "home"
