from dataclasses import dataclass
from copy import deepcopy
from typing import Callable, List, Literal
from interact import gesture_recognizer as gr
from interact import abstract_event as ae
from pyglet.window import key


class Key(gr.Recognizer):
    def __init__(self, key: int, symbol: str):
        super().__init__()
        self.key = key
        self.symbol = symbol

    @property
    def down(self):
        return gr.Trivial(ae.KeyPress(self.key, 'down'), self.handler)

    @property
    def up(self):
        return gr.Trivial(ae.KeyPress(self.key, 'up'), self.handler)

    def recognize(self, event: gr.Event) -> gr.State:
        return self.down.recognize(event)

    def __sub__(self, other):
        copy = deepcopy(self)
        return KeySequence([copy, other])

    def __add__(self, other):
        def ignore_fn(e: ae.Event):
            if not isinstance(e, ae.KeyPress) or e.action != 'up':
                return False
            return e.key != self.key

        return self.down[self.handler] - gr.IgnoreIf(ignore_fn, deepcopy(other)) - self.up[gr.default_handler]


class KeySequence(gr.Recognizer):
    def __init__(self, steps: List[gr.Recognizer], handler: gr.Handler = gr.default_handler):
        self.recognizer = gr.IgnoreIf(
            lambda e: e.action == 'up',
            gr.Sequence([step.down if isinstance(step, Key) else step for step in steps]),
            handler
        )

    def recognize(self, event: gr.Event) -> gr.State:
        return self.recognizer.recognize(event)

    def __sub__(self, other: gr.Recognizer):
        copy = deepcopy(self)
        copy.recognizer.gesture.gestures.append(other)
        return copy


MOUSE_DOWN = gr.Trivial(ae.MousePress('left', 'down'))
MOUSE_UP = gr.Trivial(ae.MousePress('left', 'up'))
RIGHT_MOUSE_DOWN = gr.Trivial(ae.MousePress('right', 'down'))
RIGHT_MOUSE_UP = gr.Trivial(ae.MousePress('right', 'up'))
MIDDLE_MOUSE_DOWN = gr.Trivial(ae.MousePress('middle', 'down'))
MIDDLE_MOUSE_UP = gr.Trivial(ae.MousePress('middle', 'up'))
MOUSE_MOVE = gr.Trivial(ae.MouseMove())
MOUSE_SCROLL = gr.Trivial(ae.MouseScroll())

if False:
    for v, k in key._key_names.items():
        print(f"{k.upper()} = Key({v}, '{k.upper()}')")

