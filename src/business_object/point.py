class Point:
    def __init__(self, x, y) -> None:
        self._x = x
        self._y = y
    
    @property
    def point(self):
        return self._x, self._y
