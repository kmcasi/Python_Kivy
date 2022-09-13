<!-- https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md -->

# :placard: ToolTip
Custom tool tip class what will pop up base on the provided target.

<br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ DOCS ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->

# 📚 Documentation
If you want to see a specific subject, click on one of listed ones.

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ LINK ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->
| Function | Short info |
| - | - |
| [info](#label-information) | Some information what you need to be aware of. |
| [initialization](#label-initialization-tooltip-class) | Initialization of this custom tool tip class. |
<!--
| [function](#tag) | info |
-->

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ CODE ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ OverlayLayout ]=-=[] -->
> #### :label: Information.
> Links [ [:books: Doc](#-documentation) | [:arrow_down_small: Down](#label-initialization-tooltip-class) ]
> - The tool tip position will be constrained and will not leave the main window.
> - You can **NOT** use two horizontal or vertical combinations like: *["top", "bottom"]* or *["left", "right"]*.
> - If the "animations" is True, the opacity attribute can not be changed after initialization because this value is used on the fade-in and fade-out animation.

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ OverlayLayout ]=-=[] -->
> #### :label: Initialization ToolTip class.
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-information) ]
> ```python3
> ToolTip.ToolTip(**kwargs)
> ```
> | Argument | Type | Default | Description |
> | - | - | - | - |
> | animations | `BooleanProperty` | **`True`** | Use animations. |
> | padding | `VariableListProperty` | `[3]` | Padding between the background and message. <br /> `[padding_left, padding_top, padding_right, padding_bottom]` |
> | border | `NumericProperty` | `2dp` | Border size, in pixels. |
> | text_color | `ColorProperty` | `#646464` | Text color, in RGBA format. |
> | background_color | `ColorProperty` | `#262626` | Background color, in RGBA format. |
> | border_color | `ColorProperty` | `#606366` | Border color, in RGBA format. |
> | font_name | `StringProperty` | `Roboto` | Filename of the font to use. <br /> If not provided, this value is taken from *`:class:`**`kivy.config.Config`***. |
> | font_size | `NumericProperty` | `16sp` | Font size of the text and the line numbers in pixels. |
> | position | `OptionProperty` | `["cursor"]` | Sets the position of the tooltip base on the target position. <br /> **Options:** <br /> `["cursor"]`, `["top"]`, `["bottom"]`, `["left"]`, `["right"]` and combinations of two of them like `["cursor", "top"]`. |
> | text | `StringProperty` | `"ToolTip message"` | Text of the tooltip. |
> | opacity | `NumericProperty` | `1.0` | Opacity of the tooltip. |
<!--
> | arg | `type` | def | info |
-->
