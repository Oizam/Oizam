from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import requests
import os

Builder.load_file('App/kivy/login_signup.kv')

class Login(Screen):
    def visibility(self):
        password = self.ids["password"]
        visibility = self.ids["visibility"]
        if (password.password == True):
            password.password = False
            visibility.text = "Cacher"
        else:
            password.password = True
            visibility.text = "Afficher"
    
    def connection(self):
        body = {"email": self.ids["login"].text, "hashed_password": self.ids["password"].text}
        response  = requests.post("https://oizam.herokuapp.com/login/login", json=body)
        if response.status_code == 200:
            os.environ["TOKEN"] =  response.json()["access token"]
            self.manager.transition.direction = "left"
            self.manager.current = "home"

class SignUp(Screen):
    def profile_creation(self):
        self.manager.transition.direction = "left"
        self.manager.current = "home"