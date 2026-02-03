from kivy.config import Config
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '700')

from app.app import ProcessoApp

if __name__ == '__main__':
    ProcessoApp().run()