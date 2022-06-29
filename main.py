from App.src import app, camera, explorer, model_dowloader, error, login_signup
from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
import os
 
Config.set('graphics', 'width', '340')
Config.set('graphics', 'height', '700')

sm = ScreenManager()
           
class Error(App):
    def build(self):
        sm.add_widget(error.InternetError(name="interneterror"))
        return sm
                       
class App(App):
    def build(self):
        
        os.environ["mode_model"] = "FR"
        sm.add_widget(login_signup.Login(name='login'))
        sm.add_widget(login_signup.SignUp(name='signup'))
        sm.add_widget(app.Home(name='home'))
        sm.add_widget(app.BirdCard(name="birdcard"))
        sm.add_widget(app.Loading(name='loading'))
        sm.add_widget(app.LoadApp(name='loadapp'))
        sm.add_widget(camera.CameraView(name='cameraview'))
        sm.add_widget(camera.PictureCamera(name="picturecamera"))
        sm.add_widget(explorer.PictureFileChooser(name="picturefilechooser"))
        sm.add_widget(explorer.FileChooser(name="filechooser"))
        return sm

if __name__ == "__main__":
    requierement = False
    try:
        path = 'App/data/model_fr.h5'
        if (os.path.exists(path) != True):
            model_dowloader.download_file_from_google_drive("1RZA08cBoC7zYIpkioavaQ7Baottkn44r", path)
        path = 'App/data/model_us.h5'
        if (os.path.exists(path) != True):
            model_dowloader.download_file_from_google_drive("1hGQHUy3tS7xHEvbwqZ6rLmN72o2loPCg", path)
        path = 'App/data/OiseauxFini.csv'
        if (os.path.exists(path) != True):
            model_dowloader.download_file_from_google_drive("1xRyuTuv7tSQHYrsGx1EJmSrcaAqY8X79", path)
        requierement = True
    except:
        pass
    if requierement:
        application =  App()
        application.run()
    else:
        application =  Error()
        application.run()