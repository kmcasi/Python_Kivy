#// IMPORT
from kivy.properties import NumericProperty, ReferenceListProperty, VariableListProperty
from kivy.uix.layout import Layout

from lib.helper.List import List


#// GLOBAL VARIABLES


#// LOGIC
class OverlayLayout(Layout):
    x = NumericProperty(0)
    '''X position of the overlay layout.

    :attr:`x` is a :class:`~kivy.properties.NumericProperty` and defaults to 0.
    '''

    y = NumericProperty(0)
    '''Y position of the overlay layout.

    :attr:`y` is a :class:`~kivy.properties.NumericProperty` and defaults to 0.
    '''

    width = NumericProperty(100)
    '''Width of the overlay layout.

    :attr:`width` is a :class:`~kivy.properties.NumericProperty` and defaults to 100.

    .. warning::
        Keep in mind that the `width` property is subject to layout logic and
        that this has not yet happened at the time of the overlay layout's `__init__`
        method.
    '''

    height = NumericProperty(100)
    '''Height of the overlay layout.

    :attr:`height` is a :class:`~kivy.properties.NumericProperty` and defaults to 100.

    .. warning::
        Keep in mind that the `height` property is subject to layout logic and
        that this has not yet happened at the time of the overlay layout's `__init__`
        method.
    '''

    pos = ReferenceListProperty(x, y)
    '''Position of the overlay layout.

    :attr:`pos` is a :class:`~kivy.properties.ReferenceListProperty` of
    (:attr:`x`, :attr:`y`) properties.
    '''

    size = ReferenceListProperty(width, height)
    '''Size of the overlay layout.

    :attr:`size` is a :class:`~kivy.properties.ReferenceListProperty` of
    (:attr:`width`, :attr:`height`) properties.
    '''

    padding = VariableListProperty([0])
    '''Padding between layout margins and children(s).
    
    Padding can be provided in multiple ways:
        [1] \u279c [padding_left, padding_top, padding_right, padding_bottom]
        
        [2] \u279c [padding_horizontal, padding_vertical]
        
        [3] \u279c [padding]

    :attr:`padding` is a :class:`~kivy.properties.VariableListProperty` and defaults to [0, 0, 0, 0].
    '''

    def __init__(self, **kwargs):
        super(OverlayLayout, self).__init__(**kwargs)
        update = self._trigger_layout
        fbind = self.fbind
        fbind("x", update)
        fbind("y", update)
        fbind("width", update)
        fbind("height", update)
        fbind("padding", update)
        fbind("size", update)
        fbind("pos", update)

    def do_layout(self, *args):
        pos:tuple[float, float] = self.__compute_pos()
        size:tuple[float, float] = self.__compute_size()

        change_layout_size:bool = False
        new_width:list[float] = []
        new_height:list[float] = []

        for child in self.children:
            child.pos = pos

            if child.size_hint_x is not None: child.width = size[0]
            else: change_layout_size = True

            if child.size_hint_y is not None: child.height = size[1]
            else: change_layout_size = True

        if change_layout_size:
            for child in self.children:
                new_width.append(child.width)
                new_height.append(child.height)
            self.size = (max(new_width), max(new_height))

    def __compute_size(self) -> tuple[float, float]:
        w:float = self.width - self.padding[0] - self.padding[2]
        h:float = self.height - self.padding[1] - self.padding[3]
        return w, h

    def __compute_pos(self) -> tuple[float, float]:
        x:float = self.x + self.padding[0]
        y:float = self.y + self.padding[3]
        return x, y
