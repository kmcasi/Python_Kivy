<!-- https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md -->

# :memo: TextInput_LN documentation
Custom TextInput class with line numbers, scroll bars and more other futures fully customizable.

<br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ PREV ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->

# 👀 Preview
> ![Preview TextInputCustom](https://github.com/kmcasi/Python_Kivy/blob/main/PREVIEW/UIX/TextInputCustom.png)
> 
> Extra control functions than what allready *`:class:`**`kivy.uix.textinput.TextInput`*** have.
> | :hammer_and_wrench: | Control | Description |
> | - | - | - |
> | :heavy_check_mark: | ![shift](https://github.com/kmcasi/Python_Kivy/blob/main/doc/key_bind/shift.png)![left_click](https://github.com/kmcasi/Python_Kivy/blob/main/doc/key_bind/left-click.png) | Set selection range. |
> | :heavy_check_mark: | ![shift](https://github.com/kmcasi/Python_Kivy/blob/main/doc/key_bind/shift.png)![scroll](https://github.com/kmcasi/Python_Kivy/blob/main/doc/key_bind/scroll.png) | Scroll horizontally. |
> | :heavy_check_mark: | ![ctrl](https://github.com/kmcasi/Python_Kivy/blob/main/doc/key_bind/alt.png)![arrows](https://github.com/kmcasi/Python_Kivy/blob/main/doc/key_bind/numpad.png) | Scrolling from keyboard (numpad). |
> 
> | :hammer_and_wrench: | Other futures |
> | - | - |
> | :x: | Drag and drop files. <br /> Was removed, but will be on *`:class:`**`TextEditor.TextEditor`*** which will be available on short time, after I fixe some buggs on this *`:class:`**`TextInput.TextInput_LN`***. |
> | :heavy_check_mark: | Dynamic line number width. |
> | :heavy_check_mark: | Scroll bars with out loseing keyboard scrolling. |
> | :part_alternation_mark: | Multithreading. |
> | :heavy_check_mark: | Change system cursor if some actions are available on the current mouse position. |
> | :recycle: | Reduce line number updates. |
> | :heavy_check_mark: | Cursor and scroll jumps when the font is changed on run time. |
> | :x: | Wrapping text like on *`:attr:`**`kivy.uix.textinput.TextInput.do_wrap`***. |
> 
> Legend [ :heavy_check_mark: Done | :x: Not (yet) | :part_alternation_mark: Partial | :recycle: Remaking ]

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ DOCS ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->

# 📚 Documentation
If you want to see a specific subject, click on one of listed ones.

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ LINK ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->
| Function | Short info |
| - | - |
| [initialization](#label-initialization-textinput-class) | Initialization of this custom TextInput class. |
| [binding](#label-useful-for-controlling-text-binding) | Useful for controlling text bind. |
| [Clear](#label-deleting-text-in-the-specified-range) | Deleting text in the specified range. |
| [text](#label-provide-you-the-existing-text) | Provide you the existing text. |
| [SetText](#label-let-you-setting-a-new-text) | Let you setting a new text. |
| [AddText](#label-let-you-adding-text-after-the-existing-one) | Let you adding text after the existing one. |
| [InsertText](#label-let-you-adding-text-on-the-cursor-position) | Let you adding text on the cursor position. |
<!--
| [function](#tag) | info |
-->

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ CODE ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ TextInput_LN ]=-=[] -->
> #### :label: Initialization TextInput class.
> Links [ [:books: Doc](#-documentation) | [:arrow_down_small: Down](#label-useful-for-controlling-text-binding) ]
> ```python3
> TextInput.TextInput_LN(**kwargs)
> ```
> - This is a wrapper base on *`:class:`**`kivy.uix.textinput.TextInput`*** and still you are limited with some arguments which have slightly different names.
> 
> | Argument | Type | Default | Description |
> | - | - | - | - |
> | align_ln | `OptionProperty` | `auto` | Horizontal alignment of the line numbers. <br /> **Options:** `"auto"`, `"left"`, `"center"` and `"right"` |
> | align_txt | `OptionProperty` | `auto` | Horizontal alignment of the text. <br /> **Options:** `"auto"`, `"left"`, `"center"` and `"right"` |
> | animations | `BooleanProperty` | **`True`** | Use animations. |
> | auto_indent | `BooleanProperty` | **`True`** | Automatically indent new text line. |
> | bg_ln | `ColorProperty` | `#313335` | Background color of the line numbers, in RGBA format. |
> | bg_txt | `ColorProperty` | `#2B2B2B` | Background color of the text, in RGBA format. |
> | color_cursor | `ColorProperty` | `#806F9F` | Color of the cursor, in RGBA format. |
> | color_line_active | `ColorProperty` | `#3F3F3F80` | Color of the active line, in RGBA format. |
> | color_ln | `ColorProperty` | `#606366` | Color of the line numbers, in RGBA format. |
> | color_scroll | `ColorProperty` | `#A6A6A680` | Color of the active scroll bars, in RGBA format. |
> | color_scroll_inactive | `ColorProperty` | `#A6A6A647` | Color of the inactive scroll bars, in RGBA format. |
> | color_selection | `ColorProperty` | `#0066994D` | Color of the selection, in RGBA format. |
> | color_txt | `ColorProperty` | `#A9B7C6` | Color of the text, in RGBA format. |
> | cursor_blink | `BooleanProperty` | **`True`** | Whether the graphic cursor should blink or not. |
> | font_name | `StringProperty` | `Roboto` | Filename of the font to use. <br /> If not provided, this value is taken from *`:class:`**`kivy.config.Config`***. |
> | font_size | `NumericProperty` | `18sp` | Font size of the text and the line numbers in pixels. |
> | margin_scroll | `NumericProperty` | `0` | Margin between the scroll bars and the margins of the text. |
> | margin_scroll_cursor | `VariableListProperty` | `[31.5]` | Padding between the cursor and the text area. <br />When the cursor is out side of this limits the text will auto scrolling to keep the cursor inside the visible area. <br /> `[margin_left, margin_top, margin_right, margin_bottom]` |
> | padding_ln | `VariableListProperty` | `[3]` | Horizontal padding of the line numbers. <br /> `[padding_left, padding_right]` |
> | padding_txt | `VariableListProperty` | `[6]` | Padding of the text. <br /> `[padding_left, padding_top, padding_right, padding_bottom]` |
> | pos_ln | `OptionProperty` | `auto` | Position of the line numbers. <br /> **Options:** `"auto"`, `"left"` and `"right"` |
> | pos_scroll_h | `OptionProperty` | `bottom` | Position of the horizontal scroll bar. <br /> **Options:** `"top"` and `"bottom"` |
> | pos_scroll_v | `OptionProperty` | `right` | Position of the vertical scroll bar. <br /> **Options:** `"left"` and `"right"` |
> | pos_scroll | `ReferenceListProperty` | `bottom`, `right` | Position of the scroll bars. <br /> `pos_scroll_h, pos_scroll_v` |
> | readonly | `BooleanProperty` | **`False`** | If True, the user will not be able to change the content of a textinput. |
> | RTL | `BooleanProperty` | **`False`** | Use right to left as base direction of the text, this impacts horizontal alignment and the line numbers position when :attr:`align_txt`, :attr:`align_ln` and :attr:`pos_ln` are `auto` (the default). |
> | spacing_content | `NumericProperty` | `0` | Space taken up between the content. |
> | spacing_line | `NumericProperty` | `0` | Space taken up between the lines. |
> | width_cursor | `NumericProperty` | `2dp` | Thickness of the cursor. |
> | width_ln | `NumericProperty` | `24dp` | Minimum width of the line numbers. |
> | width_tab | `NumericProperty` | `4` | Amount of spaces used instead of tab character (`\t`). |
> | width_scroll | `NumericProperty` | `11dp` | Thickness of the scroll bars. |
<!--
> | arg | `type` | def | info |
-->

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ binding ]=-=[] -->
> #### :label: Useful for controlling text binding.
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-initialization-textinput-class) | [:arrow_down_small: Down](#label-deleting-text-in-the-specified-range) ]
> ```python3
> TextInput.TextInput_LN.binding(**kwargs)
> ```
>   - The key arguments are the same as *`:class:`**`kivy.uix.textinput.TextInput`*** ones because by calling this, in fact you are calling *`:meth:`**`kivy.uix.textinput.TextInput.bind`*** from inside this class.

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ Clear ]=-=[] -->
> #### :label: Deleting text in the specified range.
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-useful-for-controlling-text-binding) | [:arrow_down_small: Down](#label-provide-you-the-existing-text) ]
> ```python3
> TextInput.TextInput_LN.Clear(_from:int = 0, _to:int = -1)
> ```
> | Argument | Type | Default | Description |
> | - | - | - | - |
> | _from | `int` | 0 | The starting range. |
> | _to | `int` | -1 | The ending range. |
> - :information_source: In case `_from` is bigger than `_to` the function will invert them.
> - :warning: Will log a warning[^warning] message in case `_from` is equal with `_to`.

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ text ]=-=[] -->
> #### :label: Provide you the existing text.
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-deleting-text-in-the-specified-range) | [:arrow_down_small: Down](#label-let-you-setting-a-new-text) ]
> ```python3
> TextInput.TextInput_LN.text
> ```
> Under the hood is a property function which provide you a shorter way of getting, changing and deleting the text itself.
> 
> As an example, we create the text input as below:
> ```python3
> myText = TextInput_LN()
> ```
> We can get the text from the text input like on *`:class:`**`kivy.uix.textinput.TextInput`***.
> ```python3
> txt = myText.text
> print(txt)
> ```
> We can set text value like on *`:class:`**`kivy.uix.textinput.TextInput`***, but also we can set and none string values.
> ```python3
> # None string type will be converted to string
> # like when you `print(True)`
> myText.text = True
> 
> # But we can use JUST string to extend the text 
> myText.text += " text here..."
> ```
> Also you can delete the text and on unusully way useing `del`.
> ```python3
> # All of them will clear the text
> del myText.text
> myText.text = ""
> myText.Clear()
> ```

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ SetText ]=-=[] -->
> #### :label: Let you setting a new text.
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-provide-you-the-existing-text) | [:arrow_down_small: Down](#label-let-you-adding-text-after-the-existing-one) ]
> ```python3
> TextInput.TextInput_LN.SetText(*values:any, sep:str|None = " ", end:str|None = "\n")
> ```
> | Argument | Type | Default | Description |
> | - | - | - | - |
> | values | `any` |  | Values to be added as text. |
> | sep | `str` | " " | String inserted between values. |
> | end | `str` | "\n" | String appended after the last value. |

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ AddText ]=-=[] -->
> #### :label: Let you adding text after the existing one.
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-let-you-setting-a-new-text) | [:arrow_down_small: Down](#label-let-you-adding-text-on-the-cursor-position) ]
> ```python3
> TextInput.TextInput_LN.AddText(*values:any, sep:str|None = " ", end:str|None = "\n")
> ```
> - Arguments are the same as [*`:class:`**`TextInput.TextInput_LN.SetText`***](#label-let-you-setting-a-new-text).

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ InsertText ]=-=[] -->
> #### :label: Let you adding text on the cursor position.
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-let-you-adding-text-after-the-existing-one) ]
> ```python3
> TextInput.TextInput_LN.InsertText(*values:any, sep:str|None = " ", end:str|None = "\n")
> ```
> - Arguments are the same as [*`:class:`**`TextInput.TextInput_LN.SetText`***](#label-let-you-setting-a-new-text).

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ FOOT ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->
[^error]: Error will print a message on console and will crash the app immediately.
[^warning]: Warning will print a message on console and will ignore it.
