#// IMPORT
from kivy.app import App
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.properties import ColorProperty, NumericProperty

from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

"""
The line numbers are bind on key up to use less processes like:
    L_CTRL, R_CTRL, Enter, Numpad Enter, Backspace, Delete,
    CTRL+V, CTRL+X, CTRL+Z and CTRL+Y for now.
    
    In my kivy source code I changed redo from CTRL+R to CTRL+Y. In case you 
    want to use R instead of V (or what ever is your redo bind) then go an look 
    for '_on_key_up' event and you will find what line and replace the key code.

Line numbers width are changed dynamically if is need it so you can set 'width_line'
to sero to get just the required width.

.. TODO::
    []  Fix the cursor position reset when the font_name and/or font_size are changed
        on run time.
    []  Adding multithreading to improve the speed of line numbers response. In this
        stage, if we are pasting a lot of text, the app will frees until the line 
        numbers are are updated. If you do not copy-paste huge text will be fine
        because the line numbers ar added and subtracted base on your keyboard key.
        Any way, will be much useful to add 4000+ in 1-2 sec maximum or faster.
        I did some test on my old laptop and because is an old one, if I can
        make it faster for him, than will be greate. Off course the hardware
        is important to on this tests.
        
        TIME  | PASTED LINES
        0m07s |  600+
        0m13s | 1000+
        0m43s | 2000+
        1m26s | 3000+
        2m50s | 4000+
        
        Laptop: Windows 10 PRO N, 21H2, 64-bit
                HD Graphics 620
                i3-7100U CPU, 2.4 GHz, 2 Cores, 4 Threads, L3 cache: 3MB
                8 GB RAM DDR3 (1.2-2 GB usable)
"""

#// LOGIC
class Font:
    def __init__(self, font_name:str, font_size:int, sample:str="W"):
        """**Font** purpose is to measure the size of a font single letter.

        You can get as return the width and height as integer or size as list of integers.

        >>> # "Z" is optionally, is the sample character
        >>> measure = Font("comic", 18, "Z")
        >>> print(measure.width, measure.height)
        >>> print(measure.size)

        :param font_name:   Font name as a string
        :param font_size:   Font size as an integer
        :param sample:      Character sample as a string. Default is "W", usually is the bigger character.
        """
        # Private variables
        self.__name = font_name
        self.__size = font_size
        self.__sample = sample

        # Local variables
        self.width:int  = 0
        self.height:int = 0
        self.size:tuple[int, int] = (self.width, self.height)

        self._measuring()

    def _measuring(self):
        sample = Label(text=self.__sample, font_name=self.__name, font_size=self.__size)
        sample.texture_update()

        self.width, self.height = sample.texture_size
        self.size = sample.texture_size


def List(*values:any, _len:int=4, _type:type=int) -> list:
    """**List** purpose is to return a list of elements.
    You can provide and unpair values like from 3 values get out 4.

    Main reaso was because kivy *VariableListProperty* had not worked for me for some reasons ``\(-_-)/``.

    Accepted values and the return type are: int, float, str, bool.
    See extreme example below:

    >>> List(3)                             # [3, 3, 3, 3]
    >>> List(1, 2.3, _type=float)           # [1.0, 2.3, 1.0, 2.3]
    >>> List(0.6, "a", False, _len=5)       # [1, 97, 0, 1, 97]
    >>> List(0.3, "z", _len=2, _type=bool)  # [False, True]
    >>> List(0.3, 2, True, "a", _type=str)  # ['0.3', '2', 'True', 'a']

    :param values:  The value(s) provided.
    :param _type:   The type of list elements.
    :param _len:    The amount of list elements.
    """
    out:list = []
    keep:bool = True
    while keep:
        for index in range(len(values)):
            if _type == int and type(values[index]) is str: value = ord(values[index])
            elif _type == float and type(values[index]) is str: value = float(ord(values[index]))
            else: value = values[index]
            try:

                out.append(_type(value))

                if len(out) == _len: keep = False; break
            except Exception as e: raise Exception(e)

    return out



