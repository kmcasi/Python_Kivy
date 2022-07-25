# Extracted from my general list logic witch have support for string and boolean also.
# https://github.com/kmcasi/Python/tree/main/Helper#list

#// LOGIC
def List(*values:any, _len:int=4, _type:type=int) -> list:
    """**List** purpose is to return a list of elements.
    You can provide and unpair values like from 3 values get out 4.

    Main reaso was because kivy *VariableListProperty* had not worked for me for some reasons ``\(-_-)/``.

    Accepted values and the return type are: int, float, str, bool.
    See extreme example below:

    >>> List(3)                             # [3, 3, 3, 3]
    >>> List(1, 2.3, _type=float)           # [1.0, 2.3, 1.0, 2.3]
    >>> List(0.6, "a", False, _len=5)       # [1, 97, 0, 1, 97]
    >>> List(0.3, "z", _len=2, _type=bool)  # [False, True]
    >>> List(0.3, 2, True, "a", _type=str)  # ['0.3', '2', 'True', 'a']

    :param values:  The value(s) provided.
    :param _type:   The type of list elements.
    :param _len:    The amount of list elements.
    """
    supportedType:list[type] = [int, float]

    _check_for_valid_type(_type, supportedType, "return")

    out:list = []
    keep:bool = True
    while keep:
        for index in range(len(values)):
            value = values[index]
            _check_for_valid_type(type(value), supportedType)

            try:
                out.append(_type(value))

                if len(out) == _len: keep = False
            except Exception as e: raise Exception(e)

    return out


def _check_for_valid_type(value:type, types:list[type], prefix:str="value") -> None:
    """
    The **_check_for_valid_type** function purpose is how the name is saying, to check if value is a valid type.

    :param prefix:  Word used to describe the checked value.
    :param value:   Value type to check for.
    :param types:   List of accepted types.

    :raise TypeError: If the condition is not met.
    """
    if value not in types:
        message:str = f"The list class {prefix} type must be one of: "
        _t = [str(t).split("'")[1] + (" or " if t == types[-2] else "." if t == types[-1] else ", ")
              for t in types]

        for _st in _t: message += _st

        raise TypeError(message)
