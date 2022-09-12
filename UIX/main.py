#// IMPORT
from logging import warning as WARNING

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import VariableListProperty, NumericProperty, StringProperty, ColorProperty

from kivy.uix.colorpicker import ColorPicker
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner, SpinnerOption

from lib.helper.Font import FontMeasure
from lib.TextInput import TextInput_LN as Text_LN
from lib.OverlayLayout import OverlayLayout


#// Global Variables
AppTitle:str = "Debugging // Line Numbers"

# Lists of all future needs, like color changes
DebugColors:dict[str, list[TextInput, classmethod]] = {}

#// LOGIC
class StyleList(DropDown):
    def __init__(self, **kwargs) -> None:
        super(StyleList, self).__init__(**kwargs)

        self.bar_width = 7
        self.scroll_type = ["bars", "content"]
        self.bar_pos_y = "left"

        self.bind(on_scroll_stop=lambda i,v:Window.ungrab_mouse(), on_scroll_move=lambda i,v:Window.grab_mouse())


class StyleOption(SpinnerOption):
    def __init__(self, **kwargs) -> None:
        super(StyleOption, self).__init__(**kwargs)

        self.background_down = self.background_normal
        self.background_normal = ""
        self.color = "#A9B7C6"
        self.background_color = "#2B2B2BF0"
        self.font_size = 18


