import pyglet as gl
from pyglet.window import key
from colorsys import *
from interact.gesture_recognizer import *

from examples.pyglet.scaffolding import *

ui = InteractionEngine()
bg = (1.0, 0, 0)
lines: List[Point] = []
main_batch = gl.graphics.Batch()


def change_color():
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


def begin_line():
    lines.append((ui.state.mouse_position, ui.state.mouse_position))
    draw_lines()


def update_line():
    assert lines
    lines[-1] = (lines[-1][0], ui.state.mouse_position)
    draw_lines()


cmd_quit = Trivial(KeyPress(ord('q'), 'up'), lambda: gl.app.exit())
cmd_draw_line = Sequence([
    Trivial(KeyPress(ord('l'), 'down'), begin_line),
    Repeating(Trivial(MouseMove(), update_line)),
    Trivial(KeyPress(ord('l'), 'up')),
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
                    lambda: change_intensity(0.1)
                ),
                Sequence(
                    [
                        Trivial(KeyPress(key.DOWN, 'down')),
                        Trivial(KeyPress(key.DOWN, 'up')),
                    ],
                    lambda: change_intensity(-0.1)
                ),
                Trivial(
                    MouseScroll(),
                    lambda: change_intensity(ui.state.mouse_scroll.y/100.0)
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
                    lambda: change_saturation(0.1)
                ),
                Sequence(
                    [
                        Trivial(KeyPress(key.DOWN, 'down')),
                        Trivial(KeyPress(key.DOWN, 'up')),
                    ],
                    lambda: change_saturation(-0.1)
                ),
            ])
        )
    ]
)

ui.commands = [cmd_quit, cmd_change_color, cmd_change_intensity, cmd_change_saturation, cmd_draw_line]

window = gl.window.Window(resizable=True)
window.on_key_press = on_key_press(ui)
window.on_key_release = on_key_release(ui)
window.on_mouse_press = on_mouse_press(ui)
window.on_mouse_release = on_mouse_release(ui)
window.on_mouse_motion = on_mouse_motion(ui)
window.on_mouse_drag = on_mouse_drag(ui)
window.on_mouse_scroll = on_mouse_scroll(ui)

gl.gl.glLineWidth(2)


@window.event
def on_draw():
    window.clear()
    main_batch.draw()


gl.app.run()
