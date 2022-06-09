from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

Config.set('graphics', 'width', '340')
Config.set('graphics', 'height', '700')
Builder.load_file('app.kv')

class DescriptionView(BoxLayout):
    pass

class CameraView(Screen):
    def build(self):
        pass
        
class Home(Screen):
        
    def import_picture(self):
        print("picture import")


class App(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Home(name='home'))
        sm.add_widget(CameraView(name='cameraview'))
        return sm

app =  App()
app.run()