BACKSPACE = Key(65288, 'BACKSPACE')
TAB = Key(65289, 'TAB')
LINEFEED = Key(65290, 'LINEFEED')
CLEAR = Key(65291, 'CLEAR')
ENTER = Key(65293, 'ENTER')
PAUSE = Key(65299, 'PAUSE')
SCROLLLOCK = Key(65300, 'SCROLLLOCK')
SYSREQ = Key(65301, 'SYSREQ')
ESCAPE = Key(65307, 'ESCAPE')
SPACE = Key(32, 'SPACE')
HOME = Key(65360, 'HOME')
LEFT = Key(65361, 'LEFT')
UP = Key(65362, 'UP')
RIGHT = Key(65363, 'RIGHT')
DOWN = Key(65364, 'DOWN')
PAGEUP = Key(65365, 'PAGEUP')
PAGEDOWN = Key(65366, 'PAGEDOWN')
END = Key(65367, 'END')
BEGIN = Key(65368, 'BEGIN')
DELETE = Key(65535, 'DELETE')
SELECT = Key(65376, 'SELECT')
PRINT = Key(65377, 'PRINT')
EXECUTE = Key(65378, 'EXECUTE')
INSERT = Key(65379, 'INSERT')
UNDO = Key(65381, 'UNDO')
REDO = Key(65382, 'REDO')
MENU = Key(65383, 'MENU')
FIND = Key(65384, 'FIND')
CANCEL = Key(65385, 'CANCEL')
HELP = Key(65386, 'HELP')
BREAK = Key(65387, 'BREAK')
SCRIPTSWITCH = Key(65406, 'SCRIPTSWITCH')
FUNCTION = Key(65490, 'FUNCTION')
NUMLOCK = Key(65407, 'NUMLOCK')
NUM_SPACE = Key(65408, 'NUM_SPACE')
NUM_TAB = Key(65417, 'NUM_TAB')
NUM_ENTER = Key(65421, 'NUM_ENTER')
NUM_F1 = Key(65425, 'NUM_F1')
NUM_F2 = Key(65426, 'NUM_F2')
NUM_F3 = Key(65427, 'NUM_F3')
NUM_F4 = Key(65428, 'NUM_F4')
NUM_HOME = Key(65429, 'NUM_HOME')
NUM_LEFT = Key(65430, 'NUM_LEFT')
NUM_UP = Key(65431, 'NUM_UP')
NUM_RIGHT = Key(65432, 'NUM_RIGHT')
NUM_DOWN = Key(65433, 'NUM_DOWN')
NUM_PAGE_UP = Key(65434, 'NUM_PAGE_UP')
NUM_PAGE_DOWN = Key(65435, 'NUM_PAGE_DOWN')
NUM_END = Key(65436, 'NUM_END')
NUM_BEGIN = Key(65437, 'NUM_BEGIN')
NUM_INSERT = Key(65438, 'NUM_INSERT')
NUM_DELETE = Key(65439, 'NUM_DELETE')
NUM_EQUAL = Key(65469, 'NUM_EQUAL')
NUM_MULTIPLY = Key(65450, 'NUM_MULTIPLY')
NUM_ADD = Key(65451, 'NUM_ADD')
NUM_SEPARATOR = Key(65452, 'NUM_SEPARATOR')
NUM_SUBTRACT = Key(65453, 'NUM_SUBTRACT')
NUM_DECIMAL = Key(65454, 'NUM_DECIMAL')
NUM_DIVIDE = Key(65455, 'NUM_DIVIDE')
NUM_0 = Key(65456, 'NUM_0')
NUM_1 = Key(65457, 'NUM_1')
NUM_2 = Key(65458, 'NUM_2')
NUM_3 = Key(65459, 'NUM_3')
NUM_4 = Key(65460, 'NUM_4')
NUM_5 = Key(65461, 'NUM_5')
NUM_6 = Key(65462, 'NUM_6')
NUM_7 = Key(65463, 'NUM_7')
NUM_8 = Key(65464, 'NUM_8')
NUM_9 = Key(65465, 'NUM_9')
F1 = Key(65470, 'F1')
F2 = Key(65471, 'F2')
F3 = Key(65472, 'F3')
F4 = Key(65473, 'F4')
F5 = Key(65474, 'F5')
F6 = Key(65475, 'F6')
F7 = Key(65476, 'F7')
F8 = Key(65477, 'F8')
F9 = Key(65478, 'F9')
F10 = Key(65479, 'F10')
F11 = Key(65480, 'F11')
F12 = Key(65481, 'F12')
F13 = Key(65482, 'F13')
F14 = Key(65483, 'F14')
F15 = Key(65484, 'F15')
F16 = Key(65485, 'F16')
F17 = Key(65486, 'F17')
F18 = Key(65487, 'F18')
F19 = Key(65488, 'F19')
F20 = Key(65489, 'F20')
LSHIFT = Key(65505, 'LSHIFT')
RSHIFT = Key(65506, 'RSHIFT')
LCTRL = Key(65507, 'LCTRL')
RCTRL = Key(65508, 'RCTRL')
CAPSLOCK = Key(65509, 'CAPSLOCK')
LMETA = Key(65511, 'LMETA')
RMETA = Key(65512, 'RMETA')
LALT = Key(65513, 'LALT')
RALT = Key(65514, 'RALT')
LWINDOWS = Key(65515, 'LWINDOWS')
RWINDOWS = Key(65516, 'RWINDOWS')
LCOMMAND = Key(65517, 'LCOMMAND')
RCOMMAND = Key(65518, 'RCOMMAND')
LOPTION = Key(65519, 'LOPTION')
ROPTION = Key(65520, 'ROPTION')
EXCLAMATION = Key(33, 'EXCLAMATION')
DOUBLEQUOTE = Key(34, 'DOUBLEQUOTE')
POUND = Key(35, 'POUND')
DOLLAR = Key(36, 'DOLLAR')
PERCENT = Key(37, 'PERCENT')
AMPERSAND = Key(38, 'AMPERSAND')
APOSTROPHE = Key(39, 'APOSTROPHE')
PARENLEFT = Key(40, 'PARENLEFT')
PARENRIGHT = Key(41, 'PARENRIGHT')
ASTERISK = Key(42, 'ASTERISK')
PLUS = Key(43, 'PLUS')
COMMA = Key(44, 'COMMA')
MINUS = Key(45, 'MINUS')
PERIOD = Key(46, 'PERIOD')
SLASH = Key(47, 'SLASH')
_0 = Key(48, '_0')
_1 = Key(49, '_1')
_2 = Key(50, '_2')
_3 = Key(51, '_3')
_4 = Key(52, '_4')
_5 = Key(53, '_5')
_6 = Key(54, '_6')
_7 = Key(55, '_7')
_8 = Key(56, '_8')
_9 = Key(57, '_9')
COLON = Key(58, 'COLON')
SEMICOLON = Key(59, 'SEMICOLON')
LESS = Key(60, 'LESS')
EQUAL = Key(61, 'EQUAL')
GREATER = Key(62, 'GREATER')
QUESTION = Key(63, 'QUESTION')
AT = Key(64, 'AT')
BRACKETLEFT = Key(91, 'BRACKETLEFT')
BACKSLASH = Key(92, 'BACKSLASH')
BRACKETRIGHT = Key(93, 'BRACKETRIGHT')
ASCIICIRCUM = Key(94, 'ASCIICIRCUM')
UNDERSCORE = Key(95, 'UNDERSCORE')
QUOTELEFT = Key(96, 'QUOTELEFT')
A = Key(97, 'A')
B = Key(98, 'B')
C = Key(99, 'C')
D = Key(100, 'D')
E = Key(101, 'E')
F = Key(102, 'F')
G = Key(103, 'G')
H = Key(104, 'H')
I = Key(105, 'I')
J = Key(106, 'J')
K = Key(107, 'K')
L = Key(108, 'L')
M = Key(109, 'M')
N = Key(110, 'N')
O = Key(111, 'O')
P = Key(112, 'P')
Q = Key(113, 'Q')
R = Key(114, 'R')
S = Key(115, 'S')
T = Key(116, 'T')
U = Key(117, 'U')
V = Key(118, 'V')
W = Key(119, 'W')
X = Key(120, 'X')
Y = Key(121, 'Y')
Z = Key(122, 'Z')
BRACELEFT = Key(123, 'BRACELEFT')
BAR = Key(124, 'BAR')
BRACERIGHT = Key(125, 'BRACERIGHT')
ASCIITILDE = Key(126, 'ASCIITILDE')

