from typing import Callable, List, Literal
from copy import deepcopy

from .abstract_event import Event, KeyPress

Handler = Callable[[], None]
State = Literal['active', 'success', 'fail']


def default_handler():
    pass


class Recognizer:
    def __init__(self, handler: Handler = default_handler):
        self.handler = handler

    def recognize(self, event: Event) -> State:
        return 'fail'

    def __sub__(self, other):
        return Sequence([deepcopy(self), deepcopy(other)])

    def __or__(self, other):
        return Alternatives([deepcopy(self), deepcopy(other)])

    def __add__(self, other):
        steps = []
        if isinstance(self, Sequence):
            steps.extend(self.gestures)
        if isinstance(other, Sequence):
            steps.extend(other.gestures)
        return Sequence([steps])

    def __getitem__(self, handler):
        copy = deepcopy(self)
        copy.handler = handler
        return copy

    @property
    def repeat(self):
        return Repeating(deepcopy(self))

    def repeat_until(self, r: 'Recognizer'):
        return Repeating(deepcopy(self), until=r)

    @property
    def ignore_if(self, fn):
        return IgnoreIf(fn, deepcopy(self))

    @property
    def ignore_key_up(self):
        return IgnoreIf(lambda e: isinstance(e, KeyPress) and e.action == 'up', deepcopy(self))


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
        if self.state == 'success':
            self.handler()
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

    def __sub__(self, other):
        steps = deepcopy(self.gestures)
        if isinstance(other, Sequence):
            steps.extend(deepcopy(other.gestures))
        else:
            steps.append(deepcopy(other))
        return Sequence(steps)


class Repeating(Recognizer):
    def __init__(self, gesture: Recognizer, until: Recognizer = None, handler: Handler = default_handler):
        super().__init__(handler)
        self.gesture_prototype = gesture
        self.gesture = deepcopy(self.gesture_prototype)
        self.until = until
        self.in_until = False

    def recognize(self, event: Event) -> State:
        if not self.in_until:
            state = self.gesture.recognize(event)
            if state == 'active':
                return 'active'
            elif state == 'success':
                self.gesture = deepcopy(self.gesture_prototype)
                return 'active'
        if self.until:
            self.in_until = True
            return self.until.recognize(event)
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


