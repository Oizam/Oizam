from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file('App/kivy/camera.kv')
class PictureCamera(Screen):
    pass
        

class CameraView(Screen):
        
    def capture(self):
        # camera = self.ids['camera']
        # camera.export_to_png("IMG.png")
        self.manager.get_screen("picturecamera").ids.image.reload()
        self.manager.current = "picturecamera" 
