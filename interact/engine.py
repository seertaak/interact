from dataclasses import dataclass
from typing import Callable, List, Literal
from copy import deepcopy

from .util import Point
from .abstract_event import Event
from .gesture_recognizer import Recognizer


@dataclass
class UIState:
    mouse_position: Point = Point(0, 0)
    mouse_scroll: Point = Point(0, 0)


class InteractionEngine:
    def __init__(self):
        self.gesture_prototypes = []
        self.gestures = []
        self.state = UIState()

    @property
    def commands(self):
        return self.gesture_prototypes

    @commands.setter
    def commands(self, gestures: List[Recognizer]):
        self.gesture_prototypes = gestures
        self.gestures = deepcopy(self.gesture_prototypes)

    def _handle(self, event: Event) -> List[Recognizer]:
        active_gestures = []
        for gesture in self.gestures:
            state = gesture.recognize(event)
            if state == 'active':
                active_gestures.append(gesture)
        return active_gestures

    def handle(self, event: Event):
        active_gestures = self._handle(event)

        if active_gestures:
            self.gestures = active_gestures
        else:
            self.gestures = deepcopy(self.gesture_prototypes)
            self.gestures = self._handle(event)
