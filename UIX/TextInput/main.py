#// IMPORT
from os import listdir as Files

from kivy.clock import Clock
from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner, SpinnerOption

from lib.TextInput import TextInput_LN as Text_LN
# from lib.TextEditor import TextEditor as Text_LN
from lib.TextEditor import Font_Default


#// Global Variables
AppTitle:str = "Debugging // Line Numbers"

# Lists of all future needs, like theme changes
StyleItems:list = []
StyleLists:list = []
InfoLists:list = []
# Custom fonts
SpecialFontPath:str = "lib/font/"
SpecialFont:dict = {
    "black":    "angelina",
    "cream":    "CherryCreamSoda",
    "bios":     "8bitOperatorPlus-Bold",
    "hack":     "CONSOLA",
    "twilight": "twilight New Moon",
    "neon":     "neon2"
}

# "theme_name": {"TextInputCustom_Theme_key":"TextInputCustom_Theme_argument"}
sample_color = "38"
ThemeStyle:dict = {
    "dark":    {"color_ln":"606366",        "bg_ln":"313335",
                "color_txt":"A9B7C6",       "bg_txt":"2B2B2B",
                "color_info":"646464",      "bg_info":"262626",
                "color_cursor":"806F9F",    "color_selection":"0066994D",
                "color_scroll":"A6A6A680",  "color_scroll_inactive":"A6A6A647"},

    "black":   {"color_ln":"4D4D4D",        "bg_ln":"121212",
                "color_txt":"9F9F9F",       "bg_txt":"050505",
                "color_info":"383838",      "bg_info":"0D0D0D",
                "color_cursor":"606060",    "color_selection":"5C5C5C4D",
                "color_scroll":"A6A6A647",  "color_scroll_inactive":"5F5F5F47",
                "font_name":SpecialFontPath + SpecialFont["black"],
                "font_size":30},

    "light":   {"color_ln":"999999",        "bg_ln":"F0F0F0",
                "color_txt":"000000",       "bg_txt":"FFFFFF",
                "color_info":"7F7F7F",      "bg_info":"DFDFDF",
                "color_cursor":"000000",    "color_selection":"5974AB4F",
                "color_scroll":"73737380",  "color_scroll_inactive":"73737347"},

    "cream":   {"color_ln":"313335",        "bg_ln":"9D9280",
                "color_txt":"2B2B2B",       "bg_txt":"CCA993",
                "color_cursor":"F74593",    "color_selection":"F7B2D14D",
                "color_scroll":"FFF3DF80",  "color_scroll_inactive":"FFF3DF47",
                "font_name":SpecialFontPath + SpecialFont["cream"]},

    "bios":    {"color_ln":"565656",        "bg_ln":"A0A0A0",
                "color_txt":"FEFEFE",       "bg_txt":"0000AA",
                "color_cursor":"C6C6AA",    "color_selection":"AAAAAA80",
                "color_scroll":"A0A0A080",  "color_scroll_inactive":"A0A0A047",
                "font_name":SpecialFontPath + SpecialFont["bios"]},

    "hack":    {"color_ln":"15717C",        "bg_ln":"0C1C08",
                "color_txt":"00AB00",       "bg_txt":"000000",
                "color_cursor":"C6C6AA",    "color_selection":"00890080",
                "color_scroll":"15717C80",  "color_scroll_inactive":"00890047",
                "font_name":SpecialFontPath + SpecialFont["hack"]},

    "contrast":{"color_ln":"848484",        "bg_ln":"1B1B1B",
                "color_txt":"F8F8F8",       "bg_txt":"141414",
                "color_cursor":"FFFFFF",    "color_selection":"00628080",
                "color_scroll":"FFFFFFBE",  "color_scroll_inactive":"FFFFFFBE"},

    "monokai": {"color_ln":"84847F",        "bg_ln":"2E2F2A",
                "color_txt":"F8F8F2",       "bg_txt":"272822",
                "color_cursor":"F8F8F0",    "color_selection":"57595980",
                "color_scroll":"A6A6A680",  "color_scroll_inactive":"A6A6A647"},

    "twilight":{"color_ln":"909090",        "bg_ln":"1B1B1D",
                "color_txt":"EBEBEB",       "bg_txt":"131314",
                "color_cursor":"A7A7A7",    "color_selection":"3C3F4280",
                "color_scroll":"A6A6A680",  "color_scroll_inactive":"A6A6A647",
                "font_name":SpecialFontPath + SpecialFont["twilight"],
                "font_size":30},

    "neon":    {"color_ln":"6C9E9F",        "bg_ln":"484848",
                "color_txt":"9BC28E",       "bg_txt":"404040",
                "color_cursor":"00FF00",    "color_selection":"348D3480",
                "color_scroll":"00B58047",  "color_scroll_inactive":"A6A6A647",
                "font_name":SpecialFontPath + SpecialFont["neon"],
                "font_size":36}
}

