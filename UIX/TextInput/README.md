<!-- https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md -->
# :warning: NOTE
>
> - Drag and drop files was removed, for now. Will be back under **TextEditor** class.

<br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ PREV ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->

# Preview
> Custom TextInput class with line numbers and other futures.
> 
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
> | :x: | Drag and drop files. Was removed, but will be on *`:class:`**`TextEditor.TextEditor`*** which will be available on short time, after I fixe some buggs on this *`:class:`**`TextInput.TextInput_LN`***. |
> | :heavy_check_mark: | Dynamic line number width. |
> | :heavy_check_mark: | Scroll bars with out loseing keyboard scrolling. |
> | :part_alternation_mark: | Multithreading. |
> | :heavy_check_mark: | Change system cursor if some actions are available on the current mouse position. |
> | :recycle: | Reduce line number updates. |
> | :heavy_check_mark: | Cursor and scroll jumps when the font is changed on run time. |
> 
> Legend [ :heavy_check_mark: Done | :x: Not (yet) | :part_alternation_mark: Partial | :recycle: Remaking ]

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ DOCS ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->

# 📚 Documentation
If you want to see a specific subject, click on one of listed ones.

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ LINK ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->
| Function | Short info |
| - | - |
| [initialization](#label-custom-textinput-class-with-line-numbers) | Custom TextInput class with line numbers. |
| [binding](#label-useful-for-controlling-text-binding) | Useful for controlling text bind. |
| [Theme](#label-change-the-style-dynamically) | Change the style dynamically. |
| [Clear](#label-deleting-text-in-the-specified-range) | Deleting text in the specified range. |
| [text](#label-provide-you-the-created-text) | Provide you the created text. |
| [SetText](#label-let-you-setting-a-new-text) | Let you setting a new text. |
| [AddText](#label-let-you-adding-text-after-the-existing-one) | Let you adding text after the existing one. |
| [InsertText](#label-let-you-adding-text-on-the-cursor-position) | Let you adding text on the cursor position. |
<!--
| [function](#tag) | info |
-->

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ CODE ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ TextInput_LN ]=-=[] -->
> #### :label: Custom TextInput class with line numbers.
> Links [ [:books: Doc](#-documentation) | [:arrow_down_small: Down](#label-useful-for-controlling-text-binding) ]
> ```python3
> TextInput.TextInput_LN(width_ln:int = 24, width_tab:int = 4, RTL:bool = False, auto_indent:bool = True
>                  , font_name:str = Font_Default, font_size:int = 18
>                  , width_scroll:int|float = 11, width_cursor:int|float = 2
>                  , margin_scroll:int|float = 0, margin_scroll_cursor:list|tuple = List(31.5, _type=float)
>                  , padding_ln:list|tuple = List(3), padding_txt:list|tuple = List(6), spacing:int = 0
>                  , align_ln:str = "right", align_txt:str = "left"
>                  , pos_scroll_h:str = "bottom", pos_scroll_v:str = "right"
>                  , color_ln:ColorProperty = "606366", color_txt:ColorProperty = "A9B7C6"
>                  , color_cursor:ColorProperty = "806F9F", color_selection:ColorProperty = "0066994D"
>                  , color_scroll:ColorProperty = "A6A6A680", color_scroll_inactive:ColorProperty = "A6A6A647"
>                  , bg_ln:ColorProperty = "313335", bg_txt:ColorProperty = "2B2B2B"
>                  , color_info:ColorProperty = "606366", bg_info:ColorProperty = "343638"
>                  , **kwargs)
> ```
> - This is a wrapper base on *`:class:`**`kivy.uix.textinput.TextInput`*** and still you are limited with some arguments which have slightly different names.
> 
> | Argument | Type | Default | Description |
> | - | - | - | - |
> | align_ln | `str` | "right" | Horizontal alignment of the line number. |
> | align_txt | `str` | "left" | Horizontal alignment of the text. |
> | auto_indent | `bool` | **True** | Automatically indent multiline text. |
> | bg_info | `str` <br /> `list` <br /> `tuple` | `#343638` | Background color, in RGBA format. |
> | bg_ln | `str` <br /> `list` <br /> `tuple` | `#313335` | Background color, in RGBA format. |
> | bg_txt | `str` <br /> `list` <br /> `tuple` | `#2B2B2B` | Background color, in RGBA format. |
> | color_cursor | `str` <br /> `list` <br /> `tuple` | `#806F9F` | Foreground color, in RGBA format. |
> | color_info | `str` <br /> `list` <br /> `tuple` | `#606366` | Foreground color, in RGBA format. |
> | color_ln | `str` <br /> `list` <br /> `tuple` | `#606366` | Foreground color, in RGBA format. |
> | color_scroll | `str` <br /> `list` <br /> `tuple` | `#A6A6A680` | Foreground color, in RGBA format. |
> | color_scroll_inactive | `str` <br /> `list` <br /> `tuple` | `#A6A6A647` | Foreground color, in RGBA format. |
> | color_selection | `str` <br /> `list` <br /> `tuple` | `#0066994D` | Foreground color, in RGBA format. |
> | color_txt | `str` <br /> `list` <br /> `tuple` | `#A9B7C6` | Foreground color, in RGBA format. |
> | font_name | `str` | `Roboto` | Filename of the font to use. <br /> If not provided, this value is taken from *`:class:`**`kivy.config.Config`***.|
> | font_size | `int` | 18 | Font size of the text in pixels. |
> | margin_scroll | `int` <br /> `float` | 0 | Margin between the scroll bar and the side of the scrollview. |
> | margin_scroll_cursor | `list` <br /> `tuple` | [31.5, 31.5, <br /> 31.5, 31.5] | Margin between the cursor and the side of the scrollview when auto scrolling is triggered. <br /> `[margin_left, margin_top, margin_right, margin_bottom]` |
> | padding_ln | `list` <br /> `tuple` | [3, 3, 3, 3] | Padding of the line number. <br /> `[padding_left, padding_top, padding_right, padding_bottom]` |
> | padding_txt | `list` <br /> `tuple` | [6, 6, 6, 6] | Padding of the text. <br /> `[padding_left, padding_top, padding_right, padding_bottom]` |
> | pos_scroll_h | `str` | "bottom" | Position of the horizontal scroll bar. <br /> **Options:** `"bottom"` and `"top"` |
> | pos_scroll_v | `str` | "right" | Position of the vertical scroll bar. <br /> **Options:** `"left"` and `"right"` |
> | RTL | `bool` | **False** | Right to left base direction of text. |
> | spacing | `int` | 0 | Space between the lines. |
> | width_ln | `int` | 24 | Width of the line number. |
> | width_cursor | `int` <br /> `float` | 2 | Width of the cursor. |
> | width_scroll | `int` <br /> `float` | 11 | Width of the scroll bar. |
> | width_tab | `int` | 4 | Amount of spaces used instead of tab character (`\t`). |
<!--
> | arg | `type` | def | info |
-->

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ binding ]=-=[] -->
> #### :label: Useful for controlling text binding.
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-custom-textinput-class-with-line-numbers) | [:arrow_down_small: Down](#label-change-the-style-dynamically) ]
> ```python3
> TextInput.TextInput_LN.binding(**kwargs)
> ```
>   - The key arguments are the same as *`:class:`**`kivy.uix.textinput.TextInput`*** ones because by calling this, in fact you are calling *`:meth:`**`kivy.uix.textinput.TextInput.bind`*** from inside this class.

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ Theme ]=-=[] -->
> #### :label: Change the style dynamically.
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-useful-for-controlling-text-binding) | [:arrow_down_small: Down](#label-deleting-text-in-the-specified-range) ]
> ```python3
> TextInput.TextInput_LN.Theme(crash:bool = True, **kwargs)
> ```
> | Argument | Type | Default | Description |
> | - | - | - | - |
> | crash | `bool` | **True** | Will log an error[^error] message and will crash the application in case the `kwargs` types is not one of listed ones. <br /> If `False` will log a warning[^warning] message instead. |
> | kwargs |  |  | The key arguments are the same as [*`:class:`**`TextInput.TextInput_LN`***](#label-custom-textinput-class-with-line-numbers). |
> 
> Some arguments are changed automatically.
> | Argument | Info |
> | - | - |
> | color_info | If not provided, will update base on `color_ln` with a slightly  difference of 10%. |
> | bg_info | If not provided, will update base on `bg_ln` with a slightly  difference of 5%. |
> | padding_ln <br /> padding_txt | Will auto sync vertically to avoid line number offset. <br /> **What I mean is:** On `padding_ln` just the horizontal padding values will be considered and the vertical ones will be taken fron `padding_txt`. |
> - :information_source: The `crash` value will ***not*** prevent the *`:api:`**`kivy`*** to crash if the argument type is a wrong one.
>   - This option is to prevent hard times on debug when you get an crash with a wrong value.
> - :warning: Will log a warning[^warning] message in case a specified argument is not defined.

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ Clear ]=-=[] -->
> #### :label: Deleting text in the specified range.
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-change-the-style-dynamically) | [:arrow_down_small: Down](#label-provide-you-the-created-text) ]
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
> #### :label: Provide you the created text.
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
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-provide-you-the-created-text) | [:arrow_down_small: Down](#label-let-you-adding-text-after-the-existing-one) ]
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
