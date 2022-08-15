#// IMPORT
from builtins import min, max
from contextlib import contextmanager
from logging import warning as WARNING
from logging import error as ERROR
from sys import exit as CRASH

from kivy.utils import get_color_from_hex, get_hex_from_color

from lib.helper.List import List


#// LOGIC
def clamp(value:int|float, _min:int|float=0, _max:int|float=1) -> int|float:
    """Clamp value between provided min and max values.

    **Example:**

    >>> clamp(2, _min=3, _max=5)    # 3
    >>> clamp(4, _min=3, _max=5)    # 4
    >>> clamp(6, _min=3, _max=5)    # 5

    :param value:   Value to clamp.
    :param _min:    Minimum value.
    :param _max:    Maximum value.
    :return:        Clamped value."""
    return max(_min, min(value, _max))


def normalize(value:int|float, _min:int|float=0, _max:int|float=1, digits:int=21) -> float:
    """Normalize values.

    If values are bigger then *actual* limits, the return values can have negative values
    and/or bigger values then *desired* limits.

    **Example:**

    >>> normalize(1, _min=0, _max=2)
    >>> # 0.5

    :param value:   Value to normalize.
    :param _min:    Minimum expected value.
    :param _max:    Maximum expected value.
    :param digits:  Maximum fractional digits.
    :return:        Normalized values."""
    return round((value - _min) / (_max - _min), digits)


def normalize_plus(*values:int|float, actual:list|tuple, desired:list|tuple=(0, 1), digits:int=21) -> list[float]:
    """Normalize values in desired range.

    If values are bigger then *actual* limits, the return values can have negative values
    and/or bigger values then *desired* limits.

    **Example:**

    >>> normalize_plus(1, 2, 3, 4, 5, actual=(1, 5))
    >>> # [0.0, 0.25, 0.5, 0.75, 1.0]
    >>>
    >>> normalize_plus(1, 2, 3, 4, 5, actual=(3, 7), desired=(0, 2))
    >>> # [-1.0, -0.5, 0.0, 0.5, 1.0]

    :param values:  Values to normalize.
    :param actual:  Actual values range.
    :param desired: Desired values range.
    :param digits:  Maximum fractional digits.
    :return:        List of normalized values."""
    # Special thanks to Adirio for posting this answer on Jan 5, 2018
    # https://stackoverflow.com/a/48109733/10234009
    return [round(
        desired[0] + (x - actual[0]) * (desired[1] - desired[0]) / (actual[1] - actual[0])
        , digits) for x in values]


def normalize_self(*values:int|float, offset:int|float=1, digits:int=21) -> list[float]:
    """Normalize values between them self.

    This will return a list of values between 0 and 1 multiplied by offset.
    Usefull when you want to measure performance, like GitHub traffic visualizer (git clones/visitors).

    **Example:**

    >>> normalize_self(1, 2, 3, 4, 5)
    >>> # [0.2, 0.4, 0.6, 0.8, 1.0]
    >>>
    >>> normalize_self(1, 2, 3, 4, 5, offset=0.7)
    >>> # [0.14, 0.28, 0.42, 0.56, 0.7]

    :param values:  Values to normalize.
    :param digits:  Maximum fractional digits.
    :param offset:  Highest allowed value.
    :return:        List of normalized values."""
    biggest:int|float = max(*values)
    return [round(value / biggest * offset, digits) for value in values]


def percent(value1:int|float, value2:int|float, digits:int=3, difference:bool=False) -> float:
    """Percentage difference between values.

    **Example:**

    >>> percent(1, 5)                                   # 20.0 -> 1 is 20% of 5
    >>> percent(1, 5, difference=True)                  # 80.0 -> 1 needs 80% until 5
    >>> percent(0.25, 5.7, digits=2)                    # 4.39 -> 0.25 is 4.39% of 5.7
    >>> percent(0.25, 5.7, digits=2, difference=True)   # 95.61 -> 0.25 needs 95.61 until 5.7

    :param value1:      One value.
    :param value2:      Other value.
    :param digits:      Maximum fractional digits.
    :param difference:  Remaining value until the bigest one.
    :return:            Float value."""
    normalized:list[float] = normalize_self(value1, value2, digits=digits, offset=100)
    if difference: return max(normalized) - min(normalized)
    else: return min(normalized)