#// LOGIC
class StyleList(DropDown):
    def __init__(self, **kwargs) -> None:
        """StyleList purpose is to have a custom dropdown list to be able to change them any time.

        :param kwargs:  Other arguments for the DropDown/ScrollView.
        :return:        Nothing."""
        global StyleLists

        super(StyleList, self).__init__(**kwargs)

        # Private variables
        # self.__scrolling = False

        # DropDown is inherited from ScrollView, so we set some
        # default style arguments
        self.bar_width = 7
        self.scroll_type = ["bars", "content"]
        self.bar_pos_y = "left"

        # Just to keep the mouse cursor inside the window when scrolling
        # Because when you drag the scroll bar and the cursor get out of window
        # the scrolling will stop until the cursor is inside the window
        self.bind(on_scroll_stop=self._on_scroll_stop, on_scroll_move=self._on_scroll_move)

        # Append itself on a list thant I can access it any time
        StyleLists.append(self)

    def _on_scroll_stop(self, *noUse) -> None:
        Window.ungrab_mouse()
        # if self.__scrolling:
        #     self.__scrolling = False
        #     Window.ungrab_mouse()

    def _on_scroll_move(self, *noUse) -> None:
        Window.grab_mouse()
        # if not self.__scrolling:
        #     self.__scrolling = True
        #     Window.grab_mouse()


class StyleOption(SpinnerOption):
    def __init__(self, **kwargs) -> None:
        """StyleOption purpose is to have a custom dropdown items to be able to change them any time.

        :param kwargs:  Other arguments for the SpinnerOption/Button.
        :return:        Nothing."""
        global StyleItems

        super(StyleOption, self).__init__(**kwargs)

        # Set pressed texture with what ever is on normal state one
        self.background_down = self.background_normal
        # And clear the normal texture after
        self.background_normal = ""
        # Provide a fix font size
        self.font_size = 18

        # Append itself on a list thant I can access it any time
        StyleItems.append(self)


