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

class FileType:
    INPUT = 0
    OUTPUT = 1 

class FileStatus:
    NOTREADY = 0,
    READY = 1,
    PROCESSING = 2,
    DONE = 3,
    ERROR = 4

class StickerFactoryApp(MDWidget):
    pass

class VideoSettingsMenu(MDBoxLayout):
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
    input_file_list = []
    output_file_list = []
    
    def build_app(self):
        Window.bind(on_drop_file=self.on_file_drop)
        Window.minimum_width = "800dp"
        Window.minimum_height = "650dp"
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.accent_palette = "BlueGray"
        return StickerFactoryApp()

    def on_file_drop(self, window, file_path, x, y):
        self.add_file(file_path.decode("utf-8"), FileType.INPUT)
        file_to_convert = self.input_file_list[-1]
        
        converted_file = self.start_convert(file_to_convert)
        
        self.remove_file(file_to_convert, FileType.INPUT)
        self.add_file(converted_file, FileType.OUTPUT)
        return
        
    def test(self, *args):
        print(f"test complite. args: {str(args)}")
        
    def add_file(self, filepath: str, file_type: int):
        if file_type is FileType.INPUT:
            self.input_file_list.append(filepath)
        elif file_type is FileType.OUTPUT:
            self.output_file_list.append(filepath)
        self.update_file_widget(file_type)
    
    def remove_file(self, filename: str, file_type: int):
        if file_type is FileType.INPUT:
            target_file_list = self.input_file_list
        elif file_type is FileType.OUTPUT:
            target_file_list = self.output_file_list
        target_file_list.remove(filename)
    
    def update_file_widget(self, file_type: int):
        parent_of_files_widget = self.approot.ids.maingrid.children[0]
        
        if file_type is FileType.INPUT:
            target_widget = parent_of_files_widget.ids["input_files_grid"]
            target_file_list = self.input_file_list
        elif file_type is FileType.OUTPUT:
            target_widget = parent_of_files_widget.ids["output_files_grid"]
            target_file_list = self.output_file_list
        self.clear_all_children(target_widget)
        for file in target_file_list:
            file_widget = FileItem()
            file_widget.filename = file
            target_widget.add_widget(file_widget)
    
    def clear_all_children(self, widget):
        for child in widget.children:
            widget.remove_widget(child)
        
    def start_convert(self, filepath: str):
        convertData = self.convertData
        final_file = convert.process_file(
            filepath=filepath,
            fps_amount=convertData.fps,
            crf=convertData.crf_value,
            fallback_pts=convertData.smart_adjust_fallback,
            resize_mode=convertData.resize_mode,
            smart_limit_duration=convertData.smart_adjust)
        return final_file
    
if __name__ == '__main__':
    StickerFactory().run()
