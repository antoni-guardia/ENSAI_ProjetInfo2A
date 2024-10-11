from Point import Point


class Contour:
    """
    Classe définissant le contour, indique
    si un point est à l'intérieur du contour ou non

    Attributs
    ----------
    point : Liste
        point
    """
    def __init__(self, points: list[Point]) -> None:
        self.points = points

    def est_dedans(self, point: tuple[float, float]) -> bool:
        pass
