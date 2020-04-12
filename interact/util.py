from dataclasses import dataclass


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __add__(self, p: 'Point') -> 'Point':
        return Point(self.x + p.x, self.y + p.y)

    def __sub__(self, p: 'Point') -> 'Point':
        return Point(self.x - p.x, self.y - p.y)
