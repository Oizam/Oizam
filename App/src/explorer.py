from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import re
import shutil
import os

Builder.load_file('App/kivy/explorer.kv')

class PictureFileChooser(Screen):
    pass

class FileChooser(Screen):
        
    def on_enter(self):
        filechooser = self.ids['filechooser']
        filechooser.path = os.path.abspath(os.getcwd())

          
    def save(self, path):
        regex = "([^\\s]+(\\.(?i)(jpe?g|png|gif|bmp))$)"
        p = re.compile(regex)
        if(re.search(p, path)):
            print(path)
            try :
                shutil.copyfile(path, "./IMG.png")
            except:
                pass
            self.manager.get_screen("picturefilechooser").ids.image.reload()
            self.manager.transition.direction = "left"
            self.manager.current = "picturefilechooser"
        else:
            pass      