class Debug_Items(OverlayLayout):
    key = StringProperty("Key")
    arg = StringProperty("Arg")
    info = StringProperty("Info")
    background_color = ColorProperty("2B2B2B")
    key_color = ColorProperty("606366")
    arg_color = ColorProperty("A9B7C6")
    info_color = ColorProperty("606366")
    info_btn_color = ColorProperty("46484A40")
    font_size = NumericProperty("14sp")
    font_name = StringProperty("lib/font/JetBrainsMono-Regular")
    margins = VariableListProperty([6], length=2)
    margins_info = VariableListProperty([10, 4], length=2)

    def __init__(self, sync, control, **kwargs):
        super(Debug_Items, self).__init__(**kwargs)
        self.fbind("background_color", self.__compute_color)

        self.__sync = sync
        self.__control = control
        self.__showing:bool = False
        self.__height:int = 0

        self.__background = Image(color=self.background_color, allow_stretch=True, keep_ratio=False)
        self.__separator = Image(color="#3F3F3F80", allow_stretch=True, keep_ratio=False
                                 , size_hint=(1, None), height="3dp")
        self.__layout = BoxLayout(orientation="vertical")
        self.__layout_content = BoxLayout(orientation="horizontal")
        self.__key = Label(text=self.key, font_size=self.font_size, font_name=self.font_name
                           , color=self.key_color, padding=self.margins
                           , size_hint=(None, None), bold=True, halign="right")

        self.__arg = TextInput(hint_text_color=self.info_color, cursor_color="#4971D8"
                               , font_size=self.font_size, font_name=self.font_name, multiline=False
                               , background_color=self.background_color, foreground_color=self.arg_color
                               , background_normal = "", background_active = "", on_text_validate=self.on_validate)

        self.__info = Label(font_size=self.font_size, font_name=self.font_name
                            , color=self.info_color, padding=self.margins_info
                            , halign="left", markup=True, size_hint=(None, None))

        self.__btn_info = Button(text="\u25BC", bold=True, font_name=self.font_name
                                 , size_hint=(None, None), color="#4971D8"
                                 , background_normal="", background_down="", background_color=self.info_btn_color)

        self.__btn_update = Button(text="\u00AE", bold=True, font_name=self.font_name
                                   , size_hint=(None, None), color="#C55C2D", background_color=self.info_btn_color
                                   , background_normal="", background_down="")

        self.__btn_default = Button(text="\u00AB", bold=True, font_name=self.font_name
                                    , size_hint=(None, None), color="#F9C26B", background_color=self.info_btn_color
                                    , background_normal="", background_down="", opacity=0)

        self.__warning = Label(text="\u26A0", bold=True, font_name=self.font_name, color="#C55C2D"
                               , size_hint=(None, None), opacity=0)

        self.__prev_L = Image(allow_stretch=True, keep_ratio=False, size_hint=(None, 1))
        self.__prev_R = Image(allow_stretch=True, keep_ratio=False, size_hint=(None, 1))
        self.__prev_T = Image(allow_stretch=True, keep_ratio=False, size_hint=(None, None))
        self.__prev_B = Image(allow_stretch=True, keep_ratio=False, size_hint=(None, None))

        self.__key.texture_update()
        self.__key.size = self.__key.texture_size
        self.__btn_info.size = (self.__key.height, self.__key.height)
        self.__btn_default.size = self.__btn_info.size
        self.__btn_update.size = self.__btn_info.size
        self.__warning.size = self.__btn_info.size
        self.__btn_info.font_size = self.__btn_info.height
        self.__btn_default.font_size = self.__btn_default.height
        self.__btn_update.font_size = self.__btn_update.height
        self.__warning.font_size = self.__key.height
        self.__height = self.__separator.height
        self.__compute_info()

        self.size_hint = (1, None)
        self.height = self.__key.height

        self.add_widget(self.__background)
        self.add_widget(self.__layout)

        self.__layout.add_widget(self.__layout_content)
        self.__layout_content.add_widget(self.__btn_info)
        self.__layout_content.add_widget(self.__key)
        self.__layout_content.add_widget(self.__arg)
        self.__layout_content.add_widget(self.__btn_update)
        self.__layout_content.add_widget(self.__btn_default)
        self.__layout_content.add_widget(self.__warning)

        self.__btn_info.bind(on_press=self._show_info)
        self.__btn_update.bind(on_press=self._update_arg)
        self.__btn_default.bind(on_press=self._restore_default)

        self.__compute_arg()

    def _set_clear_color(self, color) -> None:
        if self.key == "bg_txt":
            Window.clearcolor = color

    def _show_info(self, *noUse) -> None:
        self.__showing = not self.__showing
        if self.__showing:
            self.__layout.add_widget(self.__separator)
            self.__layout.add_widget(self.__info)
            self.height += self.__height
            self.__sync.height += self.__height
            self.__btn_info.text = "\u25B2"

        else:
            self.__layout.remove_widget(self.__separator)
            self.__layout.remove_widget(self.__info)
            self.height -= self.__height
            self.__sync.height -= self.__height
            self.__btn_info.text = "\u25BC"

    def _update_arg(self, *noUse) -> None:
        anim = Animation(font_size=self.__key.height * 1.3, d=.25) \
               + Animation(font_size=self.__btn_update.font_size, d=.25)
        anim.start(self.__btn_update)

        a = self.arg.split("(", 1)
        arg_type, arg_content = a[0], a[1][:-1]
        actual = str(eval(f"self._{self.__class__.__name__}__control.{self.key}"))

        if arg_type in ["BooleanProperty", "NumericProperty", "ColorProperty"]:
            actual = str(actual).replace('"', "").replace("'", "")

        if arg_type == "ColorProperty":
            actual = eval(f"get_hex_from_color({actual})").upper()

            if actual[-2:] == "FF":
                actual = actual[:-2]

        elif arg_type == "ReferenceListProperty":
            sample = str(actual)
            actual = sample.replace("'", "")[1:-1]

        elif arg_type == "VariableListProperty":
            sample = actual[1:-1]

            if "," in sample:
                v = sample.split(",")

                if len(v) == 4 and v[0].strip() == v[2].strip() and v[1].strip() == v[3].strip():
                    if v[0].strip() == v[1].strip(): sample = v[0].strip()
                    else: sample = v[0].strip() + ", " + v[1].strip()

                elif len(v) == 2 and v[0].strip() == v[1].strip():
                    sample = v[0].strip()

            actual = sample

        if actual != self.__arg.hint_text or actual != self.__arg.text != "":
            self.__arg.text = actual
            self.on_validate(self.__arg)

    def _restore_default(self, *noUse) -> None:
        if self.__btn_default.opacity:
            self.__arg.text = ""
            self.on_validate(self.__arg)

    @staticmethod
    def __escape_markup(text:str, invert:bool=False) -> str:
        if invert:
            return text.replace('&amp;', "&").replace("&bl;", "[").replace("&br;", "]")

        return text.replace("&", "&amp;").replace("[", "&bl;").replace("]", "&br;")

    def __compute_color(self, *noUse) -> None:
        self.__background.color = self.background_color

    def __compute_info(self) -> None:
        measure = FontMeasure(self.font_name, self.font_size)
        size = self.width - self.__info.padding[0] * 2
        sample:str = ""
        temp:str = ""
        mark = False
        mark_color = "#666638"

        for line in self.info.splitlines():
            for word in line.split(" "):
                word = word.replace("\\u279c", "\u279c").replace("\\u279C", "\u279c")
                replace = f"{word} "
                start, end = "", ""

                if word != "":
                    # special
                    if "`" in word:
                        mark = True
                        mark_color = "#6A8759"
                        sub = word.split("`")
                        word = sub[1].split(".")[-1]
                        start, end = sub[0], sub[2]

                        for stamp in [":attr:", ":class:", ":meth:", ":func:", ":doc:", ":mod:"]:
                            if stamp in start:
                                start = start.replace(stamp, "")
                                mark_color = "#567B7B"

                        if word == self.key:
                            word = "This"
                            mark_color = "#45529E"

                    # str
                    for sub in ["'", '"']:
                        if sub in word:
                            if word.count(sub) > 1:
                                mark = True
                                start, word, end = word.split(sub)
                                word = sub + word + sub
                                mark_color = "#6A8759"

                    # punctuation
                    if len(word) > 0 and word[0] == "[":
                        start = word[0]
                        word = word[1:]

                    if word[-1] in [".", ",", "!", "?", "]"]:
                        end = word[-1]
                        word = word[:-1]

                        if len(word) > 0 and word[-1] == "]":
                            end = word[-1] + end
                            word = word[:-1]

                    # bool
                    if word in ["True", "False"]:
                        mark = True
                        mark_color = "#C55C2D"

                    # deprecated
                    elif word.lower() == "deprecated":
                        mark = True
                        mark_color = "#FF6B68"

                    # float
                    elif "." in word:
                        x = word.split(".")
                        if x[1].isnumeric() and len(x) == 2:
                            if x[0].isnumeric() or x[0] == "":
                                mark = True
                                mark_color = "#5191A6"
                    # int
                    elif word.isdigit():
                        mark = True
                        mark_color = "#5191A6"

                    if mark:
                        start = self.__escape_markup(start)
                        end = self.__escape_markup(end)
                        word = self.__escape_markup(word)
                        replace = "%s[color=%s]%s[/color]%s " % (start, mark_color, word, end)

                    start = self.__escape_markup(start, True)
                    end = self.__escape_markup(end, True)
                    word = self.__escape_markup(word, True)
                    temp += start + word + end
                    # if self.key == "align_ln": print(measure.get_width_of(temp) < size, size, measure.get_width_of(temp), temp)
                    if measure.get_width_of(temp) < size:
                        sample += replace
                        temp += " "

                    else:
                        temp = f"{start}{word}{end} "
                        sample += f"\n{replace}"

                mark = False

            sample += "\n\n"
            temp = ""

        self.__info.text = sample[:-2]
        # self.__info.text_size = [size, None]
        self.__info.texture_update()
        self.__info.size = self.__info.texture_size
        self.__height += self.__info.height

    def __compute_arg(self) -> None:
        global DebugColors

        a = self.arg.split("(", 1)
        arg_type, arg_content = a[0], a[1][:-1]

        if arg_type in ["BooleanProperty", "NumericProperty", "ColorProperty"]:
            self.__arg.hint_text = arg_content.replace('"', "").replace("'", "")

        if arg_type == "ColorProperty" and arg_content[0] != "#":
            self.__arg.hint_text = "#" + self.__arg.hint_text
            if self.key not in DebugColors.keys():
                DebugColors[self.key] = [self.__arg, self]
                self._set_clear_color(self.__arg.hint_text)

        elif arg_type == "StringProperty":
            self.__arg.hint_text = arg_content.strip()

        elif arg_type == "OptionProperty":
            self.__arg.hint_text = arg_content.split(",", 1)[0].replace('"', "").replace("'", "").strip()

        elif arg_type == "ReferenceListProperty":
            sample = ""
            for s in arg_content.split(","):
                sample += eval(f"self._{self.__class__.__name__}__control.{s.strip()}") + ", "

            self.__arg.hint_text = sample[:-2]

        elif arg_type == "VariableListProperty":
            sample = arg_content.split("]")[0][1:]

            if "," in sample:
                v = sample.split(",")

                if len(v) == 4 and v[0].strip() == v[2].strip() and v[1].strip() == v[3].strip():
                    if v[0].strip() == v[1].strip(): sample = v[0].strip()
                    else: sample = v[0].strip() + ", " + v[1].strip()

                elif len(v) == 2 and v[0].strip() == v[1].strip():
                    sample = v[0].strip()

            self.__arg.hint_text = sample

    def __preview_margin_scroll_cursor(self) -> None:
        cbt = self.__control.bg_txt
        prev_color = [1-c for c in cbt]
        prev_color[3] = 1
        prev_opacity = .5
        target = self.__control._Text.parent.parent

        self.__prev_L.width = self.__control.margin_scroll_cursor[0]
        self.__prev_R.width = self.__control.margin_scroll_cursor[2]
        self.__prev_T.height = self.__control.margin_scroll_cursor[1]
        self.__prev_B.height = self.__control.margin_scroll_cursor[3]

        self.__prev_L.pos = target.pos
        self.__prev_R.pos = (target.right - self.__prev_R.width, target.y)
        self.__prev_T.pos = (target.x + self.__prev_L.width, target.top - self.__prev_T.height)
        self.__prev_B.pos = (target.x + self.__prev_L.width, target.y)

        self.__prev_T.width = target.width - self.__prev_L.width - self.__prev_R.width
        self.__prev_B.width = self.__prev_T.width

        self.__prev_L.color = prev_color
        self.__prev_R.color = prev_color
        self.__prev_T.color = prev_color
        self.__prev_B.color = prev_color

        self.__prev_L.opacity = prev_opacity
        self.__prev_R.opacity = prev_opacity
        self.__prev_T.opacity = prev_opacity
        self.__prev_B.opacity = prev_opacity

        try:
            Window.add_widget(self.__prev_L)
            Window.add_widget(self.__prev_R)
            Window.add_widget(self.__prev_T)
            Window.add_widget(self.__prev_B)

            tm = 1.5
            Clock.schedule_once(lambda dt:Window.remove_widget(self.__prev_L), tm)
            Clock.schedule_once(lambda dt:Window.remove_widget(self.__prev_R), tm)
            Clock.schedule_once(lambda dt:Window.remove_widget(self.__prev_T), tm)
            Clock.schedule_once(lambda dt:Window.remove_widget(self.__prev_B), tm)
        except BaseException: pass

    @property
    def width_key(self):
        return self.__key.width

    @width_key.setter
    def width_key(self, value:int):
        self.__key.text_size = [value, None]
        self.__key.width = value

    def on_validate(self, instance, *args) -> None:
        self.__warning.opacity = 0
        arg_type:str = self.arg.split("(", 1)[0]

        self.__btn_default.opacity = 1 - int(instance.text == instance.hint_text or instance.text == "")

        value:str = instance.text.strip()
        if value == "":
            value = instance.hint_text.strip()

        if "'" in value or '"' in value:
            pass

        elif arg_type == "BooleanProperty":
            value = value.capitalize()

        elif arg_type == "StringProperty":
            if value != "DEFAULT_FONT":
                value = f"\"{value}\""

        elif arg_type == "VariableListProperty":
            value = f"[{value}]"

        elif arg_type == "NumericProperty":
            for metric in ["pt", "mm", "cm", "in", "dp", "sp"]:
                if value.endswith(metric):
                    value = f'"{value.replace(" ", "")}"'

        elif arg_type == "ColorProperty":
            try: self._set_clear_color(value)
            except BaseException: pass

        try: exec(f"self._{self.__class__.__name__}__control.{self.key} = {value}")
        except BaseException:
            try: exec(f"self._{self.__class__.__name__}__control.{self.key} = \"{value}\"")
            except BaseException:
                try:
                    value = "[\"" + value[1:-1].replace(" ", "").replace(",", "\", \"") + "\"]"
                    # value = value.replace("\"", "")
                    exec(f"self._{self.__class__.__name__}__control.{self.key} = {value}")
                except BaseException:
                    try:
                        value = value.replace("\"", "")
                        exec(f"self._{self.__class__.__name__}__control.{self.key} = {value}")
                    except BaseException as err:
                        cls = self.__control.__class__.__name__
                        msg = str(err).replace("(<string>, line 1)", "").strip().capitalize()
                        if msg[-1] not in [".", "?", "!"]: msg += "."

                        WARNING(f"Debugging {cls}: {self.key} = {value} \u279C {msg}")
                        self.__warning.opacity = 1

        if self.key == "margin_scroll_cursor":
            self.__preview_margin_scroll_cursor()


class Debug(OverlayLayout):
    file_name:str = r"lib\TextInput.py"
    kwargs:dict[str, str] = {}
    kwinfos:dict[str, str] = {}
    data_height:int = 0
    font_name:str = "lib/font/JetBrainsMono-Regular"

    def __init__(self, control, **kwargs):
        super(Debug, self).__init__(**kwargs)

        self.__control = control
        self.__initialization:bool = True

        self.__extract_kwargs()

        self.__layout = BoxLayout(orientation="vertical")
        self.__layout_color_picker = OverlayLayout(size_hint=(None, None))
        self.__layout_color_picker_content = BoxLayout(orientation="vertical")
        self.__layout_content = ScrollView(bar_width="10dp", bar_color="#A6A6A6", scroll_type=["bars", "content"])
        self.__layout_data = BoxLayout(orientation="vertical", size_hint=(1, None))
        self.__background = Image(color="#202020", allow_stretch=True, keep_ratio=False)
        self.__background_color_picker = Image(color="#202020", allow_stretch=True, keep_ratio=False)

        self.__title = Label(text=f"Debugging {self.__control.__class__.__name__}"
                             , font_name=self.font_name, font_size="28sp"
                             , color="#94B69E", bold=True, padding=[12, 12], size_hint=(1, None))

        self.__legend = Label(font_name=self.font_name, font_size="28sp", color="#606366", padding=[10, 0]
                              , markup=True, size_hint=(None, None), halign="left", valign="center")

        self.__color_picker = ColorPicker(hex_color="#262626", font_name=self.font_name, size_hint=(None, 1))
        self.__btn_color_picker = Button(text="Show the color picker", bold=True
                                         , font_name=self.font_name, font_size="16sp"
                                         , size_hint=(1, None), height=30
                                         , color="#A6A6A6", background_color="#313335"
                                         , background_normal="", background_down="")

        self.__data_color = Spinner(size_hint=(1, None), font_name=self.font_name, font_size="16sp"
                                    , background_down = "", background_normal = ""
                                    , background_color="#262626", color="#646464"
                                    , option_cls=StyleOption, dropdown_cls=StyleList)

        self.__settings()
        self.__add_widget()
        self.__bind()

        self.__data_color.values = DebugColors.keys()
        self.__data_color.text = self.__data_color.values[0]

    def __settings(self) -> None:
        self.__title.texture_update()
        self.__title.size = self.__title.texture_size

        self.size_hint = (None, 1)
        self.width = max(self.width, self.__title.width + self.__layout_content.bar_width)
        self.__layout_color_picker.size = (self.width, self.__btn_color_picker.height)
        self.__color_picker.width = self.width
        self.__data_color.height = self.__btn_color_picker.height

        self.__legend.text = "[color={color_reload}]{symbol_reload}[/color]{delimiter}" \
                             "[size={info_font_size}]{info_reload}[/size]" \
                             "\n[color={color_restore}]{symbol_restore}[/color]{delimiter}" \
                             "[size={info_font_size}]{info_restore}[/size]" \
                             "\n[color={color_warning}]{symbol_warning}[/color]{delimiter}" \
                             "[size={info_font_size}]{info_warning}[/size]".format(
            symbol_reload = "\u00AE",
            symbol_restore = "\u00AB",
            symbol_warning = "\u26A0",
            delimiter = "[size=20] \u279C [/size]",
            color_reload = "#C55C2D",
            color_restore = "#F9C26B",
            color_warning = "#C55C2D",
            info_font_size = 17,
            info_reload = "Retrieving the real used value.",
            info_restore = "Change back to the default value.",
            info_warning = "An warning message was triggered."
        )
        self.__legend.texture_update()
        self.__legend.size = self.__legend.texture_size

    def __add_widget(self) -> None:
        self.add_widget(self.__background)
        self.add_widget(self.__layout)
        self.__layout.add_widget(self.__layout_content)
        self.__layout.add_widget(self.__layout_color_picker)

        self.__layout_color_picker.add_widget(self.__background_color_picker)
        self.__layout_color_picker.add_widget(self.__layout_color_picker_content)
        self.__layout_color_picker_content.add_widget(self.__btn_color_picker)

        self.__layout_content.add_widget(self.__layout_data)
        self.__layout_data.add_widget(self.__title)
        self.__layout_data.add_widget(self.__legend)
        self.__compute_data()

    def __bind(self) -> None:
        self.__layout_content.bind(on_scroll_move=self._on_scroll_move, on_scroll_stop=self._on_scroll_stop)
        self.__btn_color_picker.bind(on_press=self._show_color_picker)
        self.__color_picker.bind(color=self._on_color)
        self.__data_color.bind(text=self._set_color)

    @staticmethod
    def _on_scroll_stop(*noUse) -> None:
        Window.ungrab_mouse()

    @staticmethod
    def _on_scroll_move(*noUse) -> None:
        Window.grab_mouse()

    def _show_color_picker(self, *noUse) -> None:
        try:
            self.__layout.remove_widget(self.__layout_content)

            self.__layout_color_picker_content.add_widget(self.__data_color)
            self.__layout_color_picker_content.add_widget(self.__color_picker)

            self.__btn_color_picker.text = "Hide the color picker"
            self.__layout_color_picker.size_hint_y = 1

        except BaseException:
            self.__layout.add_widget(self.__layout_content, index=1)

            self.__layout_color_picker_content.remove_widget(self.__data_color)
            self.__layout_color_picker_content.remove_widget(self.__color_picker)

            self.__btn_color_picker.text = "Show the color picker"
            self.__layout_color_picker.size_hint_y = None
            self.__layout_color_picker.height = self.__btn_color_picker.height

    def _on_color(self, instance:ColorPicker, value) -> None:
        color = instance.hex_color
        if color[-2:].lower() == "ff": color = color[:-2]
        if color.lower() == DebugColors[self.__data_color.text][0].hint_text.lower(): color = ""

        DebugColors[self.__data_color.text][0].text = color.upper()
        DebugColors[self.__data_color.text][1].on_validate(DebugColors[self.__data_color.text][0])

    def _set_color(self, *noUse) -> None:
        color = DebugColors[self.__data_color.text][0].text

        if color == "":
            color = DebugColors[self.__data_color.text][0].hint_text

        self.__color_picker.hex_color = color

    def __compute_data(self) -> None:
        index:int = 0
        k_width:int = 0
        self.data_height:int = self.__title.height + self.__legend.height
        for k,a in self.kwargs.items():
            bg = "#26262688" if index % 2 else "#31333588"
            data = Debug_Items(key=k, arg=a, info=self.kwinfos[k], width=self.width, background_color=bg
                               , sync=self.__layout_data, control=self.__control)

            k_width = max(k_width, data.width_key)
            self.data_height += data.height

            self.__layout_data.add_widget(data)
            index += 1

        for ka in self.__layout_data.children:
            if isinstance(ka, Debug_Items):
                ka.width_key = k_width

        self.__layout_data.height = self.data_height

    def __extract_kwargs(self) -> None:
        with open(self.file_name, mode="r", encoding="UTF-8") as file:
            line = file.readline()
            extract_kwargs:bool = False
            extract_info:bool = False
            key:str = ""

            while line:
                sample = line.strip()
                if sample.startswith("class "): extract_kwargs = True

                elif sample.startswith("def "): break

                elif extract_kwargs:
                    if sample.startswith("'''") or sample.startswith('"""'):
                        extract_info = not extract_info
                        if extract_info: sample = sample[3:]

                    if extract_info:
                        if sample == "": info = "\n"
                        else: info = sample + " "

                        if key in self.kwinfos.keys(): self.kwinfos[key] += info
                        else: self.kwinfos[key] = info

                    else:
                        try:
                            k, a = sample.split("=", 1)
                            key = k.strip()
                            self.kwargs[key] = a.strip()
                        except: pass

                line = file.readline()


