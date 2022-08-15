# // IMPORT
import random
from builtins import staticmethod, property
from logging import warning as WARNING
from sys import _getframe as THIS
from os import linesep as OS_LN_SEP

from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import ColorProperty
from kivy.utils import deprecated

from kivy.core.clipboard import Clipboard
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

try:
    from lib.helper.Font import FontMeasure
    from lib.helper.List import List
    from lib.helper.Thread import ThreadLinesAdd, ThreadLinesSubstract
    from lib.helper.utils import Make, Check, clamp, normalize
except ModuleNotFoundError as e:
    from sys import exc_info

    link:str = f"https://github.com/kmcasi/Python_Kivy/tree/main/UIX/TextInput/lib/helper"
    message:str = "If you downloaded the helper files form github then, " \
                  f"modify the path '{e.name}' to match your project structure.\n" \
                  f"Otherwise you can find them on: {link}"
    raise ModuleNotFoundError(message).with_traceback(exc_info()[2])

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
"""

#// Global Variable's
Font_Default:str = Config.getdefault("kivy", "default_font", None).split("'", 2)[1]


# // LOGIC
class TextInput_LN(BoxLayout):
    def __init__(self, width_ln:int = 24, width_tab:int = 4, RTL:bool = False, auto_indent:bool = True
                 , font_name:str = Font_Default, font_size:int = 18
                 , width_scroll:int|float = 11, width_cursor:int|float = 2
                 , margin_scroll:int|float = 0, margin_scroll_cursor:list|tuple = List(31.5, _type=float)
                 , padding_ln:list|tuple = List(3), padding_txt:list|tuple = List(6), spacing:int = 0
                 , align_ln:str = "right", align_txt:str = "left"
                 , color_ln:ColorProperty = "606366", color_txt:ColorProperty = "A9B7C6"
                 , color_cursor:ColorProperty = "806F9F", color_selection:ColorProperty = "0066994D"
                 , color_scroll:ColorProperty = "A6A6A680", color_scroll_inactive:ColorProperty = "A6A6A647"
                 , bg_ln:ColorProperty = "313335", bg_txt:ColorProperty = "2B2B2B"
                 , color_info:ColorProperty = "606366", bg_info:ColorProperty = "343638"
                 , **kwargs):
        """Custom TextInput class with line numbers.

        .. NOTE::
            If you are useeing **bind** you will control the parent class witch
            is **BoxLayout**. If you want to control the TextInput bind use **binding**.
            Like and example see below.

            >>> self.myText = TextInput_LN()
            >>> self.myText.binding(text=self.your_text_bind)
        """
        super(TextInput_LN, self).__init__(**kwargs)

        # Local variables
        self.width_ln:int = width_ln
        self.width_tab:int = width_tab
        self.width_scroll:int|float = width_scroll
        self.width_cursor:int|float = width_cursor
        self.font_name:str = font_name
        self.font_size:int = font_size
        self.RTL:bool = RTL
        self.auto_indent:bool = auto_indent
        self.margin_scroll:int|float = margin_scroll
        self.margin_scroll_cursor:list|tuple = margin_scroll_cursor
        self.padding_ln:list = padding_ln
        self.padding_txt:list = padding_txt
        self.spacing:int = spacing
        self.align_ln:str = align_ln
        self.align_txt:str = align_txt
        self.color_ln:ColorProperty = color_ln
        self.color_txt:ColorProperty = color_txt
        self.color_cursor:ColorProperty = color_cursor
        self.color_selection:ColorProperty = color_selection
        self.color_scroll:ColorProperty = color_scroll
        self.color_scroll_inactive:ColorProperty = color_scroll_inactive
        self.color_info:ColorProperty = color_info
        self.bg_ln:ColorProperty = bg_ln
        self.bg_txt:ColorProperty = bg_txt
        self.bg_info:ColorProperty = bg_info

        # Private variables
        self.__lines:int = 1
        self.__width_ln_min:int = 0
        self.__width_txt_min:int = 0
        self.__focused:bool = False
        self.__ctrl:bool = False
        self.__shift:bool = False
        self.__unredo:dict[str, bool] = {"undo": False, "redo": False}
        self.__cursor_index:dict[str, int] = {"old":-1, "new":0}
        self.__scroll_horizontal:dict[str, str|bool] = {"flag":False, "button":"scrollright"}
        self.__info_font_name:str = Font_Default
        self.__info_font_size:int = 14
        self.__info_padding:tuple[int, int] = (6, 3)
        self.__info_count_only_visible_chars:bool = True
        self.__os_sep:dict[str, str] = {"\r\n":"CRLF", "\r":"CR", "\n":"LF"}
        self.__file_ln_break:str = self.__os_sep[OS_LN_SEP]
        self.__file_encoding:str = "UTF-8"
        self.__hidden_height:float = 0.0
        self.__hidden_width:float = 0.0
        self.__normalized_line_height:float = 0.0
        self.__normalized_line_height_view:float = 0.0

        # Do some stuffs before to initialize the UIX elements
        self._sync_padding()
        self._find_width_ln_min()
        self.width_ln = max(width_ln, self.__width_ln_min) + self.padding_ln[0] + self.padding_ln[2]

        # UIX elements
        self.__Layout = BoxLayout(orientation="vertical")
        self.__Layout_Content = BoxLayout(orientation="horizontal")

        self.__Scroll_LineNumber = ScrollView(always_overscroll=False, scroll_type=["bars", "content"]
                                              , width=self.width_ln, do_scroll_x=False
                                              , bar_width=0, bar_margin=0
                                              , bar_color="00000000", bar_inactive_color="00000000")

        self.__Scroll_Text = ScrollView(always_overscroll=False, scroll_type=["bars"]
                                        , bar_width=self.width_scroll, bar_margin=self.margin_scroll
                                        , bar_color=self.color_scroll, bar_inactive_color=self.color_scroll_inactive)

        self._LineNumber = TextInput(text="1", disabled=True, do_wrap=False, halign=self.align_ln
                                     , font_name=self.font_name, font_size=self.font_size
                                     , width=self.width_ln, padding=self.padding_ln, line_spacing=self.spacing
                                     , disabled_foreground_color=self.color_ln, background_color=self.bg_ln)

        self._Text = TextInput(auto_indent=self.auto_indent, do_wrap=False, tab_width=self.width_tab
                               , halign=self.align_txt, base_direction="rtl" if self.RTL else "ltr"
                               , font_name=self.font_name, font_size=self.font_size
                               , padding=self.padding_txt, cursor_width=self.width_cursor
                               , line_spacing=self.spacing
                               , foreground_color=self.color_txt, background_color=self.bg_txt
                               , cursor_color=self.color_cursor, selection_color=self.color_selection)

        self.__Info = TextInput(text=f"\t\t\t\tText"
                                , disabled=True, do_wrap=False, halign="right", tab_width=6
                                , padding=self.__info_padding
                                , disabled_foreground_color=self.color_info, background_color=self.bg_info
                                , font_name=self.__info_font_name, font_size=self.__info_font_size)

        # Settings
        self.__construct_info(ln_sep=True, encoding=True, tabs=True)
        self.__background()
        self.__size_hint()
        self.__add_widget()
        self.__bind()

    def __background(self) -> None:
        """Clear the provided background texture, by kivy atlas.

        :return: Nothing."""
        self._Text.background_normal = ""
        self._Text.background_active = ""
        self._LineNumber.background_disabled_normal = ""
        self.__Info.background_disabled_normal = ""
        self.background = ""

        # Set the self class background color
        self.background_color = self.bg_txt

    def __size_hint(self) -> None:
        """Set the uix size.

        :return: Nothing."""
        # Provide info height base on used font name, size, and vertical padding
        measure = FontMeasure(self.__info_font_name, self.__info_font_size)
        self.__Info.height = self.__info_padding[1] * 2 + measure.get_height_of(self.__Info.text)

        # UIX elements hint size
        self._LineNumber.size_hint = (None, None)
        self._Text.size_hint = (None, None)
        self.__Info.size_hint = (1, None)

        # ScrollView's hint size
        self.__Scroll_LineNumber.size_hint = (None, 1)
        self.__Scroll_Text.size_hint = (1, 1)

    def __add_widget(self) -> None:
        """Adding UIX elements.

        :return: Nothing."""
        # ScrollView's child's
        self.__Scroll_LineNumber.add_widget(self._LineNumber)
        self.__Scroll_Text.add_widget(self._Text)

        # Layout child's
        self.__Layout_Content.add_widget(self.__Scroll_LineNumber)
        self.__Layout_Content.add_widget(self.__Scroll_Text)
        self.__Layout.add_widget(self.__Layout_Content)
        self.__Layout.add_widget(self.__Info)

        # Parent layout
        self.add_widget(self.__Layout)

    def __bind(self) -> None:
        """Binding events.

        :return: Nothing."""
        self._Text.bind(focus=self._check_is_focus, cursor=self._on_cursor)

        self.__Scroll_Text.bind(scroll_y=self._on_scroll_y, size=self._on_scroll_resize
                                , on_scroll_move=self._on_scroll_move, on_scroll_stop=self._on_scroll_stop
                                , on_scroll_start=self._on_scroll_start)

        self.__Scroll_LineNumber.bind(scroll_y=self._on_scroll_y
                                      , on_scroll_move=self._on_scroll_move, on_scroll_stop=self._on_scroll_stop)

        Window.bind(on_key_down=self._on_key_down, on_key_up=self._on_key_up
                    , on_mouse_down=self._on_mouse_down, on_mouse_up=self._on_mouse_up
                    , on_resize=self._on_resize)

    def _on_resize(self, instance:Window, width:int, height:int) -> None:
        """When window is resizing, the text and line numbers need resizing to mach the ScrollView size.

        :param instance:    Who trigger this event.
        :param width:       The new window width.
        :param height:      The new window height.
        :return:            Nothing."""
        # We will do this next frame
        # If not, the scroll bar will show even the text is less than ScrollView size
        Clock.schedule_once(lambda _:self._update_text_size())

    def _on_scroll_resize(self, instance:ScrollView, size:list[float]) -> None:
        """The purpose of it is to recalculate some stuffs on internal viewport changes.

        :param instance:    Who trigger this event.
        :param size:        List of width and height values.
        :return:            Nothing."""
        self.__update_hidden_size()

    def __update_hidden_size(self) -> None:
        """Theo the name is saying, the purpose of it is to recalculate the hidden size of the text.

        :return: Nothing."""
        self.__hidden_height = self._Text.height - self.__Scroll_Text.height
        self.__hidden_width = self._Text.width - self.__Scroll_Text.width

    def _on_scroll_start(self, instance:ScrollView, event:object) -> None:
        """The purpose of it is to modify the event on mouse wheel.

        :param instance:    Who trigger this event.
        :param event:       The triggered event.
        :return:            Nothing."""
        # If the horizontal scroll was flagged, change the event button with the fake one
        if self.__scroll_horizontal["flag"]: event.button = self.__scroll_horizontal["button"]

    @staticmethod
    def _on_scroll_stop(instance:ScrollView, event:object) -> None:
        """The purpose of it is to release the cursor restrictions when the user is done scrolling.

        :param instance:    Who trigger this event.
        :param event:       The triggered event.
        :return:            Nothing."""
        Window.ungrab_mouse()

    @staticmethod
    def _on_scroll_move(instance:ScrollView, event:object) -> None:
        """The purpose of it is to keep the cursor inside the main window while is a manual scroll.
        Mouse scroll wheel do not trigger this event.

        When the user press the left click and is dragging the scroll bar (or the line number),
        in case the cursor is leaving the window, the scroll event will stop until the cursor is
        back over the main window.

        :param instance:    Who trigger this event.
        :param event:       The triggered event.
        :return:            Nothing."""
        Window.grab_mouse()

    def _on_scroll_y(self, instance:ScrollView, value:float) -> None:
        """The purpose of this logic is to sync the vertical scroll values.

        :param instance:    Who trigger this event.
        :param value:       Scroll value.
        :return:            Nothing."""
        # The only way to know who trigger this event is by checking
        # if the ScrollView is allowed to scroll horizontally
        from_ln:bool = not instance.do_scroll_x

        # Base on who call this event, update the value on the other one
        if from_ln: self.__Scroll_Text.scroll_y = value
        else: self.__Scroll_LineNumber.scroll_y = value

    def _check_is_focus(self, instance:TextInput, value:bool) -> None:
        """Checking if the text area is focused/clicked.

        :param instance:    Who trigger this event.
        :param value:       If has focused.
        :return:            Nothing."""
        self.__focused = value

        # Hide cursor position if text lose focus
        if not value: self.__construct_info(cursor=None)

    def _on_mouse_down(self, instance:Window, x:float, y:float, button:str, modifiers:list[str]) -> None:
        """Checking if some mouse key was pressed and base on that do some stuffs.

        :param instance:    Who trigger this event.
        :param x:           The horizontal mouse position.
        :param y:           The vertical mouse position.
        :param button:      Triggered button.
        :param modifiers:   Triggered special keys.
        :return:            Nothing."""
        # Checking only if the text input is focused/clicked
        if self.__focused:
            # Flag the horizontal scroll on scroll up and the corresponding fake button of it
            if self.__shift and button == "scrollup":
                self.__scroll_horizontal["flag"] = True
                self.__scroll_horizontal["button"] = "scrollright"

            # Flag the horizontal scroll on scroll down and the corresponding fake button of it
            elif self.__shift and button == "scrolldown":
                self.__scroll_horizontal["flag"] = True
                self.__scroll_horizontal["button"] = "scrollleft"

            # Un flags the horizontal scroll on next mouse button event if the above
            # conditions are not meet
            elif self.__scroll_horizontal["flag"]: self.__scroll_horizontal["flag"] = False

    def _on_mouse_up(self, instance:Window, x:float, y:float, button:str, modifiers:list[str]):
        """Checking if some mouse key was released and base on that do some stuffs.

        :param instance:    Who trigger this event.
        :param x:           The horizontal mouse position.
        :param y:           The vertical mouse position.
        :param button:      Triggered button.
        :param modifiers:   Triggered special keys.
        :return:            Nothing."""
        # Checking only if the text input is focused/clicked
        if self.__focused:
            # SHIFT + Left Click
            if self.__shift and button == "left":
                cursorIndex:tuple[[int, int], int] = (*self.__cursor_index.values(), self._Text.cursor_index())
                self._Text.select_text(min(cursorIndex), max(cursorIndex))

    def _on_cursor(self, instance:TextInput, position:tuple[int, int]) -> None:
        """The purpose of this function is to handle staffs witch are base on the cursor.

        :return: Nothing."""
        Clock.schedule_once(lambda _: self.__construct_info(cursor=True), .02)
        Clock.schedule_once(lambda _: self.__update_scroll())

    def __update_scroll(self) -> None:
        """This function handle the auto scrolling logics base on the cursor position.

        :return: Nothing."""
        offset_x:float = self.__hidden_width * self.__Scroll_Text.scroll_x
        offset_y:float = self.__hidden_height * self.__Scroll_Text.scroll_y

        normal_x:float = normalize(self._Text.cursor_pos[0]
                                   , offset_x + self.margin_scroll_cursor[0]
                                   , offset_x + self.__Scroll_Text.width - self.margin_scroll_cursor[2])
        normal_y:float = normalize(self._Text.cursor_pos[1]
                                   , offset_y + self.margin_scroll_cursor[3]
                                   , offset_y + self.__Scroll_Text.height - self.margin_scroll_cursor[1])

        if normal_x < 0:
            amount:float = (offset_x - self._Text.cursor_pos[0] + self.margin_scroll_cursor[0])
            try: amount /= self.__hidden_width
            except ZeroDivisionError: pass
            self.__Scroll_Text.scroll_x = clamp(self.__Scroll_Text.scroll_x - amount)

        elif normal_x > 1:
            amount:float = (self._Text.cursor_pos[0] - offset_x - self.__Scroll_Text.width +
                            self.width_cursor + self.margin_scroll_cursor[2])
            try: amount /= self.__hidden_width
            except ZeroDivisionError: pass
            self.__Scroll_Text.scroll_x = clamp(self.__Scroll_Text.scroll_x + amount)

        if normal_y < self.__normalized_line_height_view:
            amount:float = (offset_y - self._Text.cursor_pos[1] + self._Text.line_height +
                            self.margin_scroll_cursor[3])
            try: amount /= self.__hidden_height
            except ZeroDivisionError: pass
            self.__Scroll_Text.scroll_y = clamp(self.__Scroll_Text.scroll_y - amount)

        elif normal_y > 1:
            amount:float = (self._Text.cursor_pos[1] - offset_y - self.__Scroll_Text.height +
                            self.margin_scroll_cursor[1])
            try: amount /= self.__hidden_height
            except ZeroDivisionError: pass
            self.__Scroll_Text.scroll_y = clamp(self.__Scroll_Text.scroll_y + amount)

    def __construct_info(self, cursor:bool|None=False, ln_sep:bool|str=False, encoding:bool|str=False,
                         tabs:bool=False, source:bool|str=False) -> None:
        """The purpose of it is to update the informations.

        :param cursor:      Cursor position.
        :param ln_sep:      Line separator used.
        :param encoding:    Encoding used.
        :param tabs:        Tabs width.
        :param source:      Source type.
        :return:            Nothing."""
        # Get existing info's
        info_exist:str = self.__Info.text.split("\t")

        # Cursor -> row:col (n char(s), n line break(s))
        if cursor is None: info_cursor:str = ""
        else: info_cursor:str = f"{self._Text.cursor_row + 1}:{self._Text.cursor_col + 1}" if cursor else info_exist[0]

        # If Update cursor and text is selected
        if cursor and self._Text.selection_text:
            count_chars:str = ""
            count_ln_breaks:str = ""

            # Count line break and subtract 1 if last selected character is not a line breaker
            lines:int = len(self._Text.selection_text.splitlines()) - \
                        int(self._Text.selection_text[-1:] not in ["\r", "\n"])

            # Count selected characters
            chars:int = self._Text.selection_to - self._Text.selection_from
            # Keep characters amount positive
            if chars < 0: chars *= -1
            # Subtract line brakes amount
            if self.__info_count_only_visible_chars: chars -= lines

            # Show chars/lines if they are not 0 (zero)
            if chars: count_chars = f"{chars} char{'s' if chars > 1 else ''}"
            if lines: count_ln_breaks = f"{', ' if chars else ''}{lines} line break{'s' if lines > 1 else ''}"
            info_cursor += f" ({count_chars}{count_ln_breaks})"

        # Line separator -> CR|LF|CRLF
        if type(ln_sep) is str: info_ln_sep:str = ln_sep
        else: info_ln_sep:str = self.__file_ln_break if ln_sep else info_exist[1]

        # Encoding -> UTF-8|US-ASCII|binary...
        if type(encoding) is str: info_encoding:str = encoding
        else: info_encoding:str = self.__file_encoding if encoding else info_exist[2]

        # Tab width -> n space(s)
        info_tabs:str = f"{self.width_tab} space{'s' if self.width_tab > 1 else ''}" if tabs else info_exist[3]

        # Source -> Text|Python|C++...
        if type(source) is str: info_source:str = source
        else: info_source:str = "Text" if source else info_exist[4]

        # Construct info
        self.__Info.text = f"{info_cursor}\t{info_ln_sep}\t{info_encoding}\t{info_tabs}\t{info_source}"

    def _update_text_width_from_text(self, text:str) -> None:
        """This logic is used to update the text width when the user press a button.

        To be more specific, when the user type some text, here we check the line width where user is typing
        with the text width and if the line becomes bigger then the actual text size we will extrude the text width.

        :param text:    Pressed button as text.
        :return:        Nothing."""
        # Get the desired line width base on edits
        line_width: int = int(self.padding_txt[0] + self.padding_txt[2]
                              + self._Text._lines_rects[self._Text.cursor_row].size[0]
                              + FontMeasure(self.font_name, self.font_size).get_width_of(text))

        # Update text width if desired line width is bigger than actual width
        if line_width > self._Text.width:
            self._Text.width = line_width
            # In case the cursor is on right edge of the text,
            # set horizontal scroll value to 1 to be able to see what is added
            if self._Text.cursor_pos[0] == (self._Text.width - self.padding_txt[2]): self.__Scroll_Text.scroll_x = 1.0

    def _on_key_down(self, instance:Window, keycode:int, _:int, text:str, modifiers:list[str]) -> None:
        """Checking if some keyboard key was pressed and base on that do some stuffs.

        :param instance:    Who trigger this event.
        :param keycode:     Triggered key code.
        :param text:        ASCII version of the keycode.
        :param modifiers:   Triggered special keys.
        :param _:           I do not know...
        :return:            Nothing."""
        # Checking only if the text input is focused/clicked
        if self.__focused:
            # Update text size if necessary
            if text is not None: self._update_text_width_from_text(text)

            # Long press will trigger same logic multiple times
            # So we check if the flags was triggered already
            # before doing same flag trigger multiple times
            self._Text.readonly = "alt" in modifiers
            if not self.__ctrl and "ctrl" in modifiers: self.__ctrl = True
            if not self.__shift and "shift" in modifiers:
                self.__shift = True
                self.__cursor_index["old"] = self._Text.selection_from
                self.__cursor_index["new"] = self._Text.cursor_index()

            # ALT + Numpad 8
            if "alt" in modifiers and keycode == 264:
                self.__Scroll_Text.scroll_y = clamp(self.__Scroll_Text.scroll_y + self.__normalized_line_height)

            # ALT + Numpad 2
            elif "alt" in modifiers and keycode == 258:
                self.__Scroll_Text.scroll_y = clamp(self.__Scroll_Text.scroll_y - self.__normalized_line_height)

            # ALT + Numpad 4
            elif "alt" in modifiers and keycode == 260:
                self.__Scroll_Text.scroll_x = clamp(self.__Scroll_Text.scroll_x - self.__normalized_line_height)

            # ALT + Numpad 6
            elif "alt" in modifiers and keycode == 262:
                self.__Scroll_Text.scroll_x = clamp(self.__Scroll_Text.scroll_x + self.__normalized_line_height)

            # [Enter, Numpad Enter]
            elif keycode in [13, 271]: self._LineNumber_Add(amount=1)

            # CTRL + V
            elif self.__ctrl and keycode == 118:
                self._LineNumber_Add(Clipboard.paste())

                if not self.__unredo["undo"]: self.__unredo["undo"] = True

    def _on_key_up(self, instance:Window, keycode: int, _: int) -> None:
        """Checking if some keyboard keys was released and base on that do some stuffs.

        :param instance:    Who trigger this event.
        :param keycode:     Triggered key code.
        :param _:           I do not know...
        :return:            Nothing."""
        # Checking only if the text input is focused/clicked
        if self.__focused:
            # [Backspace, Delete]
            if keycode in [8, 127]:
                try:
                    # After a substring was deleted, we check the undo dummy to see
                    # if was some lines, and we subtract that amount of lines.
                    # Last undo item suppose to be of type backspace or delete, so
                    # we use the right pattern without checking it.
                    # TODO: Move it on key down to avoid long press mist.
                    #       Maybe there will need to use :mod:`~kivy.clock.Clock`
                    item: dict = self._Text._undo[-1]
                    substring: str = item["undo_command"][2]
                    self._LineNumber_Unknown(substring)

                # If we got an int instead of str or an empty list, do nothing
                except TypeError: pass
                except IndexError: pass

            # CTRL + X
            elif self.__ctrl and keycode == 120:
                self._LineNumber_Subtract(Clipboard.paste())

                if not self.__unredo["undo"]: self.__unredo["undo"] = True

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

            # [L_CTRL, R_CTRL]
            elif keycode in [305, 306]: self.__ctrl = False

            # [L_SHIFT, R_SHIFT]
            elif keycode in [304, 303]: self.__shift = False

    def _LineNumber_Unknown(self, substring:str|None=None) -> None:
        """This is a helper to recalculate the line numbers.

        :param substring:   The text to process as string.
        :return:            Nothing."""
        reference:int = len(self._Text.lines)

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
            self._LineNumber.text = "1"

            for line in range(2, reference + 1):
                self._LineNumber.text += f"\n{line}"

            self.__lines = reference
            self._auto_width_ln()
            Clock.schedule_once(lambda _:self._auto_text_size())

            # Recalculate the line number size (0-1)
            self.__normalized_line_height = self._Text.line_height / self._Text.height
            self.__normalized_line_height_view = self._Text.line_height / self.__Scroll_Text.height

    def _LineNumber_Add(self, substring:str|None=None, amount:int=0) -> None:
        """Add the line numbers.

        :param substring:   The text to process as string.
        :param amount:      The amount of addition.
        :return:            Nothing."""
        try:
            t = ThreadLinesAdd(self.__lines, substring, amount)
            self._LineNumber.text += t.text
            self.__lines += t.lines

            # Recalculate the line number size (0-1)
            self.__normalized_line_height = self._Text.line_height / self._Text.height
            self.__normalized_line_height_view = self._Text.line_height / self.__Scroll_Text.height
        except ValueError: pass

        # Update the line number width to mach the correct new size
        self._auto_width_ln()
        Clock.schedule_once(lambda _:self._auto_text_size())

    def _LineNumber_Subtract(self, substring=None, amount: int=0) -> None:
        """Subtract the line numbers.

        :param substring:   The text to process as string.
        :param amount:      The amount of subtraction.
        :return: Nothing."""
        try:
            t = ThreadLinesSubstract(self._LineNumber.text, substring, amount)
            self._LineNumber.text = t.text
            self.__lines -= t.lines

            # Recalculate the line number size (0-1)
            self.__normalized_line_height = self._Text.line_height / self._Text.height
            self.__normalized_line_height_view = self._Text.line_height / self.__Scroll_Text.height
        except ValueError: pass

        # Update the line number width to mach the correct new size
        self._auto_width_ln()
        Clock.schedule_once(lambda _: self._auto_text_size())

    def _auto_width_ln(self) -> None:
        """Set the maximum line number width need it to show up.
        If required more space will extrude, otherwise will use the provided line number width.

        :return: Nothing."""
        required:int = self.__width_ln_min * len(str(self.__lines)) + self.padding_ln[0] + self.padding_ln[1]
        size:int = max(self.width_ln, required)

        self.__Scroll_LineNumber.width = self._LineNumber.width = size

    def _sync_padding(self) -> None:
        """Sync the vertical padding to avoid line number offset.

        :return: Nothing."""
        # 0 = left, 1 = top, 2 = right, 3 = bottom
        self.padding_ln[1] = self.padding_txt[1] = max(self.padding_ln[1], self.padding_txt[1])
        self.padding_ln[3] = self.padding_txt[3] = max(self.padding_ln[3], self.padding_txt[3])

    def _auto_text_size(self) -> None:
        """Find the optimal text size need it to show up.

        :return: Nothing."""
        # TODO: New logic to speed up the response time on bigger text
        self.__width_txt_min = FontMeasure(self.font_name, self.font_size).get_width_of(self.text)
        self._update_text_size()

    def _update_text_size(self) -> None:
        """Like how the name is suggesting, the purpose of this logic is to update the text size.
        And the line numbers vertical size off course.

        :return: Nothing."""
        padding_horizontal:int = self.padding_txt[0] + self.padding_txt[2]

        self._Text.width = max(self.__Scroll_Text.width, self.__width_txt_min + padding_horizontal)
        self._Text.height = max(self.__Scroll_Text.height, self._Text.minimum_height)

        self._LineNumber.height = self._Text.height
        self.__update_hidden_size()

        # Recalculate the line number size (0-1)
        self.__normalized_line_height = self._Text.line_height / self._Text.height
        self.__normalized_line_height_view = self._Text.line_height / self.__Scroll_Text.height

    def _find_width_ln_min(self) -> None:
        """Find the minimum width need it to display one line number character.

        :return: Nothing."""
        measure = FontMeasure(self.font_name, self.font_size)

        self.__width_ln_min = max(measure.get_width_of(str(number)) for number in range(10))

    def Theme(self, crash:bool=True, **kwargs) -> None:
        """Change the style dynamically with some custom
        key arguments like:

        [ type: str ]
            font_name, align_ln, align_txt

        [ type: int ]
            font_size, width_tab

        [ type: int | float ]
            width_ln, width_cursor, width_scroll,
            spacing, margin_scroll

        [ type: bool ]
            RTL, auto_indent

        [ type: list | tuple ]
            padding_ln, padding_txt, margin_scroll_cursor

        [ type: ColorProperty | str | list | tuple ]
            color_ln, color_txt, color_info,
            color_cursor, color_selection,
            color_scroll, color_scroll_inactive,
            bg_ln, bg_txt, bg_info

        .. Note::
            Will log an error message and will crash the application in case
            the argument type is not one of listed ones.
            If you want to not crash it, then set `crash` value to False, but
            will log a warning message instead.

        :param crash:   Crashing the app.
        :return: Nothing.
        """
        NAME:str = "%s.%s" % (self.__class__.__name__, THIS().f_code.co_name)
        CHECKING = Check(NAME, close=crash)

        updated_padding:bool = False
        updated_font:bool = False
        info:dict[str, bool] = {"update":False, "color":False, "bg":False}

        for key, arg in kwargs.items():
            if key == "width_ln":
                with CHECKING.arg_type(key, arg, int, float, ignored=[bool]):
                    self.width_ln = float(arg)
                    self._auto_width_ln()

            elif key == "width_tab":
                with CHECKING.arg_type(key, arg, int, ignored=[bool]):
                    self.width_tab = int(arg)
                    self._Text.tab_width = self.width_tab
                    self.__construct_info(tabs=True)

            elif key == "width_cursor":
                with CHECKING.arg_type(key, arg, int, float, ignored=[bool]):
                    self.width_cursor = float(arg)
                    self._Text.cursor_width = self.width_cursor

            elif key == "width_scroll":
                with CHECKING.arg_type(key, arg, int, float, ignored=[bool]):
                    self.width_scroll = float(arg)
                    self.__Scroll_Text.bar_width = self.width_scroll

            elif key == "margin_scroll":
                with CHECKING.arg_type(key, arg, int, float, ignored=[bool]):
                    self.width_cursor = float(arg)
                    self.__Scroll_Text.bar_margin = self.width_cursor

            elif key == "margin_scroll_cursor":
                with CHECKING.arg_type(key, arg, list, tuple, ignored=[bool]):
                    if len(arg) != 4: arg = List(*arg, _len=4, _type=float)
                    self.margin_scroll_cursor = arg

            elif key == "font_name":
                with CHECKING.arg_type(key, arg, str):
                    self._LineNumber.font_name = self._Text.font_name = self.font_name = arg
                    updated_font = True

            elif key == "font_size":
                with CHECKING.arg_type(key, arg, int):
                    self._LineNumber.font_size = self._Text.font_size = self.font_size = arg
                    updated_font = True

            elif key == "RTL":
                with CHECKING.arg_type(key, arg, bool, int):
                    self.RTL = bool(arg)
                    self._Text.base_direction = "rtl" if self.RTL else "ltr"

            elif key == "auto_indent":
                with CHECKING.arg_type(key, arg, bool, ignored=[int]):
                    self.auto_indent = bool(arg)
                    self._Text.auto_indent = self.auto_indent

            elif key == "padding_ln":
                with CHECKING.arg_type(key, arg, list, tuple):
                    if len(arg) != 4: arg = List(*arg, _len=4, _type=float)
                    self.padding_ln = arg
                    updated_padding = True

            elif key == "padding_txt":
                with CHECKING.arg_type(key, arg, list, tuple):
                    if len(arg) != 4: arg = List(*arg, _len=4, _type=float)
                    self.padding_txt = arg
                    updated_padding = True

            elif key == "spacing":
                with CHECKING.arg_type(key, arg, int, float, ignored=[bool]):
                    self.spacing = float(arg)
                    self._Text.line_spacing = self.spacing
                    self._LineNumber.line_spacing = self.spacing

            elif key == "color_ln":
                with CHECKING.RGBA(key, arg, ColorProperty, str, list, tuple):
                    self.color_ln = arg
                    self._LineNumber.disabled_foreground_color = arg

            elif key == "color_txt":
                with CHECKING.RGBA(key, arg, ColorProperty, str, list, tuple):
                    self.color_txt = arg
                    self._Text.foreground_color = arg

            elif key == "color_cursor":
                with CHECKING.RGBA(key, arg, ColorProperty, str, list, tuple):
                    self.color_cursor = arg
                    self._Text.cursor_color = arg

            elif key == "color_selection":
                with CHECKING.RGBA(key, arg, ColorProperty, str, list, tuple):
                    self.color_selection = arg
                    self._Text.selection_color = arg

            elif key == "color_scroll":
                with CHECKING.RGBA(key, arg, ColorProperty, str, list, tuple):
                    self.color_scroll = arg
                    self.__Scroll_Text.bar_color = arg

            elif key == "color_scroll_inactive":
                with CHECKING.RGBA(key, arg, ColorProperty, str, list, tuple):
                    self.color_scroll_inactive = arg
                    self.__Scroll_Text.bar_inactive_color = arg

            elif key == "color_info":
                with CHECKING.RGBA(key, arg, ColorProperty, str, list, tuple):
                    self.color_info = arg
                    self.__Info.disabled_foreground_color = arg
                    info["color"] = True

            elif key == "bg_ln":
                with CHECKING.RGBA(key, arg, ColorProperty, str, list, tuple):
                    self.bg_ln = arg
                    self._LineNumber.background_color = arg
                    info["update"] = True

            elif key == "bg_txt":
                with CHECKING.RGBA(key, arg, ColorProperty, str, list, tuple):
                    self.bg_txt = arg
                    self._Text.background_color = arg
                    self.background_color = arg

            elif key == "bg_info":
                with CHECKING.RGBA(key, arg, ColorProperty, str, list, tuple):
                    self.bg_info = arg
                    self.__Info.background_color = arg
                    info["bg"] = True

            elif key == "align_ln":
                with CHECKING.arg_type(key, arg, str):
                    self.align_ln = arg
                    self._LineNumber.halign = arg

            elif key == "align_txt":
                with CHECKING.arg_type(key, arg, str):
                    self.align_txt = arg
                    self._Text.halign = arg

            else: WARNING("%s, do not have \"%s\" defined.", NAME, key)

        self._LineNumber._trigger_update_graphics()
        self._Text._trigger_update_graphics()

        # If padding was changed
        if updated_padding:
            self._sync_padding()
            self._LineNumber.padding = self.padding_ln
            self._Text.padding = self.padding_txt

            # In case the font was not changed
            if not updated_font:
                self._auto_width_ln()
                Clock.schedule_once(lambda _:self._auto_text_size())

        # If font was changed
        if updated_font:
            self._find_width_ln_min()
            self._auto_width_ln()
            Clock.schedule_once(lambda _:(self._auto_text_size(),
                                          self._Text.cancel_selection()))

        # If line number background was changed but not and the info colors
        if info["update"]:
            if not info["bg"]:
                self.bg_info = Make.Color(self.bg_ln)
                self.__Info.background_color = self.bg_info

            if not info["color"]:
                self.color_info = Make.Color(self.color_ln, .25)
                self.__Info.disabled_foreground_color = self.color_info

    @deprecated(msg="Use 'text' instead with out round brackets. "
                "Function 'TextInput_LN.GetText()' will be removed on the next two updates.")
    def GetText(self) -> str: return self.text

    @property
    def text(self) -> str:
        """Provide you the created text.

        :return:    The text variable of type string (from kivy AliasProperty)."""
        return self._Text.text

    @text.setter
    def text(self, value:any) -> None:
        """Let you setting a new text value.

        >>> self.MyText = TextInput_LN()
        >>> self.MyText.text = True
        >>> self.MyText.text += " text here..."
        >>> # True text here...

        :param value:   The new text.
        :return:        Nothing."""
        self._Text.text = str(value)
        self._LineNumber_Unknown()

    @text.deleter
    def text(self) -> None:
        """Let you deleting the text on unusual way.

        >>> self.MyText = TextInput_LN()
        >>> del self.MyText.text

        :return: Nothing."""
        self.Clear()

    def SetText(self, *values:any, sep:str|None=" ", end:str|None="\n") -> None:
        """**SetText** let you setting a new text by replacing the existing one.

        :param values:  Arguments to be added as text.
        :param sep:     String inserted between values.
        :param end:     String appended after the last value.
        :return:        Nothing.

        >>> self.list = ["The fox", "got a chicken"]
        >>> self.MyText = TextInput_LN()
        >>>
        >>> self.MyText.SetText("Your text is here.")
        >>> self.MyText.SetText(*self.list, sep="-", end=".")
        """
        self._Text.text = Make.Text(*values, sep=sep, end=end)
        self._LineNumber_Unknown()

    def AddText(self, *values:any, sep:str|None=" ", end:str|None="\n") -> None:
        """**AddText** let you adding text after the existing one.

        :param values:  Arguments to be appended after the text.
        :param sep:     String inserted between values.
        :param end:     String appended after the last value.
        :return:        Nothing.

        >>> self.list = ["The lazy cat", "got nothing"]
        >>> self.MyText = TextInput_LN()
        >>>
        >>> self.MyText.AddText("Some text is here.")
        >>> self.MyText.AddText(*self.list, sep="-", end=".")
        """
        text:str = Make.Text(*values, sep=sep, end=end)
        self._Text.text += text
        self._LineNumber_Add(text)

    def InsertText(self, *values:any, sep:str|None=" ", end:str|None="\n") -> None:
        """**InsertText** let you adding text on the cursor position.

        :param values:  Arguments to be appended after the text.
        :param sep:     String inserted between values.
        :param end:     String appended after the last value.
        :return:        Nothing.

        >>> self.list = ["The faster rat", "got cheese"]
        >>> self.MyText = TextInput_LN()
        >>>
        >>> self.MyText.InsertText("Other text is here.")
        >>> self.MyText.InsertText(*self.list, sep="-", end=".")
        """
        text:str = Make.Text(*values, sep=sep, end=end)
        self._Text.insert_text(text)
        self._LineNumber_Add(text)

    def Clear(self, _from:int=0, _to:int=-1) -> None:
        """Deleting text in the specified range.

        :param _from:   Clear from.
        :param _to:     Clear to.
        :return:        Nothing.
        :raise WARNING: If indexes are the same."""
        # Revert indexes to maintain the order from min to max
        if _from > _to > 0 or _from < _to > 0: _from, _to = _to, _from

        # If indexes are the same log and warning.
        elif _from == _to:
            NAME:str = "%s.%s" % (self.__class__.__name__, THIS().f_code.co_name)
            index:int = (len(self.text) - _from) if _from < 0 else _from
            WARNING(f"{NAME}: ('_')☞ Are not any hidden characters on index {index}.")

        else:
            fStart:bool = _from == 0
            fEnd:bool = _to == -1 or _to == len(self._Text.text)

            # If clearing from the start to the end
            if fStart and fEnd:
                self._Text.text, self._LineNumber.text, self.__lines = "", "1", 1
                self._auto_width_ln()
                self._Text.size = self.__Scroll_Text.size

                # Recalculate the line number size (0-1)
                self.__normalized_line_height = self._Text.line_height / self._Text.height
                self.__normalized_line_height_view = self._Text.line_height / self.__Scroll_Text.height

            # Otherwise, clear the specified range
            else:
                txtStart:str = "" if fStart else self._Text.text[:_from]
                txtEnd:str = "" if fEnd else self._Text.text[_to:]
                self._Text.text = txtStart + txtEnd
                self._LineNumber_Unknown()

    def binding(self, **kwargs) -> None:
        """Useful for controlling text binding.

        The key arguments are the same as :class:`kivy.uix.textinput.TextInput` class ones because by calling this,
        in fact you are calling **:meth:`kivy.uix.textinput.TextInput.bind`** from inside this class.

        :return: Nothing."""
        self._Text.bind(**kwargs)

