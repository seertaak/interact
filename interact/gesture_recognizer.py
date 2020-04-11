from typing import Callable, List, Literal
from copy import deepcopy

from .abstract_event import Event

Handler = Callable[[], None]
State = Literal['active', 'success', 'fail']


def default_handler():
    pass


class Recognizer:
    def __init__(self, handler: Handler = default_handler):
        self.handler = handler

    def recognize(self, event: Event) -> State:
        return 'fail'


class Trivial(Recognizer):
    def __init__(self, trigger: Event, handler: Handler = default_handler):
        super().__init__(handler)
        self.trigger = trigger

    def recognize(self, event: Event) -> State:
        if event == self.trigger:
            self.handler()
            return 'success'
        return 'fail'


class IgnoreIf(Recognizer):
    def __init__(self, predicate: Callable[[Event], bool], gesture: Recognizer, handler: Handler = default_handler):
        super().__init__(handler)
        self.predicate = predicate
        self.gesture = deepcopy(gesture)
        self.state = 'initial'

    def recognize(self, event: Event) -> State:
        if self.predicate(event):
            return self.state
        self.state = self.gesture.recognize(event)
        return self.state


class Alternatives(Recognizer):
    def __init__(self, alternatives: List[Recognizer], handler: Handler = default_handler):
        super().__init__(handler)
        self.remaining_alternatives = alternatives

    def recognize(self, event: Event) -> State:
        remaining_alternatives = []
        for gesture in self.remaining_alternatives:
            state = gesture.recognize(event)
            if state == 'active':
                remaining_alternatives.append(gesture)
            elif state == 'success':
                self.handler()
                return state
        if not remaining_alternatives:
            return 'fail'

        self.remaining_alternatives = remaining_alternatives
        return 'active'


class Sequence(Recognizer):
    def __init__(self, gestures: List[Recognizer], handler: Handler = default_handler):
        super().__init__(handler)
        self.position = 0
        self.gestures = gestures

    def recognize(self, event: Event) -> State:
        assert self.position < len(self.gestures)
        gesture = self.gestures[self.position]

        state = gesture.recognize(event)

        if state == 'active':
            return 'active'
        elif state == 'success':
            self.position += 1
            if self.position == len(self.gestures):
                self.handler()
                return 'success'
            return 'active'
        return 'fail'


class Repeating(Recognizer):
    def __init__(self, gesture: Recognizer, handler: Handler = default_handler):
        super().__init__(handler)
        self.gesture_prototype = gesture
        self.gesture = deepcopy(self.gesture_prototype)

    def recognize(self, event: Event) -> State:
        state = self.gesture.recognize(event)
        if state == 'active':
            return 'active'
        elif state == 'success':
            self.gesture = deepcopy(self.gesture_prototype)
            return 'active'
        return 'fail'


class Optional(Recognizer):
    def __init__(self, gesture: Recognizer, handler: Handler = default_handler):
        super().__init__(handler)
        self.gesture = deepcopy(gesture)

    def recognize(self, event: Event) -> State:
        state = self.gesture.recognize(event)
        if state == 'active':
            return 'active'
        return 'success'


