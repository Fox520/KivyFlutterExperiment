from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import DictProperty

from jnius import autoclass
import utils

KV = '''
#:import utils utils
BoxLayout:
    orientation: "vertical"
    ScrollableLabel:
        text: str(app.custom_data)
        font_size: 50
        text_size: self.width, None
        size_hint_y: None
        height: self.texture_size[1]
    
    Button:
        text: "warm flutter engine (wait 5 seconds)"
        on_release: utils.run_on_ui_thread(utils.warm_up_flutter_engine)

    Button:
        text: "open flutter activity"
        on_release: utils.run_on_ui_thread(utils.open_flutter_activity)

<ScrollableLabel@Label+ScrollView>

'''


class NotificationApp(App):
    custom_data = DictProperty(rebind=True)
    my_temp = None

    def on_start(self, **kwargs):
        pass

    def on_resume(self, **kwargs):
        if self.my_temp is not None:
            self.custom_data = self.my_temp
        else:
            print("onResume: my_temp is None")
        return True

    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    NotificationApp().run()