class Style(BoxLayout):
    def __init__(self, textInp:Text_LN, **kwargs) -> None:
        """Style purpose is to create some style options and to apply changes
        of it to the TextInputCustom class.

        :param textInp: The TextInputCustom to apply changes.
        :param kwargs:  Other arguments for the BoxLayout
        :return:        Nothing."""
        global InfoLists

        super(Style, self).__init__(**kwargs)

        # Private variables
        self.__text_input = textInp

        #Create main layouts
        self.layout_option = BoxLayout(height=36, size_hint=(1, None), spacing=3)
        self.layout_info = BoxLayout(height=14, size_hint=(1, None), spacing=3)

        # Define some class arguments
        self.height = self.layout_option.height + self.layout_info.height + self.spacing
        self.size_hint = (1, None)
        self.orientation = "vertical"

        # Create a list for all defined theme style
        themes = [t.capitalize() for t in ThemeStyle.keys()]
        # Create a list with common font sizes
        # Base on text amount and used font, a bigger font size may crash the application... SO NO WORRY
        sizes:list = ["8", "10", "12", "14", "18", "24", "30", "36", "48", "60", "72", "100", "150", "200", "300"]
        # Create a list with all TrueType fonts available in windows
        # On linux I do not know, do it your self if you need it...
        # https://linuxconfig.org/how-to-install-and-manage-fonts-on-linux
        fonts = [file[:-4] for file in Files(r"C:\Windows\fonts") if file.endswith(".ttf")]
        fontsSpecial = [font[:-4] for font in Files(SpecialFontPath[:-1]) if font.endswith((".ttf", ".TTF"))]
        fontsSpecial.append(Font_Default)

        # Style options
        styleFontSize:int = 18
        styleFontName:str = Font_Default
        self.theme = Spinner(text=themes[0], values=themes, width=100, size_hint=(None, 1),
                             font_name=styleFontName, font_size=styleFontSize,
                             option_cls=StyleOption, dropdown_cls=StyleList)

        self.font_name = Spinner(text=fonts[0], values=fonts,
                                 width=180, size_hint=(None, 1),
                                 font_name=styleFontName, font_size=styleFontSize,
                                 option_cls=StyleOption, dropdown_cls=StyleList)

        self.font_special = Spinner(text=fontsSpecial[0], values=fontsSpecial,
                                    width=200, size_hint=(None, 1),
                                    font_name=styleFontName, font_size=styleFontSize,
                                    option_cls=StyleOption, dropdown_cls=StyleList)

        self.font_size = Spinner(text=sizes[sizes.index(str(self.__text_input.font_size))], values=sizes,
                                 width=60, size_hint=(None, 1),
                                 font_name=styleFontName, font_size=styleFontSize,
                                 option_cls=StyleOption, dropdown_cls=StyleList)

        # Try to update the fonts list base on the used font on the text input
        txt_def_font_name:str = self.__text_input.font_name
        try: self.font_special.text = fontsSpecial[fontsSpecial.index(txt_def_font_name)]
        except ValueError: self.font_name.text = fonts[fonts.index(txt_def_font_name)]

        # Style info with the same width as the represented option
        infoFontSize:int = 14
        infoFontName:str = Font_Default
        self.lbl_info_value = Label(text="Font: file\nSize: size", font_name=infoFontName, font_size=infoFontSize,
                                    halign="left", width=100, size_hint=(None, 1))

        self.lbl_theme = Label(text="Theme", font_name=infoFontName, font_size=infoFontSize,
                               width=self.theme.width, size_hint=(None, 1))

        self.lbl_fontOS = Label(text="OS fonts", font_name=infoFontName, font_size=infoFontSize,
                                width=self.font_name.width, size_hint=(None, 1))

        self.lbl_fontCustom = Label(text="Custom fonts", font_name=infoFontName, font_size=infoFontSize,
                                    width=self.font_special.width, size_hint=(None, 1))

        self.lbl_size = Label(text="Size", font_name=infoFontName, font_size=infoFontSize,
                              width=self.font_size.width, size_hint=(None, 1))

        self.lbl_info = Label(text="Info", font_name=infoFontName, font_size=infoFontSize,
                              width=self.lbl_info_value.width, size_hint=(None, 1))

        # Append them to a list for future needs, like color change base on selected theme
        InfoLists.append(self.lbl_theme)
        InfoLists.append(self.lbl_fontOS)
        InfoLists.append(self.lbl_fontCustom)
        InfoLists.append(self.lbl_size)
        InfoLists.append(self.lbl_info)
        InfoLists.append(self.lbl_info_value)

        # Clear the provided background texture, by kivy atlas
        self.theme.background_down = ""
        self.theme.background_normal = ""
        self.font_name.background_down = ""
        self.font_name.background_normal = ""
        self.font_special.background_down = ""
        self.font_special.background_normal = ""
        self.font_size.background_down = ""
        self.font_size.background_normal = ""

        # Bind the text changes base on subject needs
        self.theme.bind(text=self._change_theme)
        self.font_name.bind(text=self._change_font)
        self.font_special.bind(text=self._change_font)
        self.font_size.bind(text=self._change_size)

        # Add them to the layout
        self.add_widget(self.layout_info)
        self.add_widget(self.layout_option)
        self.layout_option.add_widget(self.theme)
        self.layout_option.add_widget(self.font_name)
        self.layout_option.add_widget(self.font_size)
        self.layout_option.add_widget(self.font_special)
        self.layout_option.add_widget(self.lbl_info_value)
        self.layout_info.add_widget(self.lbl_theme)
        self.layout_info.add_widget(self.lbl_fontOS)
        self.layout_info.add_widget(self.lbl_size)
        self.layout_info.add_widget(self.lbl_fontCustom)
        self.layout_info.add_widget(self.lbl_info)

        # Apply the first theme style by default
        self._change_theme()

    def _change_info(self, name:str|None=None, size:str|int|None=None) -> None:
        font_sample:tuple[str, str] = self.lbl_info_value.text.split("\n")
        font_name:str = font_sample[0]
        font_size:str = font_sample[1]
        update_width:bool = False

        # If the name was provided, then update just the font name
        if name is not None:
            self.lbl_info_value.text = f"Font: {name}\n{font_size}"
            update_width = True

        # If the size was provided, then update just the font size
        if size is not None:
            self.lbl_info_value.text = f"{font_name}\nSize: {size}"
        update_width = True

        # If updates was mad it, then update to the new size
        if update_width:
            self.lbl_info_value.texture_update()
            self.lbl_info.width = self.lbl_info_value.width = self.lbl_info_value.texture_size[0]

    def _change_font(self, instance:object, value:str) -> None:
        # Change the font name, but first time check if is a custom one
        # to avoid name conflicts with the system fonts
        try:
            self.__text_input.Theme(font_name=value if value == Font_Default else f"{SpecialFontPath}{value}")
            self._change_info(name=value)
        # In case the font is not a custom one, try with the system one
        except OSError:
            self.__text_input.Theme(font_name=value)
            self._change_info(name=value)

    def _change_size(self, instance:object, value:str) -> None:
        # Change the font size
        try:
            self.__text_input.Theme(font_size=int(value))
            self._change_info(size=value)
        except Exception: pass

    def _change_theme(self, instance:object|None=None, value:str|None=None) -> None:
        # In case the instance is not provided, get the first theme style
        if instance is not None: theme:str = instance.text.lower()
        else: theme:str = [k for k in ThemeStyle.keys()][0]

        sample:str = ""
        font_name_changed:list[bool, str] = [False, ""]
        font_size_changed:list[bool, int] = [False, 0]

        # For every theme style items sample the kwargs
        for key, arg in ThemeStyle[theme].items():
            dec:str = "\"" if type(arg) is str else ""
            sample += f"{key}={dec}{arg}{dec}, "

            # Set text input and window color same as the text background color
            if key == "bg_txt":
                self.__text_input.background_color = arg
                Window.clearcolor = arg

            elif key == "font_name": font_name_changed = [True, arg]
            elif key == "font_size": font_size_changed = [True, arg]

            # Set background color for custom buttons
            # All of them are inherited form kivy Button class at some point (I did revers engineering)
            elif key == "bg_ln":
                self.theme.background_color = arg
                self.font_size.background_color = arg
                self.font_name.background_color = arg
                self.font_special.background_color = arg
                for item in StyleItems: item.background_color = arg + "F7"   # ~97% opacity

            # Set colors for style content base on some provided colors
            elif key == "color_ln":
                self.theme.color = arg
                self.font_size.color = arg
                self.font_name.color = arg
                self.font_special.color = arg
                for item in StyleItems: item.color = arg
            elif key == "color_txt":
                for info in InfoLists: info.color = arg
            elif key == "color_scroll":
                for item in StyleLists: item.bar_color = arg
            elif key == "color_scroll_inactive":
                for item in StyleLists: item.bar_inactive_color = arg

        # Try to execute the text input Theme function with the provided sample
        try:
            exec(f"self._Style__text_input.Theme({sample[:-2]})")

            if not font_name_changed[0]:
                self.__text_input.Theme(font_name=self.font_name.text)
                self._change_info(name=self.font_name.text)
            else:
                sample:list[str] = font_name_changed[1].split("/")
                font:str = sample[-1]
                self._change_info(name=font)
                if sample: self.font_special.text = font

            if not font_size_changed[0]:
                self.__text_input.Theme(font_size=int(self.font_size.text))
                self._change_info(size=self.font_size.text)
            else: self._change_info(size=font_size_changed[1])

        except Exception: pass


