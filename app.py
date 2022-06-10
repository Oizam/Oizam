from fileinput import filename
from fastapi import File
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
import cv2
from kivy.properties import ObjectProperty, ListProperty, StringProperty


Config.set('graphics', 'width', '340')
Config.set('graphics', 'height', '700')
Builder.load_file('app.kv')
sm = ScreenManager()
class Loading(Screen):
    pass
class Picture(Screen):
    pass

class CameraView(Screen):
    def capture(self):
        camera = self.ids['camera']
        camera.export_to_png("IMG.png")
        self.manager.get_screen("picture").ids.image.reload()
        sm.current = "picture"   

class Home(Screen):
    pass
        
    
class App(App):
    
    def build(self):
        self.file = "Fond_blanc.png.png"
        sm.add_widget(Home(name='home'))
        sm.add_widget(CameraView(name='cameraview'))
        sm.add_widget(Loading(name='loading'))
        sm.add_widget(Picture(name="picture"))
        return sm

app =  App()
app.run()