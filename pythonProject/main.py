from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm

if __name__ == '__main__':
    MyApp().run()
