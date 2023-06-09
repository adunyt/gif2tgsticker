# from kivymd.app import MDApp
from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.widget import MDWidget
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.slider import MDSlider
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.textfield import MDTextField

from kivy.properties import NumericProperty

class TwoLineIconSliderListItem(TwoLineAvatarIconListItem):
    pass
    
class TwoLineIconCheckBoxListItem(TwoLineAvatarIconListItem):
    pass

class StickerFactoryApp(MDWidget):
    pass

class VideoSettingsMenu(MDGridLayout):
    pass

class FilesPanel(MDGridLayout):
    pass

class RightWidgetBoxLayout(IRightBodyTouch, MDBoxLayout):
    pass

class RightWidgetTextField(IRightBodyTouch, MDTextField):
    pass

class RightWidgetSlider(IRightBodyTouch, MDSlider):
    pass

class FileItem(MDBoxLayout):
    pass

class StickerFactory(MDApp):
    KV_FILES = ["kivy_ui.kv"]
    DEBUG=1
    def build_app(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.accent_palette = "BlueGray"
        return StickerFactoryApp()


if __name__ == '__main__':
    StickerFactory().run()