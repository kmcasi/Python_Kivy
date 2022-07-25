# Extracted from my general font measuring logic witch have support for the pillow and tkinter also.
# https://github.com/kmcasi/Python/tree/main/Helper#font

#// IMPORT
from kivy.uix.label import Label


#// LOGIC
class FontMeasure:
    def __init__(self, font_name:str, font_size:int):
        """**Font** main purpose is to measure the size of a font single letter.
        But you can measure and an entire message(string) on multi lines.

        Example usage:

        >>> myFont = FontMeasure("comic", 18)
        >>> myFont.get_width_of("Z")    # 13
        >>> myFont.get_height_of("Z")   # 26
        >>> myFont.get_size_of("Z")     # (13, 26)

        :param font_name:   Font name as a string
        :param font_size:   Font size as an integer
        """
        # Local variables
        self._name:str = font_name
        self._size:int = font_size

    def get_width_of(self, sample:str="W") -> int:
        """Measuring the sample width.

        :param sample:  The sample as a string. Default is "W", usually is the bigger character.
        :return:        An integer.
        """
        return self.get_size_of(sample)[0]

    def get_height_of(self, sample:str="W") -> int:
        """Measuring the sample height.

        :param sample:  The sample as a string. Default is "W", usually is the bigger character.
        :return:        An integer.
        """
        return self.get_size_of(sample)[1]

    def get_size_of(self, sample:str) -> tuple[int, int]:
        """Measuring the sample size.

        :param sample:  The sample as a string. Default is "W", usually is the bigger character.
        :return:        A tuple of two integers, width and height.
        """
        # Using kivy Label to render the sample and extracting the size of it.
        font = Label(text=sample, font_name=self._name, font_size=self._size)
        font.texture_update()
        return tuple(font.texture_size)