class Main(App):
    def __init__(self, **kwargs) -> None:
        # App variables
        self.title = AppTitle

        # Local variables
        self.Sampled: bool = True

        super(Main, self).__init__(**kwargs)
        # Remove touch simulation
        Config.set("input", "mouse", "mouse,multitouch_on_demand")

        # UIX
        self.layout = BoxLayout(orientation="vertical", spacing=3)
        self.MyText = Text_LN(padding_txt=[6,6,23,110])
        self.style = Style(self.MyText, spacing=3)

    def build(self):
        self.MyText.binding(focus=self._on_focus)

        self.layout.add_widget(self.MyText)
        self.layout.add_widget(self.style)

        return self.layout

    def on_start(self):
        # The text size is calculated base on maximum size between text itself and the ScrollView
        # And if we set the text before the app is running the text size will smaller for my tastes
        info:str = """.. INFO ::
        Base on text amount and used font, a bigger font size 
        may crash the application... SO NO WORRY
        This is happen because the rendered texture of the text
        is to big on width and kivy can not handel it by default."""

        files:str = """You can drag and drop some files also...
        P.S.: Ignore the console warning when you drop some files.
        I do not know why is triggered, but I used \"on_drop_file\" and is still is there."""

        needs:str = """I found a small bug on the kivy text input it self and I send an pull request
        to fix that, but just in case if was not fixed yet then:
            > Go to kivy -> uix -> textinput.py
            > Search for line number 2610
            > Change padding index from bottom to top
            > FROM: max_y = self.top - self.padding[3]
            > TO: max_y = self.top - self.padding[1]"""

        Clock.schedule_once(lambda _:(self.MyText.SetText(info, end="\n"*3),
                                      self.MyText.AddText(files, end="\n"*3),
                                      self.MyText.AddText(needs, end="\n"*4),
                                      self.MyText.AddText("I hope was useful.")), 3)

    def _on_focus(self, instance:object, value:bool) -> None:
        if value:

            if not self.Sampled:
                with open(__file__, mode="r", encoding="UTF-8") as file:
                    self.MyText.SetText(file.read())
                    self.Sampled = True

        # else:
        #     self.MyText.Theme(width_ln=True)
        #     self.MyText.Theme(width_ln=56, font_size=12, font_name="symbol")


#// RUN
if __name__ == "__main__":
    Main().run()
