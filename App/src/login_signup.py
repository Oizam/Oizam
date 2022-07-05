from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
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
            os.environ["ID"] = str(response.json()["user_connected"])
            self.manager.transition.direction = "left"
            self.manager.current = "home"

class SignUp(Screen):
    
    def popup(self, title, text):
        layout = GridLayout(cols = 1, padding = 10)
        popupLabel = Label(text = text)
        closeButton = Button(text = "Close")
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
        popup = Popup(title= title, content = layout,
                    size_hint =(None, None), size =(200, 200))  
        popup.open() 
        closeButton.bind(on_press = popup.dismiss)
    
    def profile_creation(self):
        requierement = True
        password = True
        if (self.ids['firstname'].text == ''):
            requierement = False
        elif(self.ids['last_name'].text == ''):
            requierement = False
        elif(self.ids['username'].text == ''):
            requierement = False
        elif(self.ids['email'].text == ''):
            requierement = False
        elif(self.ids['password_signup'].text == ''):
            requierement = False
        elif(self.ids['password_signup_confirm'].text == ''):
            requierement = False
        elif(self.ids['password_signup'].text != self.ids['password_signup_confirm'].text):
            password = False
            
        if(requierement == True and password == True):
            mail = True
            if (mail == True):
                self.popup("Compte créer", "Veuillez vous connecter")
                self.manager.transition.direction = "left"
                self.manager.current = "login"
            else:
                self.popup("Mail incorect", "Ce mail est déja utilisé")
            
        elif (requierement == False):
            self.popup("Champs manquant", "Compléter tout les champs")
            
        else:
            self.popup("Erreur Mot de passe", "Mot de passe différent")