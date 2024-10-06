<!-- https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md -->

# :bookmark_tabs: LineNumber
Custom line number class what will count the lines for the provided TextInput.

<br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ DOCS ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->

# 📚 Documentation
If you want to see a specific subject, click on one of listed ones.

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ LINK ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->
| Function | Short info |
| - | - |
| [info](#label-information) | Some information what you need to be aware of. |
| [example](#label-example-of-usage) | Example of usage. |
| [initialization](#label-initialization-linenumber-class) | Initialization of this custom line number class. |
<!--
| [function](#tag) | info |
-->

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ CODE ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ INFO ]=-=[] -->
> #### :label: Information.
> Links [ [:books: Doc](#-documentation) | [:arrow_down_small: Down](#label-example-of-usage) ]
> - The LineNumber need to be pack out side of the ScrollView, if is used.
> - The vertical position and the size of this class is automaitcally calculated.
> - Is updateing base on provided TextInput. No matter if ScrollView is used or not.

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ EXAMPLE ]=-=[] -->
> #### :label: Example of usage.
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-information) | [:arrow_down_small: Down](#label-initialization-linenumber-class) ]
> ```python3
> #//|>-----------------------------------------------------------------------------------------------------------------<|
> #//| Copyright (c) 01 Sep 2024. All rights are reserved by ASI
> #//|>-----------------------------------------------------------------------------------------------------------------<|
> 
> #// IMPORT
> from kivy.app import App
> from kivy.clock import Clock
> from kivy.config import Config
> from kivy.core.window import Window
> from kivy.uix.gridlayout import GridLayout
> from kivy.uix.textinput import TextInput
> from kivy.uix.codeinput import CodeInput
> from kivy.uix.scrollview import ScrollView
> 
> from lib.LineNumber import LineNumber
> 
> 
> #// LOGIC
> class TextEditor(App):
>     def __init__(self, **kwargs):
>         super(TextEditor, self).__init__(**kwargs)
>         # Remove touch simulation
>         Config.set("input", "mouse", "mouse,multitouch_on_demand")
> 
>         self.grid_layout = GridLayout(cols=2)
>         # CodeInput is subclass of TextInput.
>         self.text_input = CodeInput(multiline=True, do_wrap=True, size_hint=(None, None), font_name="comic")
>         self.line_number = LineNumber(self.text_input, font_name="comic", font_size="12sp")
>         self.scroll_view = ScrollView(always_overscroll=False, scroll_type=["bars"], bar_width='11dp',
>                                       size_hint_x=None, width=750)
> 
>         self.text_input.bind(text=self._update_text_height)
>         Window.bind(size=self._update_size)
> 
>     def build(self):
>         self.scroll_view.add_widget(self.text_input)
> 
>         self.grid_layout.add_widget(self.line_number)
>         self.grid_layout.add_widget(self.scroll_view)
> 
>         return self.grid_layout
> 
>     def on_start(self):
>         sturtup_text:str = ""
> 
>         with open(__file__) as file:
>             sturtup_text = file.read()
> 
>         Clock.schedule_once(lambda _:self._set_startup_text(sturtup_text), 3)
> 
>     def _update_text_height(self, parent:TextInput, *_) -> None:
>         height = len(parent._lines_rects) * parent.line_height
>         height += parent.padding[1] + parent.padding[3]
> 
>         parent.height = max(height, self.scroll_view.height)
>         parent.width = self.scroll_view.width
> 
>     def _update_size(self, parent:Window, size:tuple[int, int]) -> None:
>         self.text_input.width = self.scroll_view.width = size[0] - self.line_number.width
>         self.scroll_view.height = size[1]
> 
>     def _set_startup_text(self, text:str) -> None:
>         self.text_input.text = text
> 
> 
> #// RUN
> if __name__ == '__main__':
>     TextEditor().run()
> 
> ```

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ INIT ]=-=[] -->
> #### :label: Initialization LineNumber class.
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-example-of-usage) ]
> ```python3
> LineNumber.LineNumber(**kwargs)
> ```
> | Argument | Type | Default | Description |
> | - | - | - | - |
> | text_input | `TextInput` | **Must be provided** |Need to be provided, to be able to sync. |
> | align | `OptionProperty` | `["right"]` | Horizontal alignment of the text. <br /> **Options:** <br /> `["left", "center", "right"]` |
> | background_color | `ColorProperty` | `#FFFFFF` | Background color, in RGBA format. |
> | background_texture | `StringProperty` | `atlas://.../textinput` | Background image of the line numbers. <br /> `atlas://data/images/defaulttheme/textinput` |
> | border | `ListProperty` | `[4,4,4,4]` | Border size, in pixels. Used with :attr:`background_texture`. |
> | font_context | `StringProperty` | `None` | *None* means the font is resolved by *`:attr:`**`font_name`***. |
> | font_family | `StringProperty` | `None` | Tthis is only applicable when using *`:attr:`**`font_context`*** option. |
> | font_name | `StringProperty` | `Roboto` | Filename of the font to use. <br /> If not provided, this value is taken from *`:class:`**`kivy.config.Config`***. |
> | font_size | `NumericProperty` | `15sp` | Font size of the text and the line numbers in pixels. |
> | foreground_color | `ColorProperty` | `#000000` | Text color, in RGBA format. |
> | padding | `VariableListProperty` | `[4, 4]` | Horizontal padding of the text. <br /> `[padding_left, padding_right]` |
> | width_min | `NumericProperty` | `18sp` | Minimum desired width of the text in pixels. |
<!--
> | arg | `type` | def | info |
-->
