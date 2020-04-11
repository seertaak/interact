from dataclasses import dataclass
from typing import Literal, Union

ButtonAction = Literal['up', 'down']
MouseButton = Literal['left', 'middle', 'right']


@dataclass
class KeyPress:
    key: int
    action: ButtonAction


@dataclass
class MousePress:
    button: MouseButton
    action: ButtonAction


@dataclass
class MouseMove:
    pass


@dataclass
class MouseScroll:
    pass


Event = Union[KeyPress, MousePress, MouseMove, MouseScroll]
