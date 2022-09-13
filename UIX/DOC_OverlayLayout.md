<!-- https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md -->

# :brown_square: OverlayLayout
Custom layout class what will stack all widgets on top of each other.

<br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ DOCS ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->

# 📚 Documentation
If you want to see a specific subject, click on one of listed ones.

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ LINK ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->
| Function | Short info |
| - | - |
| [info](#label-information) | Some information what you need to be aware of. |
| [initialization](#label-initialization-overlaylayout-class) | Initialization of this custom overlay class. |
<!--
| [function](#tag) | info |
-->

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ CODE ]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[] -->

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ OverlayLayout ]=-=[] -->
> #### :label: Information.
> Links [ [:books: Doc](#-documentation) | [:arrow_down_small: Down](#label-initialization-overlaylayout-class) ]
> - All added widgets will be placed on center of the layout.
> - If added widgets have `size_hint` defined with one or both value as `None`, then the overlay size the biggest size.

<br /><br />

<!-- []=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[ OverlayLayout ]=-=[] -->
> #### :label: Initialization OverlayLayout class.
> Links [ [:books: Doc](#-documentation) | [:arrow_up_small: Up](#label-information) ]
> ```python3
> OverlayLayout.OverlayLayout(**kwargs)
> ```
> | Argument | Type | Default | Description |
> | - | - | - | - |
> | x | `NumericProperty` | `0` | Horizontal position of the overlay layout. |
> | y | `NumericProperty` | `0` | Vertical position of the overlay layout. |
> | pos | `ReferenceListProperty` | `0`, `0` | Position of the overlay layout. <br /> `x, y`|
> | width | `NumericProperty` | `100` | Width of the overlay layout. |
> | height | `NumericProperty` | `100` | Height of the overlay layout. |
> | size | `ReferenceListProperty` | `100`, `100` | Size of the overlay layout. <br /> `width, height`|
> | padding | `VariableListProperty` | `[0]` | Padding between layout margins and children(s). <br /> `[padding_left, padding_top, padding_right, padding_bottom]` |
<!--
> | arg | `type` | def | info |
-->
