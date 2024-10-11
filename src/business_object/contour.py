from Point import Point


class Contour:
    """
    Classe définissant le contour, indique l'ensemble
    de points qui doivent être reliés pour dessiner un contour

    Attributs
    ----------
    point : Liste
        point
    """
    def __init__(self, points: list[Point]) -> None:
        self.points = points

    def est_dedans(self, point: tuple[float, float]) -> bool:
        pass
