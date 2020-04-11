import pyglet as gl
from pyglet.window import key
from colorsys import *
from interact import *

window = gl.window.Window(resizable=True)
label = gl.text.Label('', font_name='Ubuntu', font_size=20, x=window.width / 2, y=window.height / 2,
                      anchor_x='center', anchor_y='center')

bg = (1.0, 0, 0)

def change_color(state: UIState):
    global bg
    h, s, v = rgb_to_hsv(*bg)
    h += 0.1
    bg = hsv_to_rgb(h, s, v)
    args = list(bg)
    args.append(1.0)
    gl.gl.glClearColor(*args)


def change_intensity(dintensity):
    global bg
    h, s, v = rgb_to_hsv(*bg)
    v += dintensity
    bg = hsv_to_rgb(h, s, v)
    args = list(bg)
    args.append(1.0)
    gl.gl.glClearColor(*args)

def change_saturation(dsat):
    global bg
    h, s, v = rgb_to_hsv(*bg)
    s += dsat
    bg = hsv_to_rgb(h, s, v)
    args = list(bg)
    args.append(1.0)
    gl.gl.glClearColor(*args)


cmd_quit = Trivial(KeyPress(ord('q'), 'up'), lambda ui: gl.app.exit())
lines: List[Point] = []
main_batch = gl.graphics.Batch()

def draw_lines():
    global main_batch
    main_batch = gl.graphics.Batch()
    for line in lines:
        main_batch.add(
            2,
            gl.gl.GL_LINES,
            None,
            ('v2f', (line[0].x, line[0].y, line[1].x, line[1].y)),
            ('c3B', (255, 255, 255, 255, 255, 255))
        )

def begin_line(ui: UIState):
    lines.append((ui.mouse_position, ui.mouse_position))
    draw_lines()

def update_line(ui: UIState):
    assert lines
    lines[-1] = (lines[-1][0], ui.mouse_position)
    draw_lines()

cmd_draw_line = Sequence([
    Trivial(KeyPress(ord('l'), 'down')),
    Trivial(KeyPress(ord('l'), 'up')),
    Optional(Repeating(Trivial(MouseMove()))),
    Trivial(MousePress('left', 'down'), begin_line),
    Repeating(Trivial(MouseMove(), update_line))
])

cmd_change_color = IgnoreIf(
    lambda e: isinstance(e, KeyPress) and e.action == 'up',
    Sequence([
        Trivial(KeyPress(ord('c'), 'down')),
        Repeating(Trivial(KeyPress(ord('d'), 'down'), change_color))
    ])
)

cmd_change_intensity = Sequence(
    [
        Trivial(KeyPress(ord('i'), 'down')),
        Repeating(
            Alternatives([
                Sequence(
                    [
                        Trivial(KeyPress(key.UP, 'down')),
                        Trivial(KeyPress(key.UP, 'up')),
                    ],
                    lambda _: change_intensity(0.1)
                ),
                Sequence(
                    [
                        Trivial(KeyPress(key.DOWN, 'down')),
                        Trivial(KeyPress(key.DOWN, 'up')),
                    ],
                    lambda _: change_intensity(-0.1)
                ),
                Trivial(
                    MouseScroll(),
                    lambda ui: change_intensity(ui.mouse_scroll.y/100.0)
                )
            ])
        )
    ]
)
cmd_change_saturation = Sequence(
    [
        Trivial(KeyPress(ord('s'), 'down')),
        Repeating(
            Alternatives([
                Sequence(
                    [
                        Trivial(KeyPress(key.UP, 'down')),
                        Trivial(KeyPress(key.UP, 'up')),
                    ],
                    lambda _: change_saturation(0.1)
                ),
                Sequence(
                    [
                        Trivial(KeyPress(key.DOWN, 'down')),
                        Trivial(KeyPress(key.DOWN, 'up')),
                    ],
                    lambda _: change_saturation(-0.1)
                ),
            ])
        )
    ]
)

gestures = [cmd_quit, cmd_change_color, cmd_change_intensity, cmd_change_saturation, cmd_draw_line]
ui = InteractionMachine(gestures)
gl.gl.glLineWidth(2)


@window.event
def on_key_press(key_code: int, modifiers: int):
    ui.handle(KeyPress(key_code, 'down'))


@window.event
def on_key_release(key_code: int, modifiers: int):
    ui.handle(KeyPress(key_code, 'up'))


@window.event
def on_mouse_press(x, y, button, modifiers):
    global ui_state
    ui_state.mouse_position = Point(x, y)

    b = 'left'
    if button == 4:
        b = 'middle'
    elif button == 2:
        b = 'right'

    ui.handle(MousePress(b, 'down'))


@window.event
def on_mouse_release(x, y, button, modifiers):
    global ui_state
    ui_state.mouse_position = Point(x, y)

    b = 'left'
    if button == 4:
        b = 'middle'
    elif button == 2:
        b = 'right'

    ui.handle(MousePress(b, 'up'))


@window.event
def on_mouse_drag(x, y, dx, dy, button, modifier):
    global ui_state
    ui_state.mouse_position = Point(x, y)
    ui.handle(MouseMove())


@window.event 
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global ui_state
    ui_state.mouse_position = Point(x, y)
    ui_state.mouse_scroll = Point(scroll_x, scroll_y)
    ui.handle(MouseScroll())


@window.event
def on_mouse_motion(x, y, button, modifiers):
    global ui_state
    ui_state.mouse_position = Point(x, y)
    ui.handle(MouseMove())


@window.event
def on_draw():
    window.clear()
    label.draw()
    main_batch.draw()

gl.app.run()
