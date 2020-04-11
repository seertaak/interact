from interact.util import Point
from interact.abstract_event import KeyPress, MousePress, MouseMove, MouseScroll
from interact.engine import InteractionEngine


def on_key_press(ui: InteractionEngine):
    def fn(key_code: int, modifiers: int):
        ui.handle(KeyPress(key_code, 'down'))
    return fn


def on_key_release(ui: InteractionEngine):
    def fn(key_code: int, modifiers: int):
        ui.handle(KeyPress(key_code, 'up'))
    return fn


def on_mouse_press(ui: InteractionEngine):
    def fn(x, y, button, modifiers):
        ui.state.mouse_position = Point(x, y)

        b = 'left'
        if button == 4:
            b = 'middle'
        elif button == 2:
            b = 'right'

        ui.handle(MousePress(b, 'down'))
    return fn


def on_mouse_release(ui: InteractionEngine):
    def fn(x, y, button, modifiers):
        ui.state.mouse_position = Point(x, y)

        b = 'left'
        if button == 4:
            b = 'middle'
        elif button == 2:
            b = 'right'

        ui.handle(MousePress(b, 'up'))
    return fn


def on_mouse_drag(ui: InteractionEngine):
    def fn(x, y, dx, dy, button, modifier):
        ui.state.mouse_position = Point(x, y)
        ui.handle(MouseMove())
    return fn


def on_mouse_scroll(ui: InteractionEngine):
    def fn(x, y, scroll_x, scroll_y):
        ui.state.mouse_position = Point(x, y)
        ui.state.mouse_scroll = Point(scroll_x, scroll_y)
        ui.handle(MouseScroll())
    return fn


def on_mouse_motion(ui: InteractionEngine):
    def fn(x, y, button, modifiers):
        ui.state.mouse_position = Point(x, y)
        ui.handle(MouseMove())
    return fn
