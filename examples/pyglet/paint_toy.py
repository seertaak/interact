import pyglet as gl
from colorsys import *
from interact.sugar import *
from typing import Tuple
from math import sqrt, pi, sin, cos

from examples.pyglet.scaffolding import *

ui = InteractionEngine()
bg = (1.0, 0, 0)
lines: List[Point] = []
circles: List[Tuple[Point, float]] = []
p0 = Point(0, 0)


def set_initial_pos():
    global p0
    p0 = ui.state.mouse_position


def translate(drag=True):
    global lines
    global circles
    global p0
    d_pos = ui.state.mouse_position - p0 if drag else ui.state.mouse_scroll
    lines = [[point + d_pos for point in line] for line in lines]
    circles = [(circle[0] + d_pos, circle[1]) for circle in circles]
    p0 = ui.state.mouse_position


def change_bg(d_hue = 0.0, d_sat = 0.0, d_val = 0.0):
    global bg
    h, s, v = rgb_to_hsv(*bg)
    h += d_hue
    s += d_sat
    v += d_val
    bg = hsv_to_rgb(h, s, v)
    args = list(bg)
    args.append(1.0)
    gl.gl.glClearColor(*args)


def draw_shapes():
    global lines
    global circles
    main_batch = gl.graphics.Batch()
    for o, r in circles:
        steps = 50
        coords = []

        for i in range(0, steps):
            angle = i/steps*2*pi
            coords.append(o.x + r*cos(angle))
            coords.append(o.y + r*sin(angle))

            coords.append(coords[-2])
            coords.append(coords[-2])

        coords.extend([coords[0], coords[1]])

        main_batch.add(
            2*steps,
            gl.gl.GL_LINES,
            None,
            ('v2f', coords[2:]),
            ('c3B', [255, 255, 255, 255, 255, 255]*steps))


    for line in lines:
        main_batch.add(
            2,
            gl.gl.GL_LINES,
            None,
            ('v2f', (line[0].x, line[0].y, line[1].x, line[1].y)),
            ('c3B', (255, 255, 255, 255, 255, 255))
        )
    main_batch.draw()


def begin_line():
    global lines
    lines.append((ui.state.mouse_position, ui.state.mouse_position))


def update_line():
    global lines
    assert lines
    lines[-1] = (lines[-1][0], ui.state.mouse_position)


def begin_circle():
    global circles
    circles.append((ui.state.mouse_position, 1))


def update_circle():
    global circles
    assert circles
    origin = circles[-1][0]
    mouse = ui.state.mouse_position
    r = sqrt((mouse.x - origin.x)**2 + (mouse.y - origin.y)**2)
    circles[-1] = (origin, r)
    on_draw()
    window.flip()


number = None


def push_number(i: int):
    def fn():
        global number
        if number is not None:
            number = number*10 + i
        else:
            number = i
        print(number)
    return fn


def reset_number():
    global number
    number = None


number_recognizer = [Key(48 + i, str(i))[push_number(i)] for i in range(0, 10)]
ui.commands = [
    Q[gl.app.exit],
    (gr.Alternatives(number_recognizer) - T[lambda: gl.gl.glLineWidth(number)])[reset_number].ignore_key_up,
    L[begin_line] + MOUSE_MOVE[update_line].repeat,
    C[begin_circle] + MOUSE_MOVE[update_circle].repeat,
    BACKSPACE - BACKSPACE[lambda: (circles.clear(), lines.clear())],
    B - D[lambda: change_bg(d_hue=0.05)].repeat,
    I + ( MOUSE_SCROLL[lambda: change_bg(d_val=ui.state.mouse_scroll.y / 100.0)]
        | UP[lambda: change_bg(d_val=0.1)]
        | DOWN[lambda: change_bg(d_val=-0.1)]
        ).repeat,
    S + ( MOUSE_SCROLL[lambda: change_bg(d_sat=ui.state.mouse_scroll.y / 100.0)]
        | UP[lambda: change_bg(d_sat=0.1)]
        | DOWN[lambda: change_bg(d_sat=-0.1)]
        ).repeat,
    MOUSE_DOWN[set_initial_pos] - MOUSE_MOVE[translate].repeat_until(MOUSE_UP)
]

window = gl.window.Window(resizable=True, vsync=False)

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
    draw_shapes()


gl.app.run()