class Main(App):
    def __init__(self, **kwargs) -> None:
        super(Main, self).__init__(**kwargs)
        # Remove touch simulation
        Config.set("input", "mouse", "mouse,multitouch_on_demand")

        # App settings
        self.title = AppTitle
        Window.minimum_width, Window.minimum_height = 1024, 384
        Window.size = (max(Window.width, Window.minimum_width), max(Window.height, Window.minimum_height))
        # Window.fullscreen = "auto"

        # Local variables
        self.Sampled: bool = False

        # UIX
        self.layout = BoxLayout(orientation="vertical", spacing=3)
        self.layout_content = BoxLayout(orientation="horizontal")
        self.MyText = Text_LN(padding_txt=[6,6,23,110])
        self.debug = Debug(self.MyText, width=425)

        self.MyText.binding(focus=self._on_focus)
        # self.MyText.size_hint = (None, None)

    def build(self):
        self.layout_content.add_widget(self.MyText)
        self.layout_content.add_widget(self.debug)
        self.layout.add_widget(self.layout_content)

        return self.layout

    def on_start(self):
        # The text size is calculated base on maximum size between text itself and the ScrollView
        # And if we set the text before the app is running the text size will smaller for my tastes
        info:str = ".. INFO ::" \
                   "\n\tBase on text amount and used font, a bigger font size" \
                   "\n\tmay crash the application... SO NO WORRY" \
                   "\n\tThis is happen because the rendered texture of the text" \
                   "\n\tis to big on width and kivy can not handel it by default."

        files:str = "You can NOT drag and drop any more (for now)...\n" \
                    "Also check the documentation. In case you do not understand something.\n\n" \
                    "https://github.com/kmcasi/Python_Kivy/blob/main/UIX/TextInput/README.md#warning-note"

        needs:str = "I found a small bug on the kivy text input it self and I send an pull request\n" \
                    "to fix that, but just in case if was not fixed yet then:" \
                    "\n\t> Go to kivy -> uix -> textinput.py" \
                    "\n\t> Search for line number 2610" \
                    "\n\t> Change padding index from bottom to top" \
                    "\n\t> FROM: max_y = self.top - self.padding[3]" \
                    "\n\t> TO: max_y = self.top - self.padding[1]"

        useful:str = "If you found it useful is not to much if I ask to vote my stackoverflow answer as useful?\n" \
                     "This will increase my reputation on that platform. Thanks in advance.\n\n" \
                     "https://stackoverflow.com/a/72918353/10234009"

        Clock.schedule_once(lambda _:(self.MyText.SetText(info, end="\n"*3),
                                      self.MyText.AddText(files, end="\n"*3),
                                      self.MyText.AddText(needs, end="\n"*4),
                                      self.MyText.AddText(useful)), 3)

        # DEBUG: cursor position for auto scrolling
        # debug:str = ""
        # rows:int = 126
        # sample:str = f"Some text for debug in the line number %.{len(str(rows))}d\n".replace(" ", " - "*15)
        # for i in range(rows): debug += sample % (i+1)
        # Clock.schedule_once(lambda _: (self.MyText.SetText(debug[:-1], end=None)), 3)

    def _on_focus(self, instance:object, value:bool) -> None:
        if value:
            if not self.Sampled:
                with open(__file__, mode="r", encoding="UTF-8") as file:
                    self.MyText.SetText(file.read())
                    self.Sampled = True
                    self.title += f" ({__file__})"


#// RUN
if __name__ == "__main__":
    Main().run()