class TextInputCustom(ModalView):
    def __init__(self, width_line:NumericProperty=32, font_name:str="comic", font_size:NumericProperty=18
                 , color_line:ColorProperty="#606366", color_text:ColorProperty="#A9B7C6"
                 , color_cursor:ColorProperty="#606366", color_selection:ColorProperty="#0066994D"
                 , bg_line:ColorProperty="#313335", bg_text:ColorProperty="#2B2B2B"
                 , padding_line:List=6, padding_text:List=6
                 , **kwargs):
        """Custom TextInput class with line numbers.

        .. NOTE::
            If you are useeing **bind** you will control the parent class witch
            is **ModalView**. If you want to control the TextInput bind use **binding**.
            Like and example see below.

            >>> self.myText = TextInputCustom()
            >>> self.myText.binding(text=self.your_text_bind)
        """
        # Local variables
        self.color_line = color_line
        self.color_text = color_text
        self.color_cursor = color_cursor
        self.color_selection = color_selection
        self.bg_line = bg_line
        self.bg_text = bg_text
        self.width_line = width_line
        self.font_name = font_name
        self.font_size = font_size
        self.padding_line = padding_line
        self.padding_text = padding_text

        # Private variables
        self.__lines:int = 1
        self.__lines_width_min:NumericProperty = 0
        self.__ctrl:bool = False
        self.__focused:bool = False
        self.__unredo:dict[str, bool] = {"undo":False, "redo":False}
        self.__cursor:tuple[int, int] = (0, 0)
        self.__filename:list = []

        super(TextInputCustom, self).__init__(**kwargs)

        # UIX elements
        self._Layout = BoxLayout(orientation="horizontal")
        self._Lines = TextInput(text="1", width=self.width_line, is_focusable=False, do_wrap=False, halign="right",
                                background_color=self.bg_line, foreground_color=self.color_line,
                                font_name=self.font_name, font_size=self.font_size, padding=self.padding_line)
        self._Text = TextInput(auto_indent=True, do_wrap=False,
                               selection_color=self.color_selection, cursor_color=self.color_cursor, cursor_width=2.5,
                               background_color=self.bg_text, foreground_color=self.color_text,
                               font_name=self.font_name, font_size=self.font_size, padding=self.padding_text)

        # Determinate the line numbers width dynamically
        # if provided one is zero less.
        self._find_font_size()
        if self.width_line < 1: self._LineNumber_AutoWidth()

        # Set filling size
        self._Lines.size_hint = (None, 1)
        self._Text.size_hint = (1, 1)

        # Add them to the layout
        self._Layout.add_widget(self._Lines)
        self._Layout.add_widget(self._Text)
        self.add_widget(self._Layout)

        # Binds
        self._Text.bind(focus=self._check_is_focus)
        Window.bind(on_key_down=self._on_key_down, on_key_up=self._on_key_up)
        Window.bind(on_drop_file=self._on_drop_file, on_drop_end=self._on_drop_end)

    def binding(self, **kwargs):
        """Useful for controlling text binding.

        The key arguments are the same as **TextInput** ones because by calling this,
        in fact you are calling **TextInput.bind** from inside this class."""
        self._Text.bind(**kwargs)

    def _check_is_focus(self, instance, value): self.__focused = value

    def _on_drop_file(self, window, filename, x, y): self.__filename.append(filename)

    def _on_drop_end(self, window, x, y): self._DropFile_Open()

    def _on_key_down(self, window, keycode, _, text, modifiers):
        # Checking only if the text input is focused/clicked
        if self.__focused:
            self.__ctrl = "ctrl" in modifiers

    # Checked here to let you do your job and just after to update the line numbers.
    # This way get less calculations, by compromising the speed of line numbers update.
    def _on_key_up(self, window, keycode, _):
        # Checking only if the text input is focused/clicked
        if self.__focused:
            # [Enter, Numpad Enter]
            if keycode in [13, 271]:
                self._LineNumber_Add(amount=1)
                # Same reason as on [L_CTRL, R_CTRL] (las if statement)
                self._LineNumber_Unknown()

            # [Backspace, Delete]
            elif keycode in [8, 127]:
                try:
                    # After a substring was deleted, we check the undo dummy to see
                    # if was some lines, and we subtract that amount of lines.
                    # Last undo item suppose to be of type backspace or delete, so
                    # we use the right pattern without checking it.
                    item:dict = self._Text._undo[-1]
                    substring:str = item["undo_command"][2]
                    self._LineNumber_Subtract(substring)

                # If we got an int instead of str or an empty list, do nothing
                except TypeError: pass
                except IndexError: pass
                # Same reason as on [L_CTRL, R_CTRL] (las if statement) + is possible
                # to have something selected when you pressed this key(s).
                self._LineNumber_Unknown()

            # CTRL + V
            elif self.__ctrl and keycode == 118:
                self._LineNumber_Add(Clipboard.paste())

                if not self.__unredo["undo"]: self.__unredo["undo"] = True

            # CTRL + X
            elif self.__ctrl and keycode == 120:
                self._LineNumber_Subtract(Clipboard.paste())

                if not self.__unredo["undo"]: self.__unredo["undo"] = True

            # CTRL + Z
            elif self.__ctrl and keycode == 122:
                # Copy & Paste are the same, just adding and subtracting are inverted
                try:
                    # If undo dummy is not empty, we make sore the "undo" flag is True
                    if len(self._Text._undo) > 0: self.__unredo["undo"] = True

                    # Otherwise, if the undo dummy is empty, and we already got the last itme
                    # pass this check by raising and IndexError
                    elif not self.__unredo["undo"]: raise IndexError

                    # if not self.__unredo["redo"]: self.__unredo["redo"] = True

                    # Get the last undo item from redo and the type of it
                    item:dict = self._Text._redo[-1]
                    _type:str = item["undo_command"][0]

                    # If type comes from backspace or delete, add the line numbers from substring
                    if _type in ["bkspc", "delsel"]:  self._LineNumber_Add(item["undo_command"][2])
                    # Otherwise, if the type is insert, subtract the line numbers from substring
                    elif _type == "insert": self._LineNumber_Subtract(item["redo_command"][1])

                    # Because undo dummy was empty before we started this check we
                    # set "undo" flag as False to know that was the last item of the list
                    if len(self._Text._undo) == 0: self.__unredo["undo"] = False

                # If we got an int instead of str or an empty list, do nothing
                except TypeError: pass
                except IndexError: pass

            # I changed the kivy source code from R to Y, but if you still want
            # to use original CTRL + R, then change keycode from 121 to 114.
            # CTRL + Y
            elif self.__ctrl and keycode == 121:
                # Copy & Paste are the same, just adding and subtracting are inverted
                try:
                    # If redo dummy is not empty, we make sore the "redo" flag is True
                    if len(self._Text._redo) > 0: self.__unredo["redo"] = True

                    # Otherwise, if the redo dummy is empty, and we already got the last itme
                    # pass this check by raising and IndexError
                    elif not self.__unredo["redo"]: raise IndexError

                    # Get the last redo item from undo and the type of it
                    item:dict = self._Text._undo[-1]
                    _type:str = item["undo_command"][0]

                    # If type comes from backspace or delete, subtract the line numbers from substring
                    if _type in ["bkspc", "delsel"]: self._LineNumber_Subtract(item["undo_command"][2])
                    # Otherwise, if the type is insert, add the line numbers from substring
                    elif _type == "insert": self._LineNumber_Add(item["redo_command"][1])

                    # Because redo dummy was empty before we started this check we
                    # set "redo" flag as False to know that was the last item of the list
                    if len(self._Text._redo) == 0: self.__unredo["redo"] = False

                # If we got an int instead of str or an empty list, do nothing
                except TypeError: pass
                except IndexError: pass

            # Because line numbers are calculated on key up, is a possibility
            # to hold a key, and you can add/subtract more lines than one time.
            # So here we will make sore the line numbers are match.
            # [L_CTRL, R_CTRL]
            elif keycode in [305, 306]: self._LineNumber_Unknown()

    def _LineNumber_Unknown(self):
        """This is a helper to recalculate the line numbers."""
        reference:int = len(self._Text.lines)

        # If the reference is bigger than the (line number different from zero)
        if reference > self.__lines > 0:
            # Add just the difference
            self._LineNumber_Add(amount=reference - self.__lines)

        # If the reference is less than the line number
        elif reference < self.__lines:
            # Subtract just the difference
            self._LineNumber_Subtract(amount=self.__lines - reference)

        # Otherwise, write line numbers from scratch base on the reference.
        # Most of the time this will be call it when the line numbers and/or
        # the reference are 0 (zero) and will add that "1" line number.
        elif self.__lines != reference or self.__lines < 0:
            print("?")
            self._Lines.text = "1"

            for line in range(2, reference + 1):
                self._Lines.text += f"\n{line}"

            self.__lines = reference

        self._LineNumber_AutoWidth()

    def _LineNumber_Add(self, substring=None, amount:int=0):
        """Add the line numbers

        :param amount:  The amount of subtraction."""
        # In case the substring is provided, get amount of lines
        if substring is not None and "\n" in substring:
            # Subtraction need it overall, just on the first line number we need the
            # full amount... If we are at the beginning of the file, the split amount
            # is right, but when we are after that, an extra line number will appear
            # "from nowhere" (#math), so we will subtract one all the time mostly.
            amount = len(substring.split("\n")) - (0 if self.__lines == 0 else 1)

        for line in range(1, amount + 1):
            self._Lines.text += f"\n{self.__lines + line}"

        # Update the line numbers
        self.__lines += amount

    def _LineNumber_Subtract(self, substring=None, amount:int=0):
        """Subtract the line numbers

        :param amount:  The amount of subtraction."""
        # In case the substring is provided, get amount of lines
        if substring is not None and "\n" in substring:
            amount = len(substring.split("\n")) - 1

        lines:list = self._Lines.text.rsplit("\n", amount)
        self._Lines.text = lines[0]

        # Update the line numbers
        self.__lines -= amount

    def _LineNumber_UpdateGraphics(self) -> None:
        """**UpdateGraphics_LineNumber** purpose is to sync line numbers scroll_y
        value with the text one and to update the graphics for the line numbers."""
        self._Lines.scroll_y = self._Text.scroll_y
        self._Lines._trigger_update_graphics()

    def on_touch_up(self, touch):
        """**Scrolling event**

        Let you scroll the text but not the line numbers. They are synced with the text."""
        self._Text.on_touch_up(touch)
        self._LineNumber_UpdateGraphics()

    def on_touch_down(self, touch):
        """**Scrolling event**

        Let you scroll the text but not the line numbers. They are synced with the text."""
        self._Text.on_touch_down(touch)
        self._LineNumber_UpdateGraphics()


    def _DropFile_Open(self):
        files_count:int = len(self.__filename)

        if files_count == 1:
            try:
                with open(self.__filename.pop(), mode="rb", buffering=4096) as file:
                    self._Text.insert_text(file.read())
                self._LineNumber_Unknown()
            finally: file.close()

        # Same as above but in a range loop and + file name decorator for visual split
        else:
            for index in range(files_count):
                try:
                    with open(self.__filename[index], mode="rb", buffering=4096) as file:
                        dec, name = "=-", str(file.name)[2:-1].replace("\\\\", "\\")
                        self._Text.insert_text("\n\n#//{dec}[ {name} ]{dec}\\\\#\n\n".format(
                            name=name, dec=(dec * ((56 - len(name)) // 2))[:-1]))
                        self._Text.insert_text(file.read())
                finally:
                    file.close()
            self.__filename.clear()
            self._LineNumber_Unknown()


    def _LineNumber_AutoWidth(self):
        """Set the maximum line number with need it to show up.

        If required more space will extrude, otherwise will use the provided width line."""
        pad = (self.padding_line[0], self.padding_line[2 if len(self.padding_line) > 3 else 1])

        required = pad[0] + self.__lines_width_min * len(str(self.__lines)) + pad[1]
        self._Lines.width = max(self.width_line, required)

    def _find_font_size(self):
        """Calculate the minimum width need it to display one character."""
        sample = Font(self.font_name, self.font_size, "7")
        self.__lines_width_min = sample.width

    def Theme(self, **kwargs) -> None:
        """**Theme** let you change the style dynamically with some custom
        key arguments like:

        [type: NumericProperty]
            width_line, font_size
        [type: str]
            font_name
        [type: ColorProperty]
            color_line, color_text, color_cursor, color_selection, bg_line, bg_text

        .. Note::
            Other key arguments can be provided, but they will be applied for both
            (line numbers and text) if is possible.
        """
        update:bool = False

        if "width_line" in kwargs:
            self.width_line = kwargs["width_line"]
            self._Lines.width = self.width_line
            self._LineNumber_AutoWidth()
            kwargs.pop("width_line")
            update = True

        if "color_line" in kwargs:
            self.color_line = kwargs["color_line"]
            self._Lines.foreground_color = self.color_line
            kwargs.pop("color_line")
            update = True

        if "color_text" in kwargs:
            self.color_text = kwargs["color_text"]
            self._Text.foreground_color = self.color_text
            kwargs.pop("color_text")
            update = True

        if "color_cursor" in kwargs:
            self.color_cursor = kwargs["color_cursor"]
            self._Text.cursor_color = self.color_cursor
            kwargs.pop("color_cursor")
            update = True

        if "color_selection" in kwargs:
            self.color_selection = kwargs["color_selection"]
            self._Text.selection_color = self.color_selection
            kwargs.pop("color_selection")
            update = True

        if "bg_line" in kwargs:
            self.bg_line = kwargs["bg_line"]
            self._Lines.background_color = self.bg_line
            kwargs.pop("bg_line")
            update = True

        if "bg_text" in kwargs:
            self.bg_text = kwargs["bg_text"]
            self._Text.background_color = self.bg_text
            kwargs.pop("bg_text")
            update = True

        if "font_name" in kwargs:
            self.font_name = kwargs["font_name"]
            self._Lines.font_name = self.font_name
            self._Text.font_name = self.font_name
            self._find_font_size()
            kwargs.pop("font_name")
            update = True

        if "font_size" in kwargs:
            self.font_size = kwargs["font_size"]
            self._Lines.font_size = self.font_size
            self._Text.font_size = self.font_size
            self._find_font_size()
            kwargs.pop("font_size")
            update = True

        if "padding_line" in kwargs:
            self.padding_line = kwargs["padding_line"]
            self._Lines.padding = self.padding_line
            kwargs.pop("padding_line")
            update = True

        if "padding_text" in kwargs:
            self.padding_text =kwargs["padding_text"]
            self._Text.padding = self.padding_text
            kwargs.pop("padding_text")
            update = True

        # If is something not custom like above then try to apply them
        # for both of then (line numbers and text itself)
        if len(kwargs.keys()) > 0:
            for key, value in kwargs.items():
                decorator:str = "\"" if type(value) == str else ""
                for uix in ["_Lines", "_Text"]:
                    try:
                        exec(f"self.{uix}.{key} = {decorator}{value}{decorator}")
                        update = True
                    except Exception: pass

        # Updating graphics just if is need it
        if update:
            self._Lines._trigger_update_graphics()
            self._Text._trigger_update_graphics()

    def SetText(self, text:str) -> None:
        """**SetText** let you setting a new text by replacing the
        old one with the provided one.

        :param text:    The new text as a string type.
        :return:        Nothing.

        >>>  with open(__file__, mode="r", encoding="UTF-8") as file:
        >>>      self.MyText = TextInputCustom()
        >>>      self.MyText.SetText(file.read())
        """
        self._Text.text = text
        self._LineNumber_Unknown()

    def GetText(self) -> str:
        """**GetText** give you the inside text.

        :return:    The text variable of type string (from kivy AliasProperty)."""
        return self._Text.text



#// RUN
if __name__ == "__main__":
    class Main(App):
        def __init__(self, **kwargs):
            #Local variable
            self.Sampled:bool = False

            super(Main, self).__init__(**kwargs)


        def build(self):
            # App arguments
            self.title = "Debugging // Line Numbers"

            # UIX
            self.layout = BoxLayout()
            self.MyText = TextInputCustom(width_line=0, padding_line=List(3, _len=2))
            self.MyText.SetText("(Drag & Drop some files...)\n\nI hope was useful.\n")

            # Debug: Changing color on click inside and outside of text input
            self.MyText.binding(focus=self.on_focus)

            self.layout.add_widget(self.MyText)

            return self.layout


        def on_focus(self, instance, value):
            # As a hint just for you to know from where kivy is take it
            # kivy can use and fonts from your OS and is looking for an TTF extension
            # Font: comic   -> "C:\Windows\Fonts\Comic Sans MS\comic.ttf"
            # Font: symbol  -> "C:\Windows\Fonts\Symbol Regular\symbol.ttf"

            if value:
                # TODO: Fix cursor jump when font (name and/or size) changing on focus
                self.MyText.Theme(#font_name="comic", font_size=18,
                                  color_line="#313335", bg_line="#606366",
                                  color_text="#2B2B2B", bg_text="#A9B7C6")

                if not self.Sampled:
                    with open(__file__, mode="r", encoding="UTF-8") as file:
                        self.MyText.SetText(file.read())
                        self.Sampled = True
                # Debug non-custom values
                # self.MyText.Theme(halign="right", cursor_width=10, cursor_color=[1,0,0,1])
            else:
                self.MyText.Theme(#font_name="symbol", font_size=12,
                                  color_line="#606366", bg_line="#313335",
                                  color_text="#A9B7C6", bg_text="#2B2B2B")


    Main().run()
