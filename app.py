from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config


Config.set('graphics', 'width', '340')
Config.set('graphics', 'height', '700')
class DescriptionView(BoxLayout):
    pass

class CameraView(BoxLayout):
    def __init__(self):
        super(CameraView, self).__init__()
        
    
class Home(BoxLayout):
    def __init__(self):
        super(Home, self).__init__()
    
    def take_picture(self):
        return CameraView()
    
    def import_picture(self):
        print("picture import")


class App(App):
    def build(self):
        return Home()

app =  App()
app.run()