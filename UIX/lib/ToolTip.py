#// IMPORT
from logging import error as ERROR
from sys import exit as CRASH

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.core.text import DEFAULT_FONT
from kivy.properties import OptionProperty, VariableListProperty
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ColorProperty

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.label import Label

from lib.helper.utils import clamp


#// GLOBAL VARIABLES
Font_Default:str = Config.getdefault("kivy", "default_font", None).split("'", 2)[1]


#// LOGIC
class ToolTip(Widget):
    animations = BooleanProperty(True)
    '''Use animations.

    :attr:`animations` is a :class:`~kivy.properties.BooleanProperty` and defaults to True.
    '''

    padding = VariableListProperty([3])
    '''Padding between the background and message.
    
    Padding can be provided in multiple ways:
        [1] \u279c [padding_left, padding_top, padding_right, padding_bottom]
        
        [2] \u279c [padding_horizontal, padding_vertical]
        
        [3] \u279c [padding]

    :attr:`padding` is a :class:`~kivy.properties.VariableListProperty` and defaults to [3, 3, 3, 3].
    '''

    border = NumericProperty(2)
    '''Border size, in pixels.

    :attr:`border` is a :class:`~kivy.properties.NumericProperty` and defaults to 2.
    '''

    text_color = ColorProperty("646464")
    '''Text color, in the format RGBA.
    
    This attribute can be used to set the text color.
    
    :attr:`text_color` is a :class:`~kivy.properties.ColorProperty` and defaults to "#646464FF".
    '''

    background_color = ColorProperty("262626")
    '''Background color, in the format RGBA.
    
    :attr:`background_color` is a :class:`~kivy.properties.ColorProperty` and defaults to "#262626FF".
    '''

    border_color = ColorProperty("606366")
    '''Border color, in the format RGBA.
    
    :attr:`border_color` is a :class:`~kivy.properties.ColorProperty` and defaults to "#606366FF".
    '''

    font_name = StringProperty(DEFAULT_FONT)
    '''Filename of the font to use. The path can be absolute or relative.
    
    Relative paths are resolved by the :func:`~kivy.resources.resource_find` function.

    :attr:`font_name` is a :class:`~kivy.properties.StringProperty` and
    defaults to 'Roboto'. This value is taken from :class:`~kivy.config.Config`.
    '''

    font_size = NumericProperty("16sp")
    '''Font size of the text in pixels.

    :attr:`font_size` is a :class:`~kivy.properties.NumericProperty` and
    defaults to 16 :attr:`~kivy.metrics.sp`.
    '''

    position = OptionProperty(["cursor"], options=[["cursor"], ["top"], ["bottom"], ["left"], ["right"],
                                                   ["cursor", "top"], ["cursor", "bottom"],
                                                   ["top", "cursor"], ["bottom", "cursor"],

                                                   ["cursor", "left"], ["cursor", "right"],
                                                   ["left", "cursor"], ["right", "cursor"],

                                                   ["top", "left"], ["top", "right"],
                                                   ["left", "top"], ["right", "top"],

                                                   ["bottom", "left"], ["bottom", "right"],
                                                   ["left", "bottom"], ["right", "bottom"]])
    '''Sets the position of the tooltip base on the target position.
    
    Available options are: **["cursor"], ["top"], ["bottom"], ["left"], ["right"]** or combinations of two of them.
    
    You can **NOT** use two horizontal or vertical combinations like: *["top", "bottom"]* or *["left", "right"]*.
    
    **NOTE:** If vertical or horizontal position is not specified, the target position will be used instead.

    +---------------------+------------------------------------------------+
    | ["cursor"]          | Content is positioned on the cursor position.  |
    +---------------------+                                                |
    |                     | Can be combined with others.                   |
    +---------------------+------------------------------------------------+
    | ["top"]             | Content is positioned on top of the target.    |
    +---------------------+                                                |
    |                     | Can **NOT** be combined with "bottom".         |
    +---------------------+------------------------------------------------+
    | ["bottom"]          | Content is positioned under the target.        |
    +---------------------+                                                |
    |                     | Can **NOT** be combined with "top".            |
    +---------------------+------------------------------------------------+
    | ["left"]            | Content is positioned on left side.            |
    +---------------------+                                                |
    |                     | Can **NOT** be combined with "right".          |
    +---------------------+------------------------------------------------+
    | ["right"]           | Content is positioned on right side.           |
    +---------------------+                                                |
    |                     | Can **NOT** be combined with "left".           |
    +---------------------+------------------------------------------------+

    :attr:`position` is an :class:`~kivy.properties.OptionProperty` and
    defaults to ["cursor"].
    '''

    text = StringProperty("ToolTip message")
    '''Text of the tooltip.
    
    You can change the style of the text using tags.
    Check the :doc:`api-kivy.core.text.markup` documentation for more information.

    :attr:`text` is a :class:`~kivy.properties.StringProperty` and defaults to "ToolTip message".
    '''

    opacity = NumericProperty(1.0)
    '''Opacity of the tooltip.
    
    If the "animations" is True, the opacity attribute can not be changed after initialization 
    because this value is used on the fade-in and fade-out animation.
    
    >>> # Setting opacity for the initialization stage
    >>> self.tt = ToolTip(your_target_widget, opacity=0.75)
    
    >>> # This will be used just if the "animations" is False
    >>> self.tt.opacity = 0.5

    :attr:`opacity` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 1.0.
    '''

    def __init__(self, target:Widget, **kwargs) -> None:
        super(ToolTip, self).__init__(**kwargs)
        self.fbind("padding", self.__compute_size)
        self.fbind("border", self.__compute_size)
        self.fbind("text_color", self.__compute_color)
        self.fbind("background_color", self.__compute_color)
        self.fbind("border_color", self.__compute_color)
        self.fbind("font_name", self.__compute_message)
        self.fbind("font_size", self.__compute_message)
        self.fbind("text", self.__compute_message)

        # Private variables
        self.__target:Widget = target
        self.__area:list[int, int] = [0, 0]
        self.__opacity:float = self.opacity
        self.__animation_move = None
        self.__animation_d:float = 0.5
        self.__animation_t:str = "out_cubic"
        self.__animation = Animation(opacity=self.__opacity, d=self.__animation_d, t=self.__animation_t)

        # UIX elements
        self.__layout = RelativeLayout()
        self.__border = Image(color=self.border_color, allow_stretch=True, keep_ratio=False)
        self.__background = Image(color=self.background_color, allow_stretch=True, keep_ratio=False)
        self.__label = Label(text=self.text, color=self.text_color, markup=True
                             , font_name=self.font_name, font_size=self.font_size)

        # Settings
        self.size_hint = (None, None)
        self.__border.size_hint = self.size_hint
        self.__background.size_hint = self.size_hint
        self.__label.size_hint = self.size_hint
        self.__compute_message()

        # Layout
        self.add_widget(self.__layout)
        self.__layout.add_widget(self.__border)
        self.__layout.add_widget(self.__background)
        self.__layout.add_widget(self.__label)

        # Binds
        Window.bind(mouse_pos=self._on_mouse_pos, on_cursor_leave=self._close
                    , on_resize=lambda i,w,h:self.__compute_area())

    def add_widget(self, widget:Widget, index:int=0, canvas:str|None=None):
        """Restrict widgets to be added.

        :return:    Nothing."""
        # Allow just one child, which is added by initializer.
        if not self.children:
            return super(ToolTip, self).add_widget(widget, index, canvas)

        # Otherwise, do not allow extra widgets.
        else:
            ERROR("ToolTip: You do not have permissions to add child's.")
            CRASH()

    def remove_widget(self, widget:Widget) -> None:
        """Restrict widgets to be removed.

        :return:    Nothing."""
        ERROR("ToolTip: You do not have permissions to remove child's.")
        CRASH()

    def on_pos(self, instance:Widget, position:tuple[float, float]) -> None:
        """Update the layout position to the parent position.

        :param instance:    Who trigger this event.
        :param position:    The position of the tooltip.
        :return:            Nothing."""
        self.__layout.pos = position

    def _on_mouse_pos(self, instance:Window, position:tuple[float, float]) -> None:
        """Checking the mouse position and base on that do some stuffs.

        :param instance:    Who trigger this event.
        :param position:    The position of the mouse.
        :return:            Nothing."""
        self._close()

        if self.__target.collide_point(*position):
            Clock.schedule_once(self._show, 1)

    def _show(self, *noUse) -> None:
        """Showing the tooltip.

        :param noUse:   Allow arguments to be provided, but are not need of them.
        :return:        Nothing."""
        self.__compute_size()
        self.__compute_pos()
        Window.add_widget(self)

        if self.animations:
            self.__animation.start(self)
            self.__animation_move.start(self)

        else:
            if self.opacity == 0:
                self.opacity = self.__opacity

    def _close(self, *noUse) -> None:
        """Closing the tooltip.

        :param noUse:   Allow arguments to be provided, but are not need of them.
        :return:        Nothing."""
        Clock.unschedule(self._show)

        if self.animations:
            Animation(opacity=0, t=self.__animation_t, d=self.__animation_d / 2).start(self)
            Clock.schedule_once(lambda _:Window.remove_widget(self), self.__animation_d / 2)

        else: Window.remove_widget(self)

    def __compute_pos(self) -> None:
        """Compute the tooltip position base on preferred position.

        :return: Nothing."""
        self.pos = Window.mouse_pos if "cursor" in self.position else self.__target.pos
        self_x, self_y = self.pos

        if "top" in self.position:
            self_y = self.__target.top

        elif "bottom" in self.position:
            self_y = self.__target.y - self.height

        if "left" in self.position:
            self_x = self.__target.x - self.width

        elif "right" in self.position:
            self_x = self.__target.right

        pos_to = [clamp(self_x, _max=self.__area[0]), clamp(self_y, _max=self.__area[1])]

        if self.animations:
            self.__animation_move = Animation(pos=pos_to, d=self.__animation_d, t=self.__animation_t)
        else:
            self.pos = pos_to

    def __compute_layout(self) -> None:
        """Compute the tooltip layout base on provided padding and border.

        :return: Nothing."""
        self.__background.pos = (self.border, self.border)
        self.__label.pos = (self.border + self.padding[0], self.border + self.padding[3])

    def __compute_size(self, *noUse) -> None:
        """Compute the tooltip size base on provided padding, border and message size.

        :param noUse:   Allow arguments to be provided, but are not need of them.
        :return:        Nothing."""
        width = self.padding[0] + self.padding[2] + self.__label.width
        height = self.padding[1] + self.padding[3] + self.__label.height

        self.size = (self.border * 2 + width, self.border * 2 + height)
        self.__border.size = self.size
        self.__background.size = (width, height)

        self.__compute_area()
        self.__compute_layout()

    def __compute_message(self, *noUse) -> None:
        """Compute the tooltip message size base on provided font_name, font_size and the message itself.

        :param noUse:   Allow arguments to be provided, but are not need of them.
        :return:        Nothing."""
        self.__label.font_name = self.font_name
        self.__label.font_size = self.font_size
        self.__label.text = self.text

        self.__label.texture_update()
        self.__label.size = self.__label.texture_size

        self.__compute_size()

    def __compute_color(self, *noUse) -> None:
        """Compute the tooltip colors base on provided ones.

        :param noUse:   Allow arguments to be provided, but are not need of them.
        :return:        Nothing."""
        self.__border.color = self.border_color
        self.__background.color = self.background_color
        self.__label.color = self.text_color

    def __compute_area(self) -> None:
        """Compute the tooltip display area base on window size and the size itself.

        :return: Nothing."""
        self.__area = [Window.width - self.width, Window.height - self.height]

