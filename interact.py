from dataclasses import dataclass, field
from typing import *
from copy import deepcopy

ButtonAction = Literal['up', 'down']
MouseButton = Literal['left', 'middle', 'right']


@dataclass
class Point:
    x: int = 0
    y: int = 0


@dataclass
class UIState:
    mouse_position: Point = Point()


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

Event = Union[KeyPress, MousePress, MouseMove]
State = Literal['active', 'success', 'repeat_success', 'fail']
Handler = Callable[[], None]

ui_state = UIState()

def default_handler(e: UIState):
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
            self.handler(ui_state)
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
            print("PREDICATE TRIGGERED")
            return self.state
        print("SUb-GETSTIUr")
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
            elif state == 'success' or state == 'repeat_success':
                self.handler(ui_state)
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
                self.handler(ui_state)
                return 'success'
            return 'active'
        elif state == 'repeat_success':
            self.position += 1
            if self.position == len(self.gestures):
                self.handler(ui_state)
                return 'repeat_success'
            return self.recognize(event)
        return 'fail'


class Repeating(Recognizer):
    def __init__(self, gesture: Recognizer, handler: Handler = default_handler):
        super().__init__(handler)
        self.gesture_prototype = gesture
        self.gesture = deepcopy(self.gesture_prototype)
        self.success = 0

    def recognize(self, event: Event) -> State:
        state = self.gesture.recognize(event)
        if state == 'active':
            print(1)
            return 'active'
        elif state == 'success':
            self.success = True
            self.gesture = deepcopy(self.gesture_prototype)
            print(2)
            return 'active'
        elif state == 'repeat_success':
            self.success = True
            self.gesture = deepcopy(self.gesture_prototype)
            state = self.recognize(event)
            if state == 'active':
                print(3)
                return 'active'
            elif state == 'success':
                self.gesture = deepcopy(self.gesture_prototype)
                print(4)
                return 'active'
            self.handler(ui_state)
            print(5)
            return 'repeat_success'
        if self.success:
            self.handler(ui_state)
            print(6)
            return 'repeat_success'
        print(7)
        return 'fail'


class Optional(Recognizer):
    def __init__(self, gesture: Recognizer, handler: Handler = default_handler):
        super().__init__(handler)
        self.gesture = deepcopy(gesture)

    def recognize(self, event: Event) -> State:
        state = self.gesture.recognize(event)
        if state == 'active':
            return 'active'
        elif state == 'success':
            return 'success'
        elif state == 'repeat_success':
            return 'repeat_success'
        return 'repeat_success'


class InteractionMachine:
    def __init__(self, gestures: List[Recognizer]):
        self.gesture_prototypes = gestures
        self.gestures = deepcopy(self.gesture_prototypes)

    def handle(self, event: Event):
        active_gestures = []
        for gesture in self.gestures:
            state = gesture.recognize(event)
            if state != 'fail':
                print(gesture, state)
            if state == 'active':
                active_gestures.append(gesture)

        if active_gestures:
            self.gestures = active_gestures
        else:
            print("WIPING SLATE")
            self.gestures = deepcopy(self.gesture_prototypes)

        if False:
            self.gestures = active_gestures if active_gestures else deepcopy(self.gesture_prototypes)


if __name__ == '__main__':
    def handler(ui: UIState):
        print("Success!")

    c_down = KeyPress(ord('c'), 'down')
    c_up = KeyPress(ord('c'), 'up')

    r = Trivial(c_down)
    r.handler = handler

    ui = InteractionMachine([r])

    r.recognize(c_down)
    r.recognize(c_up)
    r.recognize(c_down)
