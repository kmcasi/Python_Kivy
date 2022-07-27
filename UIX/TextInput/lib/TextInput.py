# // IMPORT
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.properties import ColorProperty

from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

try:
    from lib.helper.Font import FontMeasure
    from lib.helper.List import List
    from lib.helper.Thread import ThreadLinesAdd, ThreadLinesSubstract
except ModuleNotFoundError as e:
    import sys

    file = str(e.name).rsplit(".", 1)[1] if "." in e.name else e.name
    link:str = f"https://github.com/kmcasi/Python_Kivy/tree/main/UIX/TextInput/lib/helper"
    if e.name.startswith("lib.helper"):
        message = "If you downloaded the helper files form github then, " \
                  f"modify the path '{e.name}' to match your project structure.\n" \
                  f"Otherwise you can find them on: {link}"
    else: message = f"If you downloaded the {file}.py helper from github then, " \
                    f"modify the path '{e.name}' to match your project structure.\n" \
                    f"Otherwise you can find it on: {link}/{file}.py"
    raise ModuleNotFoundError(message).with_traceback(sys.exc_info()[2])

"""
The line numbers are bind on key up to use less processes like:
    L_CTRL, R_CTRL, Enter, Numpad Enter, Backspace, Delete,
    CTRL+V, CTRL+X, CTRL+Z and CTRL+Y for now.

    In my kivy source code I changed redo from CTRL+R to CTRL+Y. In case you
    want to use R instead of Y (or what ever is your redo bind) then go an look
    for '_on_key_up' event and you will find the "CTRL + Y" elif statement and replace
    the key code. I wrote another comment and there as a reminder.
    Use your IDE/Editor and search for "CTRL + Y", will be much easier to find it.
    (Usually Ctrl+F is a common short cut for that.)

Line numbers width are changed dynamically if is need it so you can set 'width_line'
to zero to get just the required width.

.. TODO::
    [ ]  Fix the cursor position reset when the font_name and/or font_size are changed
        on run time.
    [x]  Adding multithreading to improve the speed of line numbers response. In this
        stage, if we are pasting a lot of text, the app will freez until the line 
        numbers are are updated. If you do not copy-paste huge text will be fine
        because the line numbers ar added and subtracted base on your keyboard key.
        Any way, will be much useful to add 4000+ in 1-2 sec maximum or faster.
        I did some test on my old laptop and because is an old one, if I can
        make it faster for him, than will be greate. Off course the hardware
        is important to on this tests.
        
        PASTED LINES |        TIME (seconds)
                     |    SINGLE     |  THREADING
                600+ |     3 - 4     |    1 - 2
               1000+ |   8.8 - 9.7   |  2.3 - 3.5
               2000+ |    38 - 39    |  5.5 - 7.4
               3000+ |  88.5 - 90.1  |    9 - 11
               4000+ | 160.2 - 162.2 | 11.3 - 15.3
        
        Laptop: Windows 10 PRO N, 21H2, 64-bit
                HD Graphics 620
                i3-7100U CPU, 2.4 GHz, 2 Cores, 4 Threads, L3 cache: 3MB
                8 GB RAM DDR3 (1.2-2 GB usable)
"""


