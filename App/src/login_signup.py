from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

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
        self.manager.current = "home"

class SignUp(Screen):
    pass
