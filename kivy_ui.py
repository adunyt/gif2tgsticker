from kivymd.app import MDApp
from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.widget import MDWidget
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.slider import MDSlider
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window

import const
import convert

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

class ConvertData():
    fps = int(const.DEFAULT_FPS)
    resize_mode = const.DEFAULT_RESIZE_MODE
    smart_adjust = const.DEFAULT_SMART_DURATION_LIMIT
    smart_adjust_fallback = const.DEFAULT_FALLBACK_PTS
    crf_value = int(const.DEFAULT_CRF)
    webp2apng_delay = const.DEFAULT_APNG_DELAY

class StickerFactory(MDApp):
    KV_FILES = ["kivy_ui.kv"]
    DEBUG=1
    
    convertData = ConvertData()
    input_file_stack = []
    output_file_stack = []
    
    def build_app(self):
        Window.bind(on_drop_file=self.on_file_drop)
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.accent_palette = "BlueGray"
        return StickerFactoryApp()

    def on_file_drop(self, window, file_path, x, y):
        self.add_file(file_path.decode("utf-8"))
        self.start_convert()
        return
        
    def test(self, *args):
        print(f"test complite. args: {str(args)}")
        
    def add_file(self, filepath):
        self.input_file_stack.append(filepath)
        self.update_input_file_view(filepath)
    
    def pop_file(self):
        filepath = self.input_file_stack.pop()
        self.update_input_file_view(filepath)
        return filepath
    
    
    def add_output_file(self, filepath):
        self.output_file_stack.append(filepath)
        self.update_output_file_view(filepath)
    
    def pop_output_file(self):
        filepath = self.output_file_stack.pop()
        self.update_output_file_view(filepath)
        return filepath
    
    def remove_file_from_input_view(self):
        input_files_widget = self.approot.ids.maingrid.children[0].ids["input_files_grid"]
        input_files_widget.remove_widget(input_files_widget.children[-1])

    def update_input_file_view(self, filepath):
        file_widget = FileItem()
        file_widget.filename = filepath
        input_files_widget = self.approot.ids.maingrid.children[0].ids["input_files_grid"]
        input_files_widget.add_widget(file_widget)
    
    def remove_file_from_output_view(self):
        input_files_widget = self.approot.ids.maingrid.children[0].ids["output_files_grid"]
        input_files_widget.remove_widget(input_files_widget.children[-1])

    def update_output_file_view(self, filepath):
        file_widget = FileItem()
        file_widget.filename = filepath
        input_files_widget = self.approot.ids.maingrid.children[0].ids["output_files_grid"]
        input_files_widget.add_widget(file_widget)
        
    def start_convert(self):
        filepath = self.pop_file()
        convertData = self.convertData
        final_file = convert.process_file(
            filepath=filepath,
            fps_amount=convertData.fps,
            crf=convertData.crf_value,
            fallback_pts=convertData.smart_adjust_fallback,
            resize_mode=convertData.resize_mode,
            smart_limit_duration=convertData.smart_adjust)
        self.add_output_file(final_file)
    
if __name__ == '__main__':
    StickerFactory().run()