# // LOGIC
class TextInputCustom(ModalView):
    def __init__(self, width_line:int = 24, font_name:str = "comic", font_size:int = 18
                 , color_line:ColorProperty = "#606366", color_text:ColorProperty = "#A9B7C6"
                 , color_cursor:ColorProperty = "#606366", color_selection:ColorProperty = "#0066994D"
                 , bg_line:ColorProperty = "#313335", bg_text:ColorProperty = "#2B2B2B"
                 , padding_line:List = List(3, _len=2), padding_text:List = List(6, _len=2)
                 , direction="left"
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
        self.direction = "rtl" if direction.lower() == "right" else "ltr"

        # Private variables
        self.__lines: int = 1
        self.__lines_width_min: int = 0
        self.__cursor_index:int = 0
        self.__ctrl: bool = False
        self.__shift:bool = False
        self.__focused: bool = False
        self.__scroll_reset:bool = False
        self.__scroll_sync:bool = False
        self.__unredo: dict[str, bool] = {"undo": False, "redo": False}
        self.__filename: list = []
        self.__font_changed:dict = {"flag": False, "cursor": (0, 0), "scroll": [0, 0]}

        super(TextInputCustom, self).__init__(**kwargs)

        # UIX elements
        self._Layout = BoxLayout(orientation="horizontal")
        self._Lines = TextInput(text="1", width=self.width_line, is_focusable=False, do_wrap=False, halign="right",
                                background_color=self.bg_line, foreground_color=self.color_line,
                                font_name=self.font_name, font_size=self.font_size, padding=self.padding_line)
        self._Text = TextInput(auto_indent=True, do_wrap=False, base_direction=self.direction,
                               selection_color=self.color_selection, cursor_color=self.color_cursor, cursor_width=2.5,
                               background_color=self.bg_text, foreground_color=self.color_text,
                               font_name=self.font_name, font_size=self.font_size, padding=self.padding_text)

        # Determinate the line numbers width dynamically
        # if provided one is zero or less.
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
        Window.bind(on_key_down=self._on_key_down, on_key_up=self._on_key_up,
                    on_mouse_up=self._on_mouse_up,
                    on_resize=self._on_resize,
                    on_drop_file=self._on_drop_file, on_drop_end=self._on_drop_end)

    def binding(self, **kwargs) -> None:
        """Useful for controlling text binding.

        The key arguments are the same as **TextInput** ones because by calling this,
        in fact you are calling **TextInput.bind** from inside this class.

        :return: Nothing."""
        self._Text.bind(**kwargs)

    def _check_is_focus(self, instance:object, value:bool) -> None:
        """Checking if the text area is focused/clicked.

        :param instance:    Who trigger this event.
        :param value:       If has focused.
        :return:            Nothing."""
        self.__focused = value

    def _on_resize(self, window:object, width:int, height:int) -> None:
        """When window is resizing.

        :param window:  Who trigger this event.
        :param width:   The new window width.
        :param height:  The new window height.
        :return:        Nothing."""
        Clock.schedule_once(self._LineNumber_UpdateScroll, .5)

    def _on_drop_file(self, window:object, filename:str, x:int, y:int) -> None:
        """When a file was dropped.

        :param window:      Who trigger this event.
        :param filename:    The file
        :param x:           The horizontal mouse position.
        :param y:           The vertical mouse position.
        :return:            Nothing."""
        # Checking only if the text input is focused/clicked
        if self.__focused: self.__filename.append(filename)

    def _on_drop_end(self, window:object, x:int, y:int) -> None:
        """After drop event is done.

        :param window:  Who trigger this event.
        :param x:       The horizontal mouse position.
        :param y:       The vertical mouse position.
        :return:        Nothing."""
        # Checking only if the text input is focused/clicked
        if self.__focused: self._DropFile_Open()

    def _on_mouse_up(self, window:object, x:int, y:int, button:str, modifiers:list[str]) -> None:
        """Checking if some mouse key was released and base on that
        do some stuffs.

        :param window:      Who trigger this event.
        :param x:           The horizontal mouse position.
        :param y:           The vertical mouse position.
        :param button:      Triggered button.
        :param modifiers:   Triggered special keys.
        :return:            Nothing."""
        # Checking only if the text input is focused/clicked
        if self.__focused:
            # SHIFT + Left Click
            if self.__shift and button == "left":
                cursorIndex:tuple[int, int] = (self.__cursor_index, self._Text.cursor_index())
                self._Text.select_text(min(cursorIndex), max(cursorIndex))

    def _on_key_down(self, window:object, keycode:int, _:int, text:str, modifiers:list[str]) -> None:
        """Checking if some keyboard key was pressed and base on that
        do some stuffs.

        :param window:      Who trigger this event.
        :param keycode:     Triggered key code.
        :param text:        ASCII version of the keycode.
        :param modifiers:   Triggered special keys.
        :param _:           I do not know...
        :return:            Nothing."""
        # Checking only if the text input is focused/clicked
        if self.__focused:
            # Long press will trigger same logic multiple times
            # So we check if the flags was triggered already
            # before doing same flag trigger multiple times
            if not self.__ctrl and "ctrl" in modifiers: self.__ctrl = True
            if not self.__shift and "shift" in modifiers:
                self.__shift = True
                self.__cursor_index = self._Text.cursor_index()

            # [Arrow Up, Arrow Down, Page Up, Page Down]
            if keycode in [273, 274, 280, 281]: self._LineNumber_UpdateScroll()

            # [Enter, Numpad Enter]
            elif keycode in [13, 271]: self._LineNumber_Add(amount=1)

            # CTRL + V
            elif self.__ctrl and keycode == 118:
                self._LineNumber_Add(Clipboard.paste())

                if not self.__unredo["undo"]: self.__unredo["undo"] = True

    def _on_key_up(self, window:object, keycode:int, _:int) -> None:
        """Checking if some keyboard keys was released and base on that
        do some stuffs.

        :param window:  Who trigger this event.
        :param keycode: Triggered key code.
        :param _:       I do not know...
        :return:        Nothing."""
        # Checking only if the text input is focused/clicked
        if self.__focused:
            # # [Arrow Up, Arrow Down, Page Up, Page Down]
            if keycode in [273, 274, 280, 281]:
                self.__scroll_sync = True
                if self.__ctrl: self.__scroll_reset = True

            # Just in case the enter key was hold it, the line number scroll will be one
            # line behind. So we flag that scroll need to be sync.
            # [Enter, Numpad Enter]
            elif keycode in [13, 271]: self.__scroll_sync = True

            # [Backspace, Delete]
            if keycode in [8, 127]:
                try:
                    # After a substring was deleted, we check the undo dummy to see
                    # if was some lines, and we subtract that amount of lines.
                    # Last undo item suppose to be of type backspace or delete, so
                    # we use the right pattern without checking it.
                    item: dict = self._Text._undo[-1]
                    substring: str = item["undo_command"][2]
                    self._LineNumber_Unknown(substring)

                # If we got an int instead of str or an empty list, do nothing
                except TypeError: pass
                except IndexError: pass

            # CTRL + V
            # elif self.__ctrl and keycode == 118:
            #     import pyperclip
            #     self._LineNumber_Add(pyperclip.paste())
            #     # self._LineNumber_Add(Clipboard.paste())
            #
            #     if not self.__unredo["undo"]: self.__unredo["undo"] = True
            #     self.__scroll_sync = True

            # CTRL + X
            elif self.__ctrl and keycode == 120:
                self._LineNumber_Subtract(Clipboard.paste())

                if not self.__unredo["undo"]: self.__unredo["undo"] = True
                self.__scroll_sync = True

            # CTRL + Z
            elif self.__ctrl and keycode == 122:
                # Copy & Paste are the same, just adding and subtracting are inverted
                try:
                    # If undo dummy is not empty, we make sore the "undo" flag is True
                    if len(self._Text._undo) > 0:
                        self.__unredo["undo"] = True

                    # Otherwise, if the undo dummy is empty, and we already got the last itme
                    # pass this check by raising and IndexError
                    elif not self.__unredo["undo"]:
                        raise IndexError

                    # if not self.__unredo["redo"]: self.__unredo["redo"] = True

                    # Get the last undo item from redo and the type of it
                    item: dict = self._Text._redo[-1]
                    _type: str = item["undo_command"][0]

                    # If type comes from backspace or delete, add the line numbers from substring
                    if _type in ["bkspc", "delsel"]:
                        self._LineNumber_Add(item["undo_command"][2])
                    # Otherwise, if the type is insert, subtract the line numbers from substring
                    elif _type == "insert":
                        self._LineNumber_Subtract(item["redo_command"][1])

                    # Because undo dummy was empty before we started this check we
                    # set "undo" flag as False to know that was the last item of the list
                    if len(self._Text._undo) == 0: self.__unredo["undo"] = False

                # If we got an int instead of str or an empty list, do nothing
                except TypeError: pass
                except IndexError: pass
                finally: self.__scroll_sync = True

            # I changed the kivy source code from R to Y, but if you still want
            # to use original CTRL + R, then change keycode from 121 to 114.
            # CTRL + Y
            elif self.__ctrl and keycode == 121:
                # Copy & Paste are the same, just adding and subtracting are inverted
                try:
                    # If redo dummy is not empty, we make sore the "redo" flag is True
                    if len(self._Text._redo) > 0:
                        self.__unredo["redo"] = True

                    # Otherwise, if the redo dummy is empty, and we already got the last itme
                    # pass this check by raising and IndexError
                    elif not self.__unredo["redo"]:
                        raise IndexError

                    # Get the last redo item from undo and the type of it
                    item: dict = self._Text._undo[-1]
                    _type: str = item["undo_command"][0]

                    # If type comes from backspace or delete, subtract the line numbers from substring
                    if _type in ["bkspc", "delsel"]:
                        self._LineNumber_Subtract(item["undo_command"][2])
                    # Otherwise, if the type is insert, add the line numbers from substring
                    elif _type == "insert":
                        self._LineNumber_Add(item["redo_command"][1])

                    # Because redo dummy was empty before we started this check we
                    # set "redo" flag as False to know that was the last item of the list
                    if len(self._Text._redo) == 0: self.__unredo["redo"] = False

                # If we got an int instead of str or an empty list, do nothing
                except TypeError: pass
                except IndexError: pass
                finally: self.__scroll_sync = True

            # [L_CTRL, R_CTRL]
            elif keycode in [305, 306]: self.__ctrl = False

            # [L_SHIFT, R_SHIFT]
            elif keycode in [304, 303]: self.__shift = False

            # Update line numbers scroll if is necessary
            if self.__scroll_sync or not self.__ctrl:
                # If the text view was scrolled we will leave behind the text cursor, then reset
                # the line number scroll on key press because the text scroll will change to.
                if self.__scroll_reset:
                    self.__scroll_reset = False
                    self._LineNumber_UpdateScroll()
                elif self.__scroll_sync:
                    self.__scroll_sync = False
                    self._LineNumber_UpdateScroll()

    def _LineNumber_Unknown(self, substring:str|None=None) -> None:
        """This is a helper to recalculate the line numbers.

        :param substring:   The text to process as string.
        :return:            Nothing."""
        reference: int = len(self._Text.lines)

        # If the reference is bigger than the (line number different from zero)
        if reference > self.__lines > 1:
            # Add just the difference
            self._LineNumber_Add(substring, amount=reference - self.__lines)

        # If the reference is less than the line number
        elif reference < self.__lines:
            # Subtract just the difference
            self._LineNumber_Subtract(substring, amount=self.__lines - reference)

        # Otherwise, write line numbers from scratch base on the reference.
        # Most of the time this will be call it when the line numbers and/or
        # the reference are less than 1 and will add that "1" line number.
        elif self.__lines != reference or self.__lines < 1:
            self._Lines.text = "1"

            for line in range(2, reference + 1):
                self._Lines.text += f"\n{line}"

            self.__lines = reference

            self._LineNumber_AutoWidth()

    def _LineNumber_Add(self, substring:str|None=None, amount:int=0) -> None:
        """Add the line numbers.

        :param substring:   The text to process as string.
        :param amount:      The amount of addition.
        :return:            Nothing."""
        # Use multithreading to figure out the optimal way to handle
        # the lines amount and the text version of it
        try:
            t = ThreadLinesAdd(self.__lines, substring, amount)
            self._Lines.text += t.text
            self.__lines += t.lines
        except ValueError: pass

        # Update the line number width to mach the correct new size
        self._LineNumber_AutoWidth()

    def _LineNumber_Subtract(self, substring=None, amount:int=0) -> None:
        """Subtract the line numbers.

        :param substring:   The text to process as string.
        :param amount:      The amount of subtraction.
        :return: Nothing."""
        try:
            t = ThreadLinesSubstract(self._Lines.text, substring, amount)
            self._Lines.text = t.text
            self.__lines -= t.lines
            print(self.__lines)
        except ValueError: pass

        # Update the line number width to mach the correct new size
        self._LineNumber_AutoWidth()

    def _LineNumber_UpdateScroll(self, *noUse, sampleX:int|None=None, sampleY:int|None=None) -> None:
        """**_LineNumber_UpdateScroll** purpose is to sync line numbers scroll_y
        value with the text one and to update the graphics for the line numbers.

        :param noUse:   Is unused, but is necessary for the tick events, like when
                        more values are provided then I need.
        :param sampleX: The text scroll x value.
        :param sampleY: The text scroll y value.
        :return: Nothing.
        """
        if sampleX is not None: self._Text.scroll_x = sampleX
        if sampleY is not None: self._Text.scroll_y = sampleY
        self._Lines.scroll_y = self._Text.scroll_y
        self._Lines._trigger_update_graphics()

    def on_touch_up(self, touch:object) -> None:
        """**Scrolling event**

        Let you scroll the text but not the line numbers. They are synced with the text.

        :param touch:   What type of event it is.
        :return:        Nothing."""
        self._Text.on_touch_up(touch)
        self._LineNumber_UpdateScroll()

    def on_touch_down(self, touch:object) -> None:
        """**Scrolling event**

        Let you scroll the text but not the line numbers. They are synced with the text.

        :param touch:   What type of event it is.
        :return:        Nothing."""
        self._Text.on_touch_down(touch)
        self._LineNumber_UpdateScroll()

    def on_touch_move(self, touch:object) -> None:
        """**Scrolling event**

        Let you scroll the text but not the line numbers. They are synced with the text.

        :param touch:   What type of event it is.
        :return:        Nothing."""
        self._Text.on_touch_move(touch)
        self._LineNumber_UpdateScroll()

    def _DropFile_Open(self) -> None:
        """The purpose of this is to extract the dropped  file(s) content and to slip it
        on the current cursor position.

        .. NOTE ::
            This is a proof of concept. Need some rework for more elegant way to approach this.

        :return: Nothing."""
        files_count: int = len(self.__filename)

        if files_count == 1:
            try:
                with open(self.__filename.pop(), mode="rb", buffering=4096) as file:
                    self._Text.insert_text(file.read())
                self._LineNumber_Unknown()
            finally:
                file.close()

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

    def _LineNumber_AutoWidth(self) -> None:
        """Set the maximum line number with need it to show up.

        If required more space will extrude, otherwise will use the provided width line.

        :return: Nothing."""
        pad = (self.padding_line[0], self.padding_line[2 if len(self.padding_line) > 3 else 1])

        required = pad[0] + self.__lines_width_min * len(str(self.__lines)) + pad[1]
        self._Lines.width = max(self.width_line, required)

    def _find_font_size(self, sample:str="7") -> None:
        """Calculate the minimum width need it to display one character.

        :param sample:  The sample as a string.
        :return:        Nothing."""
        font = FontMeasure(self.font_name, self.font_size)
        self.__lines_width_min = font.get_width_of(sample)

    def Theme(self, **kwargs) -> None:
        """**Theme** let you change the style dynamically with some custom
        key arguments like:

        [type: int]
            width_line, font_size
        [type: str]
            font_name, direction
        [type: ColorProperty]
            color_line, color_text, color_cursor, color_selection, bg_line, bg_text
        [type: List]
            padding_line, padding_text

        .. Note::
            Other key arguments can be provided, but they will be applied for both
            (line numbers and text) if is possible.

        :return: Nothing.
        """
        update: bool = False

        if "direction" in kwargs:
            self.direction = "rtl" if kwargs["direction"].lower() == "right" else "ltr"
            self._Text.base_direction = self.direction
            kwargs.pop("direction")
            update = True

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
            self.__font_changed["flag"] = True
            kwargs.pop("font_name")
            update = True

        if "font_size" in kwargs:
            self.font_size = kwargs["font_size"]
            self._Lines.font_size = self.font_size
            self._Text.font_size = self.font_size
            self._find_font_size()
            self.__font_changed["flag"] = True
            kwargs.pop("font_size")
            update = True

        if "padding_line" in kwargs:
            self.padding_line = kwargs["padding_line"]
            self._Lines.padding = self.padding_line
            kwargs.pop("padding_line")
            update = True

        if "padding_text" in kwargs:
            self.padding_text = kwargs["padding_text"]
            self._Text.padding = self.padding_text
            kwargs.pop("padding_text")
            update = True

        # If is something not custom like above then try to apply them
        # for both of then (line numbers and text itself)
        if len(kwargs.keys()) > 0:
            for key, value in kwargs.items():
                decorator: str = "\"" if type(value) == str else ""
                for uix in ["_Lines", "_Text"]:
                    try:
                        exec(f"self.{uix}.{key} = {decorator}{value}{decorator}")
                        update = True
                    except Exception: pass

        # If the text was unfocused and the font was changed
        # then save the cursor and the scroll values
        if not self.__focused and self.__font_changed["flag"]:
            self.__font_changed["cursor"] = self._Text.cursor
            self.__font_changed["scroll"] = [self._Text.scroll_x, self._Text.scroll_y]

        # Updating graphics just if is need it
        if update:
            self._Lines._trigger_update_graphics()
            self._Text._trigger_update_graphics()

            # If the font was changed schedule an event to fix
            # the cursor and the scroll changes
            if self.__font_changed["flag"]:
                Clock.schedule_once(self._fix_font_changes_jumps)
                self.__font_changed["flag"] = False

    def _fix_font_changes_jumps(self, *noUse) -> None:
        """How the name is saying, the purpose of this is to fix the cursor and scroll changes
        when the font is changeing on run time.

        :param noUse:   Is unused, but is necessary for the tick events, like when
                        more values are provided then I need.
        :return:        Nothing."""
        self._Text.cursor = self.__font_changed["cursor"]
        self._LineNumber_UpdateScroll(sampleX=self.__font_changed["scroll"][0],
                                      sampleY=self.__font_changed["scroll"][1])
        self._Text.cancel_selection()

    @staticmethod
    def _MakeText(*values:object, sep:str|None=" ", end:str|None="\n") -> str:
        """Making text from provided values.

        :param values:  Arguments to be added as text.
        :param sep:     String inserted between values.
        :param end:     String appended after the last value.
        :return:        String."""
        text:str = ""
        for value in values: text += f"{sep}{value}" if sep is not None else value
        if end is not None: text += end
        return text[len(sep):] if sep is not None else text

    def SetText(self, *values:object, sep:str|None=" ", end:str|None="\n") -> None:
        """**SetText** let you setting a new text by replacing the existing one.

        :param values:  Arguments to be added as text.
        :param sep:     String inserted between values.
        :param end:     String appended after the last value.
        :return:        Nothing.

        >>> self.list = ["The fox", "got a chicken"]
        >>> self.MyText = TextInputCustom()
        >>>
        >>> self.MyText.SetText("Your text is here.")
        >>> self.MyText.SetText(*self.list, sep="-", end=".")
        """
        self._Text.text = self._MakeText(*values, sep=sep, end=end)
        self._LineNumber_Unknown()

    def AddText(self, *values:object, sep:str|None=" ", end:str|None="\n") -> None:
        """**AddText** let you adding text after the existing one.

        :param values:  Arguments to be appended after the text.
        :param sep:     String inserted between values.
        :param end:     String appended after the last value.
        :return:        Nothing.

        >>> self.list = ["The lazy cat", "got nothing"]
        >>> self.MyText = TextInputCustom()
        >>>
        >>> self.MyText.AddText("Other text is here.")
        >>> self.MyText.AddText(*self.list, sep="-", end=".")
        """
        text:str = self._MakeText(*values, sep=sep, end=end)
        self._Text.text += text
        self._LineNumber_Add(text)

    def GetText(self) -> str:
        """**GetText** provide you the text.

        :return:    The text variable of type string (from kivy AliasProperty)."""
        return self._Text.text

    def Clear(self) -> None:
        """**Clear** the entire text and also the line numbers, off course.

        :return: Nothing."""
        self._Text.text, self.__lines, self._Lines.text = "", 1, "1"
        self._LineNumber_AutoWidth()

