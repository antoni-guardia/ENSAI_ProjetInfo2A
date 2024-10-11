from src.business_object.contour import Contour

class Polygone:
    def __init__(self, contour: Contour) -> None:
        self.contour = contour

    def est_dedans(self, point: tuple) -> bool:
        """
        Vérifier qu'un point est à l'intérieur d'un polygone à l'aide de la classe Contour.
        :param point: Un tuple (x, y) représentant le point.
        :return: Vrai si le point est dedant, et faux sinon
        """
        return self.contour.est_dedans(point)

    def recherche_point_extremum(self):
        """
        Recherche le maximum et minimum d'un point
        :return: Un dictionnaire contenant les extremums.
        """
        points = self.contour.points()
        min_x = min(point[0] for point in points)
        max_x = max(point[0] for point in points)
        min_y = min(point[1] for point in points)
        max_y = max(point[1] for point in points)
 
        return {
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y
        }

    def point_dans_rectangle(self, point: tuple) -> bool:
        """
        Vérifier si le point est dans le rectangle
        :param point: Un tuple (x, y) représentant le point.
        :return: Vrai si le point est dans le rectangle, Faux sinon
        """
        extremum = self.recherche_point_extremum()
        x, y = point
        return (extremum['min_x'] <= x <= extremum['max_x']) and (extremum['min_y'] <= y <= extremum['max_y'])
