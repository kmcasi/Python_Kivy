# // IMPORT
from builtins import staticmethod, property
from logging import warning as WARNING
from sys import _getframe as THIS
from os import linesep as OS_LN_SEP
from string import digits as NUMBERS

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.core.text import DEFAULT_FONT
from kivy.properties import OptionProperty, VariableListProperty, ReferenceListProperty
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ColorProperty
from kivy.utils import deprecated

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from lib.OverlayLayout import OverlayLayout
from lib.ToolTip import ToolTip
from lib.helper.Font import FontMeasure
from lib.helper.List import List
from lib.helper.Thread import ThreadLinesAdd, ThreadLinesSubstract
from lib.helper.utils import Make, Check, clamp, normalize

"""
Line numbers width are changed dynamically if is need it so you can set 'width_line'
to zero to get just the required width.

In my kivy source code I changed redo from CTRL+R to CTRL+Y. In case you
want to use R instead of Y (or what ever is your redo bind) then go an look
for '_on_key_up' event and you will find the "CTRL + Y" elif statement and replace
the key code. I wrote another comment and there as a reminder.
Use your IDE/Editor and search for "CTRL + Y", will be much easier to find it.
(Usually Ctrl+F is a common short cut for that.)
"""


# // LOGIC
class TextInput_LN(BoxLayout):
    align_ln = OptionProperty("auto", options=["left", "center", "right", "auto"])
    '''Horizontal alignment of the line numbers.
    
    Possible values are: "auto", "left", "center" and "right".
    
    Auto will attempt to autodetect horizontal alignment for RTL text (Pango only), otherwise it behaves like "left".

    :attr:`align_ln` is an :class:`~kivy.properties.OptionProperty` and defaults to "auto".
    '''

    align_txt = OptionProperty("auto", options=["left", "center", "right", "auto"])
    '''Horizontal alignment of the text.
    
    Possible values are: "auto", "left", "center" and "right".
    
    Auto will attempt to autodetect horizontal alignment for RTL text (Pango only), otherwise it behaves like "left".

    :attr:`align_txt` is an :class:`~kivy.properties.OptionProperty` and defaults to "auto".
    '''

    animations = BooleanProperty(True)
    '''Use animations.

    :attr:`animations` is a :class:`~kivy.properties.BooleanProperty` and defaults to True.
    '''

    auto_indent = BooleanProperty(True)
    '''Automatically indent multiline text.

    :attr:`auto_indent` is a :class:`~kivy.properties.BooleanProperty` and defaults to True.
    '''

    bg_info = ColorProperty("262626")
    '''Background color of the information's, in RGBA format.
    
    This is deprecated and will be removed on the next update. Will be available on :class:`TextEditor.TextEditor`.
    
    :attr:`bg_info` is a :class:`~kivy.properties.ColorProperty` and defaults to "#262626FF".
    '''

    bg_ln = ColorProperty("313335")
    '''Background color of the line numbers, in RGBA format.
    
    :attr:`bg_ln` is a :class:`~kivy.properties.ColorProperty` and defaults to "#313335FF".
    '''

    bg_txt = ColorProperty("2B2B2B")
    '''Background color of the text, in RGBA format.
    
    :attr:`bg_txt` is a :class:`~kivy.properties.ColorProperty` and defaults to "#2B2B2BFF".
    '''

    color_cursor = ColorProperty("806F9F")
    '''Color of the cursor, in RGBA format.
    
    :attr:`color_cursor` is a :class:`~kivy.properties.ColorProperty` and defaults to "#806F9FFF".
    '''

    color_info = ColorProperty("646464")
    '''Color of the text information's, in RGBA format.
    
    This is deprecated and will be removed on the next update. Will be available on :class:`TextEditor.TextEditor`.
    
    :attr:`color_info` is a :class:`~kivy.properties.ColorProperty` and defaults to "#646464FF".
    '''

    color_line_active = ColorProperty("3F3F3F80")
    '''Color of the active line, in RGBA format.
    
    :attr:`color_line_active` is a :class:`~kivy.properties.ColorProperty` and defaults to "#3F3F3F80".
    '''

    color_ln = ColorProperty("606366")
    '''Color of the line numbers, in RGBA format.
    
    :attr:`color_ln` is a :class:`~kivy.properties.ColorProperty` and defaults to "#606366FF".
    '''

    color_scroll = ColorProperty("A6A6A680")
    '''Color of the active scroll bars, in RGBA format.
    
    :attr:`color_scroll` is a :class:`~kivy.properties.ColorProperty` and defaults to "#A6A6A680".
    '''

    color_scroll_inactive = ColorProperty("A6A6A647")
    '''Color of the inactive scroll bars, in RGBA format.
    
    :attr:`color_scroll_inactive` is a :class:`~kivy.properties.ColorProperty` and defaults to "#A6A6A647".
    '''

    color_selection = ColorProperty("0066994D")
    '''Color of the selection, in RGBA format.
    
    :attr:`color_selection` is a :class:`~kivy.properties.ColorProperty` and defaults to "#0066994D".
    '''

    color_txt = ColorProperty("A9B7C6")
    '''Color of the text, in RGBA format.
    
    :attr:`color_txt` is a :class:`~kivy.properties.ColorProperty` and defaults to "#A9B7C6FF".
    '''

    cursor_blink = BooleanProperty(True)
    '''Whether the graphic cursor should blink or not.

    :attr:`cursor_blink` is a :class:`~kivy.properties.BooleanProperty` and defaults to True.
    '''

    font_name = StringProperty(DEFAULT_FONT)
    '''Filename of the font to use for the text and the line numbers. The path can be absolute or relative.
    
    Relative paths are resolved by the :func:`~kivy.resources.resource_find` function.

    :attr:`font_name` is a :class:`~kivy.properties.StringProperty` and defaults to 'Roboto'.
    This value is taken from :class:`~kivy.config.Config`.
    '''

    font_size = NumericProperty("18sp")
    '''Font size of the text and the line numbers in pixels.

    :attr:`font_size` is a :class:`~kivy.properties.NumericProperty` and defaults to 18 :attr:`~kivy.metrics.sp`.
    '''

    info_font_name = StringProperty(DEFAULT_FONT)
    '''Filename of the font to use for the text information's. The path can be absolute or relative.
    
    Relative paths are resolved by the :func:`~kivy.resources.resource_find` function.
    
    This is deprecated and will be removed on the next update. Will be available on :class:`TextEditor.TextEditor`.

    :attr:`info_font_name` is a :class:`~kivy.properties.StringProperty` and defaults to 'Roboto'.
    This value is taken from :class:`~kivy.config.Config`.
    '''

    info_font_size = NumericProperty("14sp")
    '''Font size of the information's in pixels.
    
    This is deprecated and will be removed on the next update. Will be available on :class:`TextEditor.TextEditor`.

    :attr:`info_font_size` is a :class:`~kivy.properties.NumericProperty` and defaults to 14 :attr:`~kivy.metrics.sp`.
    '''

    margin_scroll = NumericProperty(0)
    '''Margin between the scroll bars and the margins of the text.

    :attr:`margin_scroll` is a :class:`~kivy.properties.NumericProperty`, default to 0.
    '''

    margin_scroll_cursor = VariableListProperty([31.5], lenght=4)
    '''Padding between the cursor and the text area.
    
    When the cursor is out side of this limits the text will auto scrolling to keep the cursor inside the visible area.
    
    Padding can be provided in multiple ways:
    
        [1] \u279c [padding_left, padding_top, padding_right, padding_bottom]
        
        [2] \u279c [padding_horizontal, padding_vertical]
        
        [3] \u279c [padding]

    :attr:`margin_scroll_cursor` is a :class:`~kivy.properties.VariableListProperty` and 
    defaults to [31.5, 31.5, 31.5, 31.5].
    '''

    padding_info = VariableListProperty([6, 3])
    '''Padding of the text information's.
    
    This is deprecated and will be removed on the next update. Will be available on :class:`TextEditor.TextEditor`.
    
    Padding can be provided in multiple ways:
    
        [1] \u279c [padding_left, padding_top, padding_right, padding_bottom]
        
        [2] \u279c [padding_horizontal, padding_vertical]
        
        [3] \u279c [padding]

    :attr:`padding_info` is a :class:`~kivy.properties.VariableListProperty` and defaults to [6, 3, 6, 3].
    '''

    padding_ln = VariableListProperty([3], length=2)
    '''Horizontal padding of the line numbers.
    
    Padding can be provided in multiple ways:
        
        [1] \u279c [padding_left, padding_right]
        
        [2] \u279c [padding]

    :attr:`padding_ln` is a :class:`~kivy.properties.VariableListProperty` and defaults to [3, 3].
    '''

    padding_txt = VariableListProperty([6])
    '''Padding of the text.
    
    Padding can be provided in multiple ways:
    
        [1] \u279c [padding_left, padding_top, padding_right, padding_bottom]
        
        [2] \u279c [padding_horizontal, padding_vertical]
        
        [3] \u279c [padding]

    :attr:`padding_txt` is a :class:`~kivy.properties.VariableListProperty` and defaults to [6, 6, 6, 6].
    '''

    pos_ln = OptionProperty("auto", options=["left", "right", "auto"])
    '''Position of the line numbers.
    
    Possible values are: "auto", "left" and "right".
    
    Auto will attempt to autodetect horizontal alignment for RTL text (Pango only), otherwise it behaves like "left".
    
    :attr:`pos_ln` is an :class:`~kivy.properties.OptionProperty`, defaults to "auto".
    '''

    pos_scroll_h = OptionProperty("bottom", options=["top", "bottom"])
    '''Position of the horizontal scroll bar.
    
    Possible values are "top" and "bottom".

    :attr:`pos_scroll_h` is an :class:`~kivy.properties.OptionProperty`, defaults to "bottom".
    '''

    pos_scroll_v = OptionProperty("right", options=["left", "right"])
    '''Position of the vertical scroll bar.
    
    Possible values are "left" and "right".

    :attr:`pos_scroll_v` is an :class:`~kivy.properties.OptionProperty`, defaults to "right".
    '''

    pos_scroll = ReferenceListProperty(pos_scroll_h, pos_scroll_v)
    '''Position of the scroll bars.

    :attr:`pos_scroll` is a :class:`~kivy.properties.ReferenceListProperty` of
    (:attr:`pos_scroll_h`, :attr:`pos_scroll_v`)
    '''

    readonly = BooleanProperty(False)
    '''If True, the user will not be able to change the content of a textinput.

    :attr:`readonly` is a :class:`~kivy.properties.BooleanProperty` and defaults to False.
    '''

    RTL = BooleanProperty(False)
    '''Use right to left as base direction of the text, this impacts horizontal alignment and the line numbers position
    when :attr:`align_txt`, :attr:`align_ln` and :attr:`pos_ln` are `auto` (the default).

    :attr:`RTL` is a :class:`~kivy.properties.BooleanProperty` and defaults to False.
    '''

    spacing_content = NumericProperty(0)
    '''Space taken up between the content.

    :attr:`spacing_content` is a :class:`~kivy.properties.NumericProperty` and defaults to 0.
    '''

    spacing_info = VariableListProperty([10, 0], length=2)
    '''Spacing of the text information's.
    
    This is deprecated and will be removed on the next update. Will be available on :class:`TextEditor.TextEditor`.
    
    Spacing can be provided in multiple ways:
        
        [1] \u279c [spacing_horizontal, spacing_vertical]
        
        [2] \u279c [spacing]

    :attr:`spacing_info` is a :class:`~kivy.properties.VariableListProperty` and defaults to [10, 0].
    '''

    spacing_line = NumericProperty(0)
    '''Space taken up between the lines.

    :attr:`spacing_line` is a :class:`~kivy.properties.NumericProperty` and defaults to 0.
    '''

    width_cursor = NumericProperty("2dp")
    '''Thickness of the cursor.

    :attr:`width_cursor` is a :class:`~kivy.properties.NumericProperty` and defaults to 2 :attr:`~kivy.metrics.dp`.
    '''

    width_ln = NumericProperty("24dp")
    '''Minimum width of the line numbers.
    
    Line numbers width is determined automatically base on :attr:`padding_ln`, :attr:`font_name`
    , :attr:`font_size` and self context (number).

    :attr:`width_ln` is a :class:`~kivy.properties.NumericProperty` and defaults to 24 :attr:`~kivy.metrics.dp`.
    '''

    width_tab = NumericProperty(4)
    '''By default, each tab will be replaced by four spaces on the text. 
    You can set a lower or higher value.

    :attr:`width_tab` is a :class:`~kivy.properties.NumericProperty` and defaults to 4.
    '''

    width_scroll = NumericProperty("11dp")
    '''Thickness of the scroll bars.

    :attr:`width_scroll` is a :class:`~kivy.properties.NumericProperty` and defaults to 11.5 :attr:`~kivy.metrics.dp`.
    '''


    def __init__(self, **kwargs):
        """Custom TextInput class with line numbers.

        .. NOTE::
            If you are useeing **bind** you will control the parent class witch
            is **BoxLayout**. If you want to control the TextInput bind use **binding**.
            Like and example see below.

            >>> self.myText = TextInput_LN()
            >>> self.myText.binding(text=self.your_text_bind)
        """
        super(TextInput_LN, self).__init__(**kwargs)

        # Private variables
        self.__lines:int = 1
        self.__width_ln_min:int = 0
        self.__width_txt_min:int = 0
        self.__focused:bool = False
        self.__ctrl:bool = False
        self.__shift:bool = False
        self.__unredo:dict[str, bool] = {"undo": False, "redo": False}
        self.__selection_text_exist:bool = False
        self.__selection_text:dict[str, int] = {"from":0, "to":0}
        self.__scroll_horizontal:dict[str, bool|str] = {"flag":False, "button":"scrollright"}
        self.__os_sep:dict[str, str] = {"\r\n":"CRLF", "\r":"CR", "\n":"LF"}
        self.__file_ln_break:str = self.__os_sep[OS_LN_SEP]
        self.__file_encoding:str = "UTF-8"
        self.__hidden_height:float = 0.0
        self.__hidden_width:float = 0.0
        self.__normalized_line_height:float = 0.0
        self.__normalized_line_height_view:float = 0.0
        self.__animations_line_active:bool = False
        self.__animations_auto_scroll:bool = False
        self.__animations_progress:dict[any, Animation] = {}
        self.__infos:dict[str, Label] = {}
        self.__area_scroll_h:List = List(0, size=2, _type=float)
        self.__area_scroll_v:List = List(0, size=2, _type=float)

        # Info control panel
        self.__info_count_only_visible_chars:bool = True

        # UIX elements
        self.__Layout = BoxLayout(orientation="vertical", spacing=self.spacing_content)
        self.__Layout_ln = OverlayLayout()
        self.__Layout_txt = OverlayLayout()
        self.__Layout_info = OverlayLayout()
        self.__Info = StackLayout(orientation="rl-bt", padding=self.padding_info)
        self.__Layout_Content = BoxLayout(orientation="horizontal", spacing=self.spacing_content)

        self.__Scroll_LineNumber = ScrollView(always_overscroll=False, scroll_type=["bars", "content"]
                                              , width=self.width_ln, do_scroll_x=False
                                              , bar_width=0, bar_margin=0
                                              , bar_color="00000000", bar_inactive_color="00000000")

        self.__Scroll_Text = ScrollView(always_overscroll=False, scroll_type=["bars"]
                                        , bar_width=self.width_scroll, bar_margin=self.margin_scroll
                                        , bar_color=self.color_scroll, bar_inactive_color=self.color_scroll_inactive
                                        , bar_pos_x = self.pos_scroll_h, bar_pos_y=self.pos_scroll_v)

        self._LineNumber = TextInput(text="1", disabled=True, do_wrap=False, halign=self.align_ln
                                     , font_name=self.font_name, font_size=self.font_size
                                     , width=self.width_ln, padding=self.padding_ln, line_spacing=self.spacing_line
                                     , disabled_foreground_color=self.color_ln, background_color="00000000")

        self._Text = TextInput(auto_indent=self.auto_indent, do_wrap=False, tab_width=self.width_tab
                               , halign=self.align_txt, base_direction="rtl" if self.RTL else "ltr"
                               , font_name=self.font_name, font_size=self.font_size
                               , padding=self.padding_txt, cursor_width=self.width_cursor
                               , line_spacing=self.spacing_line, cursor_blink=self.cursor_blink, readonly=self.readonly
                               , foreground_color=self.color_txt, background_color="00000000"
                               , cursor_color=self.color_cursor, selection_color=self.color_selection)

        self.__Layout_BG_hover_info = FloatLayout(opacity=0)
        self.__BG_ln:Image = Image(color=self.bg_ln, allow_stretch=True, keep_ratio=False)
        self.__BG_txt:Image = Image(color=self.bg_txt, allow_stretch=True, keep_ratio=False)
        self.__BG_info:Image = Image(color=self.bg_info, allow_stretch=True, keep_ratio=False)
        self.__BG_hover_info = Image(color=self.bg_ln, allow_stretch=True, keep_ratio=False
                                     , size_hint=(None, None), size=(0, 0))
        self.__Line_active:Image = Image(color=self.color_line_active, allow_stretch=True, keep_ratio=False, opacity=0)

        for info_key in ["source", "tabs", "encoding", "ln_sep", "cursor"]:
            self.__infos[info_key] = Label(color=self.color_info, size_hint=(None, 1), padding=self.spacing_info,
                                           font_name=self.info_font_name, font_size=self.info_font_size)

        # ToolTip's
        self.__tt_ic = ToolTip(self.__infos["cursor"], position=["top"], animations=self.animations,
                               text="Cursor position "
                                    "[size={size}]([color={color}][b]{subtext}[/b][/color])[/size]"
                                    "\n\n[color={todo_color}]TODO:[size={todo_size}][/size][/color]\n{todo}".format(
                                   size = int(self.info_font_size),
                                   color = Make.Color(self.color_info, .1, True),
                                   subtext = "Ctrl+G",
                                   todo_color="#A8C023",
                                   todo_size=24,
                                   todo="Move cursor to the specified\nposition will be available\non the next update.")
                               )
        self.__tt_il = ToolTip(self.__infos["ln_sep"], position=["top"], animations=self.animations,
                               text="Line separator: [color={color}][b]{subtext}[/b][/color]"
                                    "\n\n[color={todo_color}]TODO:[size={todo_size}][/size][/color]\n{todo}".format(
                                   color = Make.Color(self.color_info, .1, True),
                                   subtext = self.__file_ln_break.replace("CR", "\\r").replace("LF", "\\n"),
                                   todo_color="#A8C023",
                                   todo_size=24,
                                   todo="Changing the line separator\nwill be available on\nthe next update.")
                               )
        self.__tt_ie = ToolTip(self.__infos["encoding"], position=["top"], animations=self.animations,
                               text="File encoding"
                                    "\n\n[color={todo_color}]TODO:[size={todo_size}][/size][/color]\n{todo}".format(
                                   todo_color="#A8C023",
                                   todo_size=24,
                                   todo="Changing the file encoding\nwill be available on\nthe next update.")
                               )
        self.__tt_it = ToolTip(self.__infos["tabs"], position=["top"], animations=self.animations,
                               text="Tab size"
                                    "\n\n[color={todo_color}]TODO:[size={todo_size}][/size][/color]\n{todo}".format(
                                   todo_color="#A8C023",
                                   todo_size=24,
                                   todo="Changing the tab size\nwill be available on\nthe next update.")
                               )
        self.__tt_is = ToolTip(self.__infos["source"], position=["top"], animations=self.animations,
                               text="File type"
                                    "\n\n[color={todo_color}]TODO:[size={todo_size}][/size][/color]\n{todo}".format(
                                   todo_color="#A8C023",
                                   todo_size=24,
                                   todo="This information's will\nbe removed on the next\nupdate.\nWill be available "
                                        "on the\ntext editor class.")
                               )

        # Settings
        self._update_info(ln_sep=True, encoding=True, tabs=True, source="text")
        self.__background()
        self.__size_hint()
        self.__add_widget()
        self.__bind()
        self.__fbind()
        self.__auto_RTL()
        self.__find_width_ln_min()
        self.__auto_width_ln()

    def __compute_bool(self, *noUse) -> None:
        self.__tt_ie.animations = self.animations
        self.__tt_it.animations = self.animations
        self.__tt_is.animations = self.animations
        self.__tt_ic.animations = self.animations
        self.__tt_il.animations = self.animations
        self._Text.auto_indent = self.auto_indent

    def __compute_color(self, *noUse) -> None:
        self.__BG_info.color = self.bg_info
        self.__BG_ln.color = self.bg_ln
        self.__BG_txt.color = self.bg_txt
        self._Text.cursor_color = self.color_cursor
        self.__Line_active.color = self.color_line_active
        self._LineNumber.disabled_foreground_color = self.color_ln
        self.__Scroll_Text.bar_color = self.color_scroll
        self.__Scroll_Text.bar_inactive_color = self.color_scroll_inactive
        self._Text.selection_color = self.color_selection
        self._Text.foreground_color = self.color_txt

        for index in self.__infos.values():
            index.color = self.color_info

    def __compute_font(self, *noUse) -> None:
        bk_font:tuple = (self._Text.cursor, self.__Scroll_Text.scroll_x, self.__Scroll_Text.scroll_y)

        self._LineNumber.font_name = self._Text.font_name = self.font_name
        self._LineNumber.font_size = self._Text.font_size = self.font_size

        self.__find_width_ln_min()
        self.__auto_width_ln()
        Clock.schedule_once(lambda _:(self.__auto_text_size(),
                                      self.__fix_font_changes_bug(*bk_font),
                                      self._Text.cancel_selection()))

    def __compute_padding(self, *noUse) -> None:
        self._LineNumber.padding = [self.padding_ln[0], self.padding_txt[1], self.padding_ln[1], self.padding_txt[3]]
        self._Text.padding = self.padding_txt

        self.__auto_width_ln()
        self.__auto_text_size()

    def __compute_position(self, *noUse) -> None:
        self.__Scroll_Text.bar_pos_x = self.pos_scroll_h
        self.__Scroll_Text.bar_pos_y = self.pos_scroll_v
        self._LineNumber.halign = self.align_ln
        self._Text.halign = self.align_txt

        self.__compute_swipe(self.pos_ln)

    def __compute_RTL(self, *noUse) -> None:
        self._Text.base_direction = "rtl" if self.RTL else "ltr"
        self._LineNumber.base_direction = "ltr" if self.RTL else "rtl"

        self.__compute_swipe("auto")
        self.__auto_scroll()

    def __compute_size(self, *noUse) -> None:
        self.__Scroll_Text.bar_width = self.width_scroll
        self.__Scroll_Text.bar_margin = self.margin_scroll

        self.__auto_width_ln()
        self.__compute_scroll_bar_area()

    def __compute_spacing(self, *noUse) -> None:
        self._Text.line_spacing = self.spacing_line
        self._LineNumber.line_spacing = self.spacing_line

        self.__Layout.spacing = self.spacing_content
        self.__Layout_Content.spacing = self.spacing_content

        self._LineNumber._trigger_update_graphics()
        self._Text._trigger_update_graphics()

    def __compute_swipe(self, side):
        swipe = self.__Layout_Content.children[-1]

        if side == "left" and isinstance(swipe, ScrollView):
            self.__Layout_Content.remove_widget(swipe)
            self.__Layout_Content.add_widget(swipe)

        elif side == "right" and isinstance(swipe, OverlayLayout):
            self.__Layout_Content.remove_widget(swipe)
            self.__Layout_Content.add_widget(swipe)

        elif side == "auto":
            self.__compute_swipe("right" if self.RTL else "left")

        self.__compute_scroll_bar_area()

    def __compute_text(self, *noUse) -> None:
        self._Text.tab_width = int(self.width_tab)
        self._Text.cursor_width = self.width_cursor
        self._Text.cursor_blink = self.cursor_blink
        self._Text.readonly = self.readonly

    def __compute_scroll_bar_area(self) -> None:
        if self.pos_scroll_v == "left":
            self.__area_scroll_v[0] = self.__area_scroll_v[1] = self.__Scroll_Text.x + self.margin_scroll - 1
            self.__area_scroll_v[1] += self.width_scroll + 2

        elif self.pos_scroll_v == "right":
            self.__area_scroll_v[0] = self.__area_scroll_v[1] = self.__Scroll_Text.right - self.margin_scroll + 1
            self.__area_scroll_v[0] -= self.width_scroll + 2

        if self.pos_scroll_h == "bottom":
            self.__area_scroll_h[0] = self.__area_scroll_h[1] = self.__Scroll_Text.y + self.margin_scroll - 1
            self.__area_scroll_h[1] += self.width_scroll + 1

        elif self.pos_scroll_h == "top":
            self.__area_scroll_h[0] = self.__area_scroll_h[1] = self.__Scroll_Text.top - self.margin_scroll + 1
            self.__area_scroll_h[0] -= self.width_scroll + 2

    def __background(self) -> None:
        """Clear the provided background texture, by kivy atlas.

        :return: Nothing."""
        # Remove the background source
        self._Text.background_normal = ""
        self._Text.background_active = ""
        self._LineNumber.background_disabled_normal = ""
        self.background = ""

    def __size_hint(self) -> None:
        """Set the uix size.

        :return: Nothing."""
        # Provide info height base on used font name, size, and vertical padding
        measure = FontMeasure(self.info_font_name, self.info_font_size)
        self.__Layout_info.height = self.padding_info[1] * 2 + measure.get_height_of()

        # Layouts size hint
        self.__Layout_ln.size_hint = (None, 1)
        self.__Layout_txt.size_hint = (None, None)
        self.__Layout_info.size_hint = (1, None)

        # UIX elements size hint
        self._LineNumber.size_hint = (1, None)
        self._Text.size_hint = (None, None)
        # self.__Line_active.size_hint = (1, None)
        self.__Line_active.size_hint = (.5, None)

    def __add_widget(self) -> None:
        """Adding UIX elements.

        :return: Nothing."""
        # Layout: Main
        self.add_widget(self.__Layout)
        self.__Layout.add_widget(self.__Layout_Content)
        self.__Layout.add_widget(self.__Layout_info)

        # Layout: Content
        self.__Layout_Content.add_widget(self.__Layout_ln)
        self.__Layout_Content.add_widget(self.__Scroll_Text)

        # Layout: Line number
        self.__Layout_ln.add_widget(self.__BG_ln)
        self.__Layout_ln.add_widget(self.__Scroll_LineNumber)

        # Layout: Text
        self.__Layout_txt.add_widget(self.__BG_txt)
        self.__Layout_txt.add_widget(self.__Line_active)
        self.__Layout_txt.add_widget(self._Text)

        # Layout: Info
        self.__Layout_BG_hover_info.add_widget(self.__BG_hover_info)
        self.__Layout_info.add_widget(self.__BG_info)
        self.__Layout_info.add_widget(self.__Layout_BG_hover_info)
        self.__Layout_info.add_widget(self.__Info)
        for info in self.__infos.values():
            self.__Info.add_widget(info)

        # ScrollView's
        self.__Scroll_LineNumber.add_widget(self._LineNumber)
        self.__Scroll_Text.add_widget(self.__Layout_txt)

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
                    , mouse_pos=self._on_mouse_pos, on_resize=self._on_resize)

    def __fbind(self) -> None:
        self.fbind("align_ln", self.__compute_position)
        self.fbind("align_txt", self.__compute_position)
        self.fbind("animations", self.__compute_bool)
        self.fbind("auto_indent", self.__compute_bool)
        self.fbind("bg_ln", self.__compute_color)
        self.fbind("bg_txt", self.__compute_color)
        self.fbind("color_cursor", self.__compute_color)
        self.fbind("color_line_active", self.__compute_color)
        self.fbind("color_ln", self.__compute_color)
        self.fbind("color_scroll", self.__compute_color)
        self.fbind("color_scroll_inactive", self.__compute_color)
        self.fbind("color_selection", self.__compute_color)
        self.fbind("color_txt", self.__compute_color)
        self.fbind("cursor_blink", self.__compute_text)
        self.fbind("font_name", self.__compute_font)
        self.fbind("font_size", self.__compute_font)
        self.fbind("bg_info", self.__compute_color)
        self.fbind("color_info", self.__compute_color)
        self.fbind("margin_scroll", self.__compute_size)
        self.fbind("margin_scroll_cursor", self.__auto_scroll)
        self.fbind("padding_ln", self.__compute_padding)
        self.fbind("padding_txt", self.__compute_padding)
        self.fbind("pos_ln", self.__compute_position)
        self.fbind("pos_scroll_h", self.__compute_position)
        self.fbind("pos_scroll_v", self.__compute_position)
        self.fbind("spacing_content", self.__compute_spacing)
        self.fbind("spacing_line", self.__compute_spacing)
        self.fbind("readonly", self.__compute_text)
        self.fbind("RTL", self.__compute_RTL)
        self.fbind("width_cursor", self.__compute_text)
        self.fbind("width_ln", self.__compute_size)
        self.fbind("width_scroll", self.__compute_size)
        self.fbind("width_tab", self.__compute_text)

        # self.fbind("info_font_name", self.__compute_font)
        # self.fbind("info_font_size", self.__compute_font)
        # self.fbind("padding_info", self.__compute_padding)
        # self.fbind("spacing_info", self.__compute_spacing)

    def _on_resize(self, instance:Window, width:int, height:int) -> None:
        """When window is resizing, the text and line numbers need resizing to mach the ScrollView size.

        :param instance:    Who trigger this event.
        :param width:       The new window width.
        :param height:      The new window height.
        :return:            Nothing."""
        # We will do this next frame
        # If not, the scroll bar will show even the text is less than ScrollView size
        Clock.schedule_once(lambda _:self.__update_text_size())

    def _on_scroll_resize(self, instance:ScrollView, size:list[float]) -> None:
        """The purpose of it is to recalculate some stuffs on internal viewport changes.

        :param instance:    Who trigger this event.
        :param size:        List of width and height values.
        :return:            Nothing."""
        self.__update_hidden_size()
        self.__compute_scroll_bar_area()

    def __update_hidden_size(self) -> None:
        """Theo the name is saying, the purpose of it is to recalculate the hidden size of the text.

        :return: Nothing."""
        self.__hidden_height = self._Text.height - self.__Scroll_Text.height
        self.__hidden_width = self._Text.width - self.__Scroll_Text.width

    def __normalize_line_size(self) -> None:
        """Recalculate the line number size and normalize it in range [0, 1]"""
        try:
            self.__normalized_line_height = self._Text.line_height / self._Text.height
            self.__normalized_line_height_view = self._Text.line_height / self.__Scroll_Text.height
        except ZeroDivisionError: pass

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

    def __animate(self, target:any, index:str, r:bool=True, d:float=1.0, t="linear", **kwargs) -> None:
        """Animate things if allowed, otherwise just set **target** arguments.

        >>> # Example
        >>> self.__animate(widget, "widget_opacity", opacity=0)

        :param target:  Targeted widget.
        :param index:   Animation index.
        :param r:       Extra restriction.
        :param d:       Duration.
        :param t:       Transition.
        :param kwargs:  Key arguments to animate.
        :return:        Nothing."""
        if self.animations and r:
            if index in self.__animations_progress.keys():
                self.__animations_progress[index].stop(target)

            anim = Animation(**kwargs, duration=d, transition=t)

            self.__animations_progress[index] = anim
            anim.start(target)

        else:
            for key, arg in kwargs.items(): exec(f"target.{key} = {arg}")

    def _check_is_focus(self, instance:TextInput, value:bool) -> None:
        """Checking if the text area is focused/clicked.

        :param instance:    Who trigger this event.
        :param value:       If has focused.
        :return:            Nothing."""
        self.__focused = value

        # Base on text focus, make sure of some things
        if value:
            self.__animate(self.__Line_active, "line_active_opacity", d=0.2, opacity=1)

        else:
            self.__animate(self.__Line_active, "line_active_opacity", opacity=0)
            self._update_info(cursor=None)

    def _on_mouse_down(self, instance:Window, x:float, y:float, button:str, modifiers:list[str]) -> None:
        """Checking if some mouse key was pressed and base on that do some stuffs.

        :param instance:    Who trigger this event.
        :param x:           The horizontal mouse position.
        :param y:           The vertical mouse position.
        :param button:      Triggered button.
        :param modifiers:   Triggered special keys.
        :return:            Nothing."""
        # Flag the horizontal scroll on scroll up and the corresponding fake button of it
        if self.__shift and button == "scrollup":
            self.__scroll_horizontal["flag"] = True
            self.__scroll_horizontal["button"] = "scrollright"

        # Flag the horizontal scroll on scroll down and the corresponding fake button of it
        elif self.__shift and button == "scrolldown":
            self.__scroll_horizontal["flag"] = True
            self.__scroll_horizontal["button"] = "scrollleft"

        # Unflagging the horizontal scroll on next mouse button event if the above
        # conditions are not meet
        elif self.__scroll_horizontal["flag"]: self.__scroll_horizontal["flag"] = False

        # Checking only if the text input is focused/clicked
        if self.__focused:
            # Left Click: Flagging active line animation
            if button == "left": self.__animations_line_active = True

    def _on_mouse_up(self, instance:Window, x:float, y:float, button:str, modifiers:list[str]) -> None:
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
                # If some text was already selected and the cursor is somewhere in front of the selection
                if self.__selection_text_exist and self._Text.cursor_index() < self.__selection_text["from"]:
                    # Change the starting point of the selection
                    self.__selection_text["from"] = self._Text.cursor_index()

                # Otherwise, change just the end point of the selection
                else: self.__selection_text["to"] = self._Text.cursor_index()

                # Set text selection from minimum index value to the maximum one
                self._Text.select_text(min(self.__selection_text.values()), max(self.__selection_text.values()))

            # Left Click: Unflagging active line animation
            elif button == "left": self.__animations_line_active = False

    def _on_mouse_pos(self, instance:Window, position:tuple[float, float]) -> None:
        """Checking the mouse position and base on that do some stuffs.

        :param instance:    Who trigger this event.
        :param position:    The position of the mouse.
        :return:            Nothing."""
        if self.__Scroll_Text.collide_point(*position):
            scroll_area:bool = False

            if self.__area_scroll_v[0] < position[0] < self.__area_scroll_v[1]: scroll_area = True
            elif self.__area_scroll_h[0] < position[1] < self.__area_scroll_h[1]: scroll_area = True

            instance.set_system_cursor("hand" if scroll_area else "ibeam")

        elif self.__Scroll_LineNumber.collide_point(*position): instance.set_system_cursor("hand")

        else: instance.set_system_cursor("arrow")

        if self.__Info.collide_point(*position):
            if self.animations: Animation(opacity=1, d=0.25).start(self.__Layout_BG_hover_info)
            else: self.__Layout_BG_hover_info.opacity = 1

            for info in self.__infos.values():
                if info.collide_point(*position):
                    if self.animations:
                        self.__animate(self.__BG_hover_info, "bg_hover_info", t="in_out_elastic"
                                       , pos=info.pos, size=info.size)
                    else:
                        self.__BG_hover_info.pos = info.pos
                        self.__BG_hover_info.size = info.size

        else:
            if self.animations: Animation(opacity=0, d=0.25).start(self.__Layout_BG_hover_info)
            else: self.__Layout_BG_hover_info.opacity = 0

    def _on_cursor(self, instance:TextInput, position:tuple[int, int]) -> None:
        """The purpose of this function is to handle staffs witch are base on the cursor.

        :return: Nothing."""
        self.__animate(self.__Line_active, "line_active_move"
                       , d=0.5, t="in_out_elastic", r=self.__animations_line_active
                       , y=self._Text.cursor_pos[1] - self._Text.line_height)

        Clock.schedule_once(lambda _: self._update_info(cursor=True), .02)
        Clock.schedule_once(lambda _: self.__auto_scroll())

    def _update_info(self, cursor:bool|None=False, ln_sep:bool=False, encoding:bool=False,
                     tabs:bool=False, source:str="") -> None:
        """The purpose of it is to update the information's.

        :param cursor:      Cursor position.
        :param ln_sep:      Line separator used.
        :param encoding:    Encoding used.
        :param tabs:        Tabs width.
        :param source:      Source type.
        :return:            Nothing."""
        # Cursor -> row:col (n char(s), n line break(s))
        if cursor is None: self.__infos["cursor"].opacity = 0
        else:
            info = self.__infos["cursor"]
            info.text = f"{self._Text.cursor_row + 1}:{self._Text.cursor_col + 1}"

            if self._Text.selection_text:
                count_chars:str = ""
                count_ln_breaks:str = ""
                delimiter:str = " | "

                # Count line break and subtract 1 if last selected character is not a line breaker
                lines:int = len(self._Text.selection_text.splitlines()) - \
                            int(self._Text.selection_text[-1:] not in ["\r", "\n"])

                # Count selected characters
                chars:int = self._Text.selection_to - self._Text.selection_from
                # Keep characters amount positive
                if chars < 0: chars *= -1
                # Subtract line brakes amount
                if self.__info_count_only_visible_chars:
                    chars -= lines
                    delimiter = " & "

                # Show chars/lines if they are not 0 (zero)
                if chars: count_chars = f"{chars} char{'s' if chars > 1 else ''}"
                if lines: count_ln_breaks = f"{delimiter if chars else ''}{lines} line break{'s' if lines > 1 else ''}"
                info.text += f" ({count_chars}{count_ln_breaks})"

            info.texture_update()
            info.width = info.texture_size[0]
            info.opacity = 1

        # Line separator -> CR|LF|CRLF
        if ln_sep:
            info = self.__infos["ln_sep"]
            info.text = self.__file_ln_break.upper()
            info.texture_update()
            info.width = info.texture_size[0]

        # Encoding -> UTF-8|US-ASCII|binary...
        if encoding:
            info = self.__infos["encoding"]
            info.text = self.__file_encoding.upper()
            info.texture_update()
            info.width = info.texture_size[0]

        # Tab width -> n space(s)
        if tabs:
            info = self.__infos["tabs"]
            info.text = f"{self.width_tab} space{'s' if self.width_tab > 1 else ''}"
            info.texture_update()
            info.width = info.texture_size[0]

        # Source -> Text|Python|C++...
        if bool(source):
            info = self.__infos["source"]
            info.text = source.capitalize()
            info.texture_update()
            info.width = info.texture_size[0]

    def _on_key_down(self, instance:Window, keycode:int, _:int, text:str, modifiers:list[str]) -> None:
        """Checking if some keyboard key was pressed and base on that do some stuffs.

        :param instance:    Who trigger this event.
        :param keycode:     Triggered key code.
        :param text:        ASCII version of the keycode.
        :param modifiers:   Triggered special keys.
        :param _:           I do not know...
        :return:            Nothing."""
        if not self.__shift and "shift" in modifiers:
            # Flag shift if not flagged already
            self.__shift = True

            # SHIFT + LeftClick selection range
            # If some text was already selected, extract the selected range
            if self._Text.selection_text:
                self.__selection_text_exist = True
                self.__selection_text["from"] = self._Text.selection_from
                self.__selection_text["to"] = self._Text.selection_to

            # Otherwise, set the starting point of the selection with the current cursor position
            else:
                self.__selection_text_exist = False
                self.__selection_text["from"] = self._Text.cursor_index()

        # Checking only if the text input is focused/clicked
        if self.__focused:
            # Update text size if necessary
            if text is not None: self.__update_text_width_from_text(text)

            # Long press will trigger same logic multiple times
            # So we check if the flags was triggered already
            # before doing same flag trigger multiple times
            if not self.readonly: self._Text.readonly = "alt" in modifiers
            if not self.__ctrl and "ctrl" in modifiers: self.__ctrl = True

            # [Home, End, Page Up, Page Down]: Flagging auto scrolling animation
            if keycode in [278, 279, 280, 281]: self.__animations_auto_scroll = True

            # ALT + Numpad 8
            elif "alt" in modifiers and keycode == 264:
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
            elif keycode in [13, 271]: self.__LineNumber_Add(amount=1)

            # CTRL + V
            elif self.__ctrl and keycode == 118:
                self.__LineNumber_Add(Clipboard.paste())

                if not self.__unredo["undo"]: self.__unredo["undo"] = True

    def _on_key_up(self, instance:Window, keycode: int, _: int) -> None:
        """Checking if some keyboard keys was released and base on that do some stuffs.

        :param instance:    Who trigger this event.
        :param keycode:     Triggered key code.
        :param _:           I do not know...
        :return:            Nothing."""
        # Unflagging shift
        # [L_SHIFT, R_SHIFT]
        if keycode in [304, 303]: self.__shift = False

        # Checking only if the text input is focused/clicked
        elif self.__focused:
            # [Home, End, Page Up, Page Down]: Unflagging auto scrolling animation
            if keycode in [278, 279, 280, 281]: self.__animations_auto_scroll = False

            # [Backspace, Delete]
            elif keycode in [8, 127]:
                try:
                    # After a substring was deleted, we check the undo dummy to see
                    # if was some lines, and we subtract that amount of lines.
                    # Last undo item suppose to be of type backspace or delete, so
                    # we use the right pattern without checking it.
                    # TODO: Move it on key down to avoid long press mist.
                    #       Maybe there will need to use :mod:`~kivy.clock.Clock`
                    item: dict = self._Text._undo[-1]
                    substring: str = item["undo_command"][2]
                    self.__LineNumber_Unknown(substring)

                # If we got an int instead of str or an empty list, do nothing
                except TypeError: pass
                except IndexError: pass

            # CTRL + X
            elif self.__ctrl and keycode == 120:
                self.__LineNumber_Subtract(Clipboard.paste())

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
                        self.__LineNumber_Add(item["undo_command"][2])
                    # Otherwise, if the type is insert, subtract the line numbers from substring
                    elif _type == "insert":
                        self.__LineNumber_Subtract(item["redo_command"][1])

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
                        self.__LineNumber_Subtract(item["undo_command"][2])
                    # Otherwise, if the type is insert, add the line numbers from substring
                    elif _type == "insert":
                        self.__LineNumber_Add(item["redo_command"][1])

                    # Because redo dummy was empty before we started this check we
                    # set "redo" flag as False to know that was the last item of the list
                    if len(self._Text._redo) == 0: self.__unredo["redo"] = False

                # If we got an int instead of str or an empty list, do nothing
                except TypeError: pass
                except IndexError: pass

            # CTRL + G
            elif self.__ctrl and keycode == 103:
                # TODO: Ctrl+G
                WARNING("TODO: Move cursor to the specified position will be available on the next update.")

            # [L_CTRL, R_CTRL]
            elif keycode in [305, 306]: self.__ctrl = False

    def __LineNumber_Unknown(self, substring:str|None=None) -> None:
        """This is a helper to recalculate the line numbers.

        :param substring:   The text to process as string.
        :return:            Nothing."""
        reference:int = len(self._Text.lines)

        # If the reference is bigger than the (line number different from zero)
        if reference > self.__lines > 1:
            # Add just the difference
            self.__LineNumber_Add(substring, amount=reference - self.__lines)

        # If the reference is less than the line number
        elif reference < self.__lines:
            # Subtract just the difference
            self.__LineNumber_Subtract(substring, amount=self.__lines - reference)

        # Otherwise, write line numbers from scratch base on the reference.
        # Most of the time this will be call it when the line numbers and/or
        # the reference are less than 1 and will add that "1" line number.
        elif self.__lines != reference or self.__lines < 1:
            self._LineNumber.text = "1"

            for line in range(2, reference + 1):
                self._LineNumber.text += f"\n{line}"

            self.__lines = reference
            self.__auto_width_ln()
            Clock.schedule_once(lambda _:self.__auto_text_size())

            self.__normalize_line_size()

    def __LineNumber_Add(self, substring:str|None=None, amount:int=0) -> None:
        """Add the line numbers.

        :param substring:   The text to process as string.
        :param amount:      The amount of addition.
        :return:            Nothing."""
        try:
            t = ThreadLinesAdd(self.__lines, substring, amount)
            self._LineNumber.text += t.text
            self.__lines += t.lines

            self.__normalize_line_size()
        except ValueError: pass

        # Update the line number width to mach the correct new size
        self.__auto_width_ln()
        Clock.schedule_once(lambda _:self.__auto_text_size())

    def __LineNumber_Subtract(self, substring=None, amount: int=0) -> None:
        """Subtract the line numbers.

        :param substring:   The text to process as string.
        :param amount:      The amount of subtraction.
        :return: Nothing."""
        try:
            t = ThreadLinesSubstract(self._LineNumber.text, substring, amount)
            self._LineNumber.text = t.text
            self.__lines -= t.lines

            self.__normalize_line_size()
        except ValueError: pass

        # Update the line number width to mach the correct new size
        self.__auto_width_ln()
        Clock.schedule_once(lambda _: self.__auto_text_size())

    def __auto_RTL(self) -> None:
        """Auto detect if OS is RTL.

        :return: Nothing."""
        from kivy.core.text import Label

        bd = Label.find_base_direction("Auto find RTL")
        if bd is not None:
            self.RTL = "rtl" in bd
            self.__compute_RTL()

    def __auto_width_ln(self) -> None:
        """Set the maximum line number width need it to show up.
        If required more space will extrude, otherwise will use the provided line number width.

        :return: Nothing."""
        required:int = self.__width_ln_min * len(str(self.__lines)) + self.padding_ln[0] + self.padding_ln[1]
        size:int = max(self.width_ln, required)

        self.__Layout_ln.width = size

    def __auto_scroll(self, *noUse) -> None:
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
            self.__animate(self.__Scroll_Text, "scrolling_text_x", t="out_quint", r=self.__animations_auto_scroll
                           , scroll_x=clamp(self.__Scroll_Text.scroll_x - amount))

        elif normal_x > 1:
            amount:float = (self._Text.cursor_pos[0] - offset_x - self.__Scroll_Text.width +
                            self.width_cursor + self.margin_scroll_cursor[2])
            try: amount /= self.__hidden_width
            except ZeroDivisionError: pass
            self.__animate(self.__Scroll_Text, "scrolling_text_x", t="out_quint", r=self.__animations_auto_scroll
                           , scroll_x=clamp(self.__Scroll_Text.scroll_x + amount))

        if normal_y < self.__normalized_line_height_view:
            amount:float = (offset_y - self._Text.cursor_pos[1] + self._Text.line_height +
                            self.margin_scroll_cursor[3])
            try: amount /= self.__hidden_height
            except ZeroDivisionError: pass
            self.__animate(self.__Scroll_Text, "scrolling_text_y", t="out_cubic", r=self.__animations_auto_scroll
                           , scroll_y=clamp(self.__Scroll_Text.scroll_y - amount))

        elif normal_y > 1:
            amount:float = (self._Text.cursor_pos[1] - offset_y - self.__Scroll_Text.height +
                            self.margin_scroll_cursor[1])
            try: amount /= self.__hidden_height
            except ZeroDivisionError: pass
            self.__animate(self.__Scroll_Text, "scrolling_text_y", t="out_cubic", r=self.__animations_auto_scroll
                           , scroll_y=clamp(self.__Scroll_Text.scroll_y + amount))

    def __auto_text_size(self) -> None:
        """Find the optimal text size need it to show up.

        :return: Nothing."""
        # TODO: New logic to speed up the response time on bigger text
        self.__width_txt_min = FontMeasure(self.font_name, self.font_size).get_width_of(self.text)
        self.__update_text_size()

    def __update_text_size(self) -> None:
        """Like how the name is suggesting, the purpose of this logic is to update the text size.
        And the line numbers vertical size off course.

        :return: Nothing."""
        padding_horizontal:int = self.padding_txt[0] + self.padding_txt[2]

        self._Text.width = max(self.__Scroll_Text.width, self.__width_txt_min + padding_horizontal)
        self._Text.height = max(self.__Scroll_Text.height, self._Text.minimum_height)

        self._LineNumber.height = self._Text.height
        self.__Line_active.height = self._Text.line_height
        self.__Layout_txt.size = self._Text.size
        self.__update_hidden_size()

        self.__normalize_line_size()

    def __update_text_width_from_text(self, text:str) -> None:
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
            self.__Layout_txt.width = line_width
            self.__update_hidden_size()

    def __find_width_ln_min(self) -> None:
        """Find the minimum width need it to display one line number character.

        :return: Nothing."""
        measure = FontMeasure(self.font_name, self.font_size)

        self.__width_ln_min = max(measure.get_width_of(number) for number in NUMBERS)

    def __fix_font_changes_bug(self, cursor:tuple[int, int], scroll_x:float, scroll_y:float) -> None:
        """Fix the cursor and scroll changes when the font name and/or font size are changed.

        :param cursor:      Cursor position [ row, col ].
        :param scroll_x:    Horizontal scroll value.
        :param scroll_y:    Vertical scroll value.
        :return:            Nothing."""
        # To fix them we need to set them to a specific value
        # Like, before to change the font, we save these values and after will set them back.
        self._Text.cursor = cursor
        self.__Scroll_Text.scroll_x = scroll_x
        self.__Scroll_Text.scroll_y = scroll_y

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
        self.__LineNumber_Unknown()

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
        self.__LineNumber_Unknown()

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
        self.__LineNumber_Add(text)

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
        self.__LineNumber_Add(text)

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
                self.__auto_width_ln()
                self._Text.size = self.__Scroll_Text.size

                self.__normalize_line_size()

            # Otherwise, clear the specified range
            else:
                txtStart:str = "" if fStart else self._Text.text[:_from]
                txtEnd:str = "" if fEnd else self._Text.text[_to:]
                self._Text.text = txtStart + txtEnd
                self.__LineNumber_Unknown()

    def binding(self, **kwargs) -> None:
        """Useful for controlling text binding.

        The key arguments are the same as :class:`kivy.uix.textinput.TextInput` class ones because by calling this,
        in fact you are calling **:meth:`kivy.uix.textinput.TextInput.bind`** from inside this class.

        :return: Nothing."""
        self._Text.bind(**kwargs)