class Check:
    def __init__(self, def_name:str, close:bool=True) -> None:
        """The **Check** purpose is to log an error if something is wrong.

        **Example:**

        >>> checking = Check("MyClass.function")
        >>> age = 24
        >>> color = "FF004D"
        >>> with checking.arg_type("age", int): pass
        >>> with checking.RGBA("color", str, list, tuple): pass

        :param def_name:    Function name.
        :param close:       Close the application.
        :return:            Nothing."""

        self.def_name:str = def_name
        self.close:bool = close
        self.LOG = ERROR if close else WARNING

    @contextmanager
    def arg_type(self, key:str, arg:any, *types:type, ignored:list[type]=[any]) -> None:
        """The **arg_type** purpose is to log an error if argument type is a wrong one.

        :param key:     The used key argument.
        :param arg:     The used argument.
        :param types:   The accepted types.
        :param ignored: Types what can be accepted, but not recommended.
        :return:        Nothing."""

        # if type(arg) not in types:
        if type(arg) not in [*types, *ignored]:
            message: str = f"On {self.def_name}, \"{key}\" argument must be an %s, instead of {type(arg).__name__}."

            try:
                accepted: str = ""
                types_list: list[str] = [str(t).split("'", 2)[1] + (" or " if t == types[-2] else ", ") for t in types]

                for ts in types_list: accepted += ts

                self.LOG(message, accepted[:-2])

            except IndexError:
                # ERROR(message, str(types).split("'", 2)[1])
                self.LOG(message, str(types).split("'", 2)[1])

            if self.close: CRASH()

        yield


    @contextmanager
    def RGBA(self, key:str, arg:any, *types:type) -> None:
        """ The **RGBA** purpose is to log an error if the provided color has an invalid format.

        :param key:     The used key argument.
        :param types:   The accepted types.
        :param arg:     The used argument.
        :return:        Nothing."""

        try:
            self.arg_type(key, arg, *types)
            yield

        except ValueError as err:
            info:list[str] = err.args[0].split(" ", 1)[1].split("(got", 1)
            self.LOG("On %s, the \"%s\" %s: Reason -> Unable to determine RGB(A) values just from %s"
                     , self.def_name, key, info[0][:-1], info[1][1:-1])

            if self.close: CRASH()


class Make:
    """**Make** purpose is to store all helpers for creations.
    Something line `namespace` in C++.

    **Example:**

    >>> Make.Text("Some", True, "values")   # "Some True values"
    >>> Make.Color("FF004D")                # [1, 0.05, 0.35196078431372546, 1.0]
    >>> Make.Color("FF004D", HEX=True)      # #ff0c59ff
    """

    @staticmethod
    def Text(*values:object, sep:str|None=" ", end:str|None="\n") -> str:
        """Making text from provided values.

        :param values:  Arguments to be added as text.
        :param sep:     String inserted between values.
        :param end:     String appended after the last value.
        :return:        String."""
        text:str = ""

        for value in values: text += f"{sep}{value}" if sep is not None else value
        if end is not None: text += end

        return text[len(sep):] if sep is not None else text

    @staticmethod
    def Color(color, difference:float=0.05, HEX:bool=False) -> str|list[float]:
        """Making slight different color from provided color.

        :param color:       Color value.
        :param difference:  Difference added/subtracted.
        :param HEX:         If new color should be HEX type.
        :return:            New color values."""

        adding:bool = False
        # Make shore we work with RGBA color by sampling a full white color
        sample:list[float] = List(1, _len=4, _type=float)

        # If provided color is an HEX type, extract the values from it
        try: color = get_color_from_hex(color)
        except AttributeError: pass

        # Replace provided color values in the sample
        # in case the alpha values is missing
        for index in range(4): sample[index] = color[index]

        # Before to change the color sample the alpha value
        alpha:float = sample[-1]

        # Check RGB values if add the difference
        for rgb_index in range(3):
            if sample[rgb_index] - difference < 0: adding = True

        # Add/Subtract the difference
        # Also clamp teh values between 0-1 in case the provided difference is too big
        if adding: sample = [clamp(index + difference, 0, 1) for index in sample]
        else: sample = [clamp(index - difference, 0, 1) for index in sample]

        # Restore the sampled alpha value
        sample[-1] = alpha

        # Return the new color base on wanted value
        if HEX: return get_hex_from_color(sample)
        else: return sample

