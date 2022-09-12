# Extracted from my general list logic witch have support for string and boolean also.
# https://github.com/kmcasi/Python/tree/main/Helper#list

#// IMPORT
from typing import Final
from builtins import abs
from logging import error, warning


#// LOGIC
class List:
    def __init__(self, *values:int|float, size:int=4, _type:type=int) -> None:
        """List purpose is to help on list common mathematical operations and comparison.

        You can provide and unpair values like from 3 values get out 4.
        Are no any restriction for the amount provided values and the output ones.

        :param size:    Amount of values.
        :param _type:   Type of values.
        """
        # Private Variables
        self.size:Final[int] = size
        self.type:Final[type] = _type

        # Protected Variables
        self.__items:list[_type] = []
        self.__supportedType:list[type] = [int, float]
        self.__supportedType_text:str = ""
        self.__arrow:str = "\u279C"

        for sample in [f", {tp.__name__}" for tp in self.__supportedType]: self.__supportedType_text += sample
        tmp = self.__supportedType_text.rsplit(", ", 1)
        self.__supportedType_text = tmp[0][2:] + " or " + tmp[1]

        # Construct the list
        try:
            for index in range(self.size):
                value = values[index % len(values)]
                if type(value) in self.__supportedType: self.__items.append(self.type(value))
                else: raise TypeError

        except TypeError: self.__error_type("initialization")

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}': A list with {self.size} value{'s' if self.size > 1 else ''} " \
               f"of type {self.type.__name__}>"

    def __getitem__(self, index) -> int|float:
        try: return self.__items[index]
        except IndexError:
            more:bool = index > (self.size - 1)
            raise IndexError(f"{self.__class__.__name__}:[Getting] {self.__arrow} Index {index} is "
                             f"{'bigger' if more else 'less'} than {'the list size' if more else 'first value'}"
                             f"{', which' if more else '. The list size'} is {self.size}. "
                             f"Did you mean index {(self.size - 1) * (1 if more else -1)}?")

    def __setitem__(self, index, value:int|float) -> None:
        try:
            if type(value) in self.__supportedType:
                self.__items[index] = value
            else: raise TypeError

        except IndexError:
            more:bool = index > (self.size - 1)
            raise IndexError(f"{self.__class__.__name__}:[Setting] {self.__arrow} Index {index} is "
                             f"{'bigger' if more else 'less'} than {'the list size' if more else 'first value'}"
                             f"{', which' if more else '. The list size'} is {self.size}. "
                             f"Did you mean index {(self.size - 1) * (1 if more else -1)}?")
        except TypeError:
            raise TypeError(f"{self.__class__.__name__}:[Setting] {self.__arrow} Can operate only with "
                            f"{self.__supportedType_text}. The value '{value}' is a {type(value).__name__} type.")

    def __contains__(self, other:int|float) -> bool:
        try:
            if type(other) not in self.__supportedType: raise TypeError
            if other not in self.__items: return False

            # If the above conditions are not meet, then return True
            return True

        # In case some exceptions was triggered, provide a general info about that
        except TypeError: self.__error_type("contains")

    def __len__(self) -> int: return len(self.__items)
    def __str__(self) -> str: return str(self.__items)

    def __add__(self, other:list|tuple|set|dict|int|float) -> list: return self.__math_temp("+", other, "addition")
    def __sub__(self, other:list|tuple|set|dict|int|float) -> list: return self.__math_temp("-", other, "subtraction")
    def __mul__(self, other:list|tuple|set|dict|int|float) -> list: return self.__math_temp("*", other, "multiplication")
    def __truediv__(self, other:list|tuple|set|dict|int|float) -> list: return self.__math_temp("/", other, "division")
    def __floordiv__(self, other:list|tuple|set|dict|int|float) -> list: return self.__math_temp("//", other, "floor division")
    def __mod__(self, other:list|tuple|set|dict|int|float) -> list: return self.__math_temp("%", other, "modulus")

    def __iadd__(self, other:list|tuple|set|dict|int|float):
        self.__math("+=", other, "addition")
        return self

    def __isub__(self, other:list|tuple|set|dict|int|float):
        self.__math("-=", other, "subtraction")
        return self

    def __imul__(self, other:list|tuple|set|dict|int|float):
        self.__math("*=", other, "multiplication")
        return self

    def __itruediv__(self, other:list|tuple|set|dict|int|float):
        self.__math("/=", other, "division")
        return self

    def __ifloordiv__(self, other:list|tuple|set|dict|int|float):
        self.__math("//=", other, "floor division")
        return self

    def __imod__(self, other:list|tuple|set|dict|int|float):
        self.__math("%=", other, "modulus")
        return self

    def __pow__(self, power:list|tuple|set|dict|int|float, modulo:int|float|None=None) -> list:
        result:list = []
        try:
            # Extract :class:`python.builtins.set` and :class:`python.builtins.dict` values
            # to :class:`python.builtins.list`
            if type(power) is set: power = list(power)
            elif type(power) is dict: power = list(power.values())

            # If is a list
            if isinstance(power, (list, tuple)):
                # In case the size is not the same, raise an :class:`python.builtins.IndexError`
                if len(power) != self.size: raise IndexError

                # Do power math for every index value of the list with the corresponding index power
                for index in range(self.size):
                    result.append(pow(self.__items[index], power[index], modulo))

            # Otherwise, if is a single value
            else:
                # In case the value type is not in supported ones, raise an :class:`python:builtins.TypeError`
                if type(power) not in self.__supportedType: raise TypeError

                # Do power math for every value in the list
                for index in range(self.size):
                    result.append(pow(self.__items[index], power, modulo))

            return result

        # In case some exceptions was triggered, provide a general info about that
        except TypeError: self.__error_type("exponentiation")
        except IndexError: self.__error_index("exponentiation")

        except ValueError as ve:
            from traceback import print_stack
            print_stack(limit=-1)

            modulus:str = ""
            if ve.args[0].endswith(" modulus"): modulus = f" ({str(modulo)})"
            warning(f"{self.__class__.__name__}:[Exponentiation] {self.__arrow} {ve.args[0].capitalize()}{modulus}.")

    def __ipow__(self, power:list|tuple|set|dict|int|float, modulo:int|float|None=None):
        try:
            # Extract :class:`python.builtins.set` and :class:`python.builtins.dict` values
            # to :class:`python.builtins.list`
            if type(power) is set: power = list(power)
            elif type(power) is dict: power = list(power.values())

            # If is a list
            if isinstance(power, (list, tuple)):
                # In case the size is not the same, raise an :class:`python.builtins.IndexError`
                if len(power) != self.size: raise IndexError

                # Do power math for every index value of the list with the corresponding index power
                for index in range(self.size):
                    self.__items[index] = pow(self.__items[index], power[index], modulo)

            # Otherwise, if is a single value
            else:
                # In case the value type is not in supported ones, raise an :class:`python:builtins.TypeError`
                if type(power) not in self.__supportedType: raise TypeError

                # Do power math for every value in the list
                for index in range(self.size):
                    self.__items[index] = pow(self.__items[index], power, modulo)

            return self

        # In case some exceptions was triggered, provide a general info about that
        except TypeError: self.__error_type("exponentiation")
        except IndexError: self.__error_index("exponentiation")

        except ValueError as ve:
            from traceback import print_stack
            print_stack(limit=-1)

            modulus:str = ""
            if ve.args[0].endswith(" modulus"): modulus = f" ({str(modulo)})"
            warning(f"{self.__class__.__name__}:[Exponentiation] {self.__arrow} {ve.args[0].capitalize()}{modulus}.")

    def __neg__(self) -> list: return [(v * -1) if v > 0 else v for v in self.__items]
    def __pos__(self) -> list: return [(v * -1) if v < 0 else v for v in self.__items]
    def __abs__(self) -> list: return [abs(v) for v in self.__items]
    def __floor__(self) -> list: return [self.type(float(v).__floor__()) for v in self.__items]
    def __ceil__(self) -> list: return [self.type(float(v).__ceil__()) for v in self.__items]
    def __trunc__(self) -> list: return [self.type(float(v).__trunc__()) for v in self.__items]
    def __round__(self, n:int|None=None) -> list: return [self.type(float(v).__round__(n)) for v in self.__items]
    def __reversed__(self) -> list: return [self[self.size - index - 1] for index in range(self.size)]

    def __int__(self) -> list:
        if self.type is int: return self.__items
        return [int(v) for v in self.__items]

    def __float__(self) -> list:
        if self.type is float: return self.__items
        return [float(v) for v in self.__items]

    def __lt__(self, other:list|tuple|set|dict|int|float) -> bool:
        try:
            # Extract :class:`python.builtins.set` and :class:`python.builtins.dict` values
            # to :class:`python.builtins.list`
            if type(other) is set: other = list(other)
            elif type(other) is dict: other = list(other.values())

            # If is a list
            if isinstance(other, (list, tuple)):
                # In case the size is not the same, raise an :class:`python.builtins.IndexError`
                if len(other) != self.size: raise IndexError

                # In case the index value is less than index list value, return False
                for index in range(self.size):
                    if other[index] < self.__items[index]: return False

            # Otherwise, if is a single value
            else:
                # In case the value type is not in supported ones, raise an :class:`python:builtins.TypeError`
                if type(other) not in self.__supportedType: raise TypeError

                # In case the value is less than one list value, return False
                for index in self.__items:
                    if other < index: return False

            # If the above conditions are not meet, then return True
            return True

        # In case some exceptions was triggered, provide a general info about that
        except TypeError: self.__error_type("comparison")
        except IndexError: self.__error_index("comparison")

    def __gt__(self, other:list|tuple|set|dict|int|float) -> bool:
        try:
            # Extract :class:`python.builtins.set` and :class:`python.builtins.dict` values
            # to :class:`python.builtins.list`
            if type(other) is set: other = list(other)
            elif type(other) is dict: other = list(other.values())

            # If is a list
            if isinstance(other, (list, tuple)):
                # In case the size is not the same, raise an :class:`python.builtins.IndexError`
                if len(other) != self.size: raise IndexError

                # In case the index value is bigger than index list value, return False
                for index in range(self.size):
                    if other[index] > self.__items[index]: return False

            # Otherwise, if is a single value
            else:
                # In case the value type is not in supported ones, raise an :class:`python:builtins.TypeError`
                if type(other) not in self.__supportedType: raise TypeError

                # In case the value is bigger than one list value, return False
                for index in self.__items:
                    if other > index: return False

            # If the above conditions are not meet, then return True
            return True

        # In case some exceptions was triggered, provide a general info about that
        except TypeError: self.__error_type("comparison")
        except IndexError: self.__error_index("comparison")

    def __eq__(self, other:list|tuple|set|dict|int|float) -> bool:
        try:
            # Extract :class:`python.builtins.set` and :class:`python.builtins.dict` values
            # to :class:`python.builtins.list`
            if type(other) is set: other = list(other)
            elif type(other) is dict: other = list(other.values())

            # If is a list
            if isinstance(other, (list, tuple)):
                # In case the size is not the same, raise an :class:`python.builtins.IndexError`
                if len(other) != self.size: raise IndexError

                # In case the index value is NOT equal than index list value, return False
                for index in range(self.size):
                    if other[index] != self.__items[index]: return False

            # Otherwise, if is a single value
            else:
                # In case the value type is not in supported ones, raise an :class:`python:builtins.TypeError`
                if type(other) not in self.__supportedType: raise TypeError

                # In case the value is NOT equal with one list value, return False
                for index in self.__items:
                    if other != index: return False

            # If the above conditions are not meet, then return True
            return True

        # In case some exceptions was triggered, provide a general info about that
        except TypeError: self.__error_type("comparison")
        except IndexError: self.__error_index("comparison")

    def __le__(self, other:list|tuple|set|dict|int|float) -> bool: return self < other or self == other
    def __ge__(self, other:list|tuple|set|dict|int|float) -> bool: return self > other or self == other

    def intersect(self, other:list|tuple|set|dict|int|float) -> list:
        """Find which values are intersecting.

        :param other:   Comparative sample.
        :return:        List of intersected values."""
        result:list = []

        try:
            # Extract :class:`python.builtins.set` and :class:`python.builtins.dict` values
            # to :class:`python.builtins.list`
            if type(other) is set: other = list(other)
            elif type(other) is dict: other = list(other.values())

            # If is a list
            if isinstance(other, (list, tuple)):
                # In case the size is not the same, raise an :class:`python.builtins.IndexError`
                if len(other) != self.size: raise IndexError

                for value in other:
                    if value in self.__items:
                        if value not in result: result.append(value)

            # Otherwise, if is a single value
            else:
                # In case the value type is not in supported ones, raise an :class:`python:builtins.TypeError`
                if type(other) not in self.__supportedType: raise TypeError

                if other in self.__items: result.append(other)

            # If the above conditions are not meet, then return True
            return result

        # In case some exceptions was triggered, provide a general info about that
        except TypeError: self.__error_type("comparison")
        except IndexError: self.__error_index("comparison")

    def __math(self, operation:str, other:any, info:str) -> None:
        exec(f"""
try:
    if type(other) is set: other = list(other)
    elif type(other) is dict: other = list(other.values())
    
    if isinstance(other, (list, tuple)):
        if len(other) != self.size: raise IndexError
        
        for index in range(self.size):
            self._{self.__class__.__name__}__items[index] {operation} other[index]
    
    else:
        if type(other) not in self._{self.__class__.__name__}__supportedType: raise TypeError
        
        for index in range(self.size):
            self._{self.__class__.__name__}__items[index] {operation} other

except TypeError: self._{self.__class__.__name__}__error_type("{info}")
except IndexError: self._{self.__class__.__name__}__error_index("{info}")
        """, {"self": self,
              "other": other,
              "error": error}
             )

    def __math_temp(self, operation:str, other:any, info:str) -> list:
        result:list = []
        exec(f"""
try:
    if type(other) is set: other = list(other)
    elif type(other) is dict: other = list(other.values())
    
    if isinstance(other, (list, tuple)):
        if len(other) != self.size: raise IndexError
        
        for index in range(self.size):
            result.append(self._{self.__class__.__name__}__items[index] {operation} other[index])
    
    else:
        if type(other) not in self._{self.__class__.__name__}__supportedType: raise TypeError
        
        for index in range(self.size):
            result.append(self._{self.__class__.__name__}__items[index] {operation} other)

except TypeError: self._{self.__class__.__name__}__error_type("{info}")
except IndexError: self._{self.__class__.__name__}__error_index("{info}")
        """, {"self": self,
              "result":result,
              "other": other,
              "error": error}
             )
        return result

    def __error_type(self, info:str) -> None:
        raise TypeError(f"{self.__class__.__name__}:[{info.capitalize()}] {self.__arrow} Can operate only with "
              f"{self.__supportedType_text}.")

    def __error_index(self, info:str) -> None:
        raise TypeError(f"{self.__class__.__name__}:[{info.capitalize()}] {self.__arrow} Can operate only with "
              f"lists of the same size.")
