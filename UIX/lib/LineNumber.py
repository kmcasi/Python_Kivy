#//|>-----------------------------------------------------------------------------------------------------------------<|
#//| Copyright (c) 01 Sep 2024. All rights are reserved by ASI
#//|>-----------------------------------------------------------------------------------------------------------------<|

#// IMPORT
from os import cpu_count
from concurrent.futures import ThreadPoolExecutor as Threads

from kivy.core.text import DEFAULT_FONT, Label
from kivy.graphics import Color, Rectangle, BorderImage
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from kivy.properties import StringProperty, NumericProperty, ColorProperty, OptionProperty
from kivy.properties import ListProperty, VariableListProperty


#// LOGIC
class LineNumber(Widget):
    align = OptionProperty('right', options=['left', 'center', 'right'])
    '''Horizontal alignment of the text.
    
    Available options are : left, center and right.
    
    :attr:`align` is an :class:`~kivy.properties.OptionProperty` and defaults to 'right'.
    '''

    background_color = ColorProperty()
    '''Current tint color of the background, in (r, g, b, a) format.

    :attr:`background_color` is a :class:`~kivy.properties.ColorProperty` and defaults to [1, 1, 1, 1] (white).
    '''

    background_texture = StringProperty('atlas://data/images/defaulttheme/textinput')
    '''Background image of the line numbers.

    :attr:`background_texture` is a :class:`~kivy.properties.StringProperty` and defaults to 
    'atlas://data/images/defaulttheme/textinput'.
    '''

    border = ListProperty([4, 4, 4, 4])
    '''Border used for :class:`~kivy.graphics.vertex_instructions.BorderImage` graphics instruction. 
    Used with :attr:`background_texture`. Can be used for a custom background.

    It must be a list of four values: (bottom, right, top, left). Read the BorderImage instruction for more 
    information about how to use it.

    :attr:`border` is a :class:`~kivy.properties.ListProperty` and defaults to [4, 4, 4, 4].
    '''

    font_context = StringProperty(None, allownone=True)
    '''Font context. `None` means the font is used in isolation, so you are guaranteed to be drawing with the TTF file 
    resolved by :attr:`font_name`. Specifying a value here will load the font file into a named context, enabling 
    fallback between all fonts in the same context. If a font context is set, you are not guaranteed that rendering 
    will actually use the specified TTF file for all glyphs (Pango will pick the one it thinks is best).

    If Kivy is linked against a system-wide installation of FontConfig, you can load the system fonts by specifying a 
    font context starting with the special string `system://`. This will load the system fontconfig configuration and 
    add your application-specific fonts on top of it (this imposes a significant risk of family name collision, 
    Pango may not use your custom font file, but pick one from the system)

    .. note::
        This feature requires the Pango text provider.

    :attr:`font_context` is a :class:`~kivy.properties.StringProperty` and defaults to None.
    '''

    font_family = StringProperty(None, allownone=True)
    '''Font family, this is only applicable when using :attr:`font_context` option. The specified font family will be 
    requested, but note that it may  not be available, or there could be multiple fonts registered with the same family.
    The value can be a family name (string) available in the font context (for example a system font in a `system://` 
    context, or a custom font file added using :class:`kivy.core.text.FontContextManager`).
    If set to `None`, font selection is controlled by the :attr:`font_name` setting.

    .. note::
        If using :attr:`font_name` to reference a custom font file, you should leave this as `None`. 
        The family name is managed automatically in this case.

    .. note::
        This feature requires the Pango text provider.

    :attr:`font_family` is a :class:`~kivy.properties.StringProperty` and defaults to None.
    '''

    font_name = StringProperty(DEFAULT_FONT)
    '''Filename of the font to use. The path can be absolute or relative.
    Relative paths are resolved by the :func:`~kivy.resources.resource_find` function.

    :attr:`font_name` is a :class:`~kivy.properties.StringProperty` and defaults to 'Roboto'. 
    This value is taken from :class:`~kivy.config.Config`.
    '''

    font_size = NumericProperty('15sp')
    '''Font size of the text in pixels.

    :attr:`font_size` is a :class:`~kivy.properties.NumericProperty` and defaults to 15 :attr:`~kivy.metrics.sp`.
    '''

    foreground_color = ColorProperty([0, 0, 0, 1])
    '''Current color of the foreground, in (r, g, b, a) format.

    :attr:`foreground_color` is a :class:`~kivy.properties.ColorProperty` and defaults to [0, 0, 0, 1] (black).
    '''

    padding = VariableListProperty([4], length=2)
    '''Horizontal padding of the text: [padding_left, padding_right].

    padding also accepts a one argument form [padding_horizontal].

    :attr:`padding` is a :class:`~kivy.properties.VariableListProperty` and defaults to [4, 4].
    '''

    width_min = NumericProperty('18sp')
    '''Minimum desired width of the text in pixels.

    :attr:`width_min` is a :class:`~kivy.properties.NumericProperty` and defaults to 18 :attr:`~kivy.metrics.sp`.
    '''

    def __init__(self, text_input, **kwargs) -> None:
        super().__init__(**kwargs)

        # Private variables
        self.__text_input:TextInput = text_input
        self.__desired_number_width:int = 0

        self.__bind()
        self._update_font()

    def __bind(self) -> None:
        self.bind(align=self._update_line_numbers,
                  background_color=self._update_line_numbers,
                  background_texture=self._update_line_numbers,
                  border=self._update_line_numbers,
                  font_context=self._update_font,
                  font_family=self._update_font,
                  font_name=self._update_font,
                  font_size=self._update_font,
                  foreground_color=self._update_line_numbers,
                  padding=self._update_line_numbers)

        self.__text_input.bind(parent=self._sync_scroll,
                               size=self._update_line_numbers,
                               text=self._update_line_numbers)

    def _sync_scroll(self, instance:TextInput, parent) -> None:
        """Used to bind the scroll event for updating the line numbers."""
        # Kivy’s unbind method is designed to quietly fail if the event handler doesn't exist
        instance.unbind(scroll_y=self._update_line_numbers)
        try: instance.parent.unbind(scroll_y=self._update_line_numbers)
        except KeyError: pass

        # Bind :attr:`scroll_y` base on the parent
        if isinstance(parent, ScrollView):
            instance.parent.bind(scroll_y=self._update_line_numbers)
        else:
            instance.bind(scroll_y=self._update_line_numbers)

    def _update_font(self, *_) -> None:
        """Used to calculate the maximum width need it to draw one number."""
        sizes:list[int] = []

        for number in range(10):
            label = Label(text=str(number), font_size=self.font_size, font_name=self.font_name,
                          font_family=self.font_family, font_context=self.font_context)
            label.refresh()
            sizes.append(label.texture.size[0])

        self.__desired_number_width = max(*sizes)
        self._update_line_numbers()

    def __draw_line_number(self, number:int, y:float, y_min_render:float, y_max_render:float) -> None:
        """Used to draw one line number."""
        # Make texture
        label:Label = Label(text=str(number), color=self.foreground_color, font_size=self.font_size,
                            font_name=self.font_name, font_family=self.font_family, font_context=self.font_context)
        label.refresh()

        # Get necessary values for drawing
        texture:Texture = label.texture
        size:list[int] = [*texture.size]
        uv:list[float] = [
            0.0, 1.0,   # bottom-left
            1.0, 1.0,   # bottom-right
            1.0, 0.0,   # top-right
            0.0, 0.0    # top-left
        ]

        # Update the values for partial visible ones
        if y > y_max_render:
            h:int = int(size[1] - (y - y_max_render))
            uv[5] = uv[7] = 1.0 - h / size[1]
            size[1] = h

        if y < y_min_render:
            h:int = int(y + size[1] - y_min_render)
            uv[1] = uv[3] = h / size[1]
            size[1] = h
            y = y_min_render

        # Calculate the horizontal position
        if self.align == "left":
            x = self.x + self.padding[0]
        elif self.align == "right":
            x = self.width - size[0] - self.padding[1]
        else:
            x = (self.width - size[0]) // 2

        # Draw the line number
        Rectangle(texture=texture, pos=(x, y), size=size, tex_coords=uv)

    def __count_wrapped_lines(self, arg:list[int, int]) -> int:
        """Used to count the amount of wrapped lines with multithreading."""
        wrapped:int = 0

        try:
            for index in range(arg[0], sum(arg)):
                if self.__text_input._lines_flags[index] != 1:
                    wrapped += 1

        except IndexError: pass

        return wrapped

    def _update_line_numbers(self, *_) -> None:
        """Update the visible line numbers"""
        self.canvas.clear()

        # Draw the line number
        with self.canvas:
            Color(*self.background_color)

            # Get necessary values
            total_lines:int = len(self.__text_input._lines_flags)
            padding_top:float = self.__text_input.padding[1]
            padding_bottom:float = self.__text_input.padding[3]
            line_height:int = self.__text_input.line_height

            # Calculate the constraints
            y: float = self.top - padding_top - line_height
            y_min:float = self.y - line_height + 1
            # y_max:float = self.top - 1
            y_min_render:float = self.y
            y_max_render:float = self.top - line_height

            # Update the constraints base on the parent instance
            if not isinstance(self.__text_input.parent, ScrollView):
                y_min += padding_bottom
                # y_max -= padding_top
                y_min_render += padding_bottom
                y_max_render -= padding_top

            # Auto update necessary parameters
            desired_width:int = self.padding[0] + self.padding[1] + self.__desired_number_width * len(str(total_lines))
            self.width = max(self.width_min,  desired_width)

            # Calculate the scroll position, first visible lines and vertical position of the first line
            if isinstance(self.__text_input.parent, ScrollView):
                hidden_area:float = self.__text_input.height - self.height
                scroll:float = (1.0 - self.__text_input.parent.scroll_y) * hidden_area
                first_visible_line:int = max(0, int((scroll - padding_top) / line_height))

                try: y = self.__text_input._lines_rects[first_visible_line].pos[1] - hidden_area + scroll + self.y
                except IndexError: pass

            else:
                scroll:float = self.__text_input.scroll_y
                first_visible_line:int = max(0, int(scroll / line_height))
                y += scroll % line_height

            # If the text is wrapped, calculate the first logical line number
            if self.__text_input.do_wrap:
                line_number:int = first_visible_line
                cpus:int = max(2, cpu_count() - 7)

                # Use multithreading if is worth it. Otherwise, will be much slower than main thread
                if line_number > 100:
                    chunk_size:int = line_number // cpus
                    chunk_offset:int = line_number - chunk_size * cpus

                    with Threads() as threads:
                        chunks = [[cpu * chunk_size, chunk_size] for cpu in range(cpus)]
                        # Offset the first chunk by one, because the first line is not counted as a new line
                        chunks[0][0] += 1
                        chunks[0][1] -= 1

                        # If we have an unequal chunk size, use it also
                        if chunk_offset > 0:
                            chunks.append([cpus * chunk_size, chunk_offset])

                        # Use the multithreading for counting wrapped lines and update the line number
                        line_number -= sum(threads.map(self.__count_wrapped_lines, chunks))

                # Otherwise, use the main thread for counting the real line numbers
                else:
                    try:
                        for hidden_line in range(1, first_visible_line):
                            if self.__text_input._lines_flags[hidden_line] != 1:
                                line_number -= 1

                    except IndexError: pass

            # Draw background
            BorderImage(source=self.background_texture, pos=self.pos, size=self.size, border=self.border)

            # Check for all visible lines
            for line in range(first_visible_line, total_lines):
                try:
                    # If the text is wrapped, draw the logical line number only for non-wrapped lines
                    if self.__text_input.do_wrap:
                        if self.__text_input._lines_flags[line] == 1 or line == 0:
                            line_number += 1
                            self.__draw_line_number(line_number, y, y_min_render, y_max_render)

                    # Otherwise draw the line number for every line
                    else:
                        self.__draw_line_number(line + 1, y, y_min_render, y_max_render)

                except IndexError: pass

                # Move to the next line's y position
                y -= line_height

                # Break if we've rendered all the visible lines
                if y < y_min: break
