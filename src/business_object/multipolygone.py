from business_object.polygone import Polygone
from business_object.point import Point


class MultiPolygone:

    """
    Classe définissant un multipolygone.
    """

    def __init__(self, polygones: list[Polygone], id: int = None):
        """
        Initialisation de la classe MultiPolygone.

        Parameters
        ----------
        polygones: list[tuple]
            Ensemble des polygones conformant le multipolygone.
            Le premier sera dit polygone principale, et les autres seront ces exclaves


        Raises
        ------
            TypeError si polygones n'est pas une liste de polygones.

        """
        if not isinstance(polygones, list):
            raise TypeError("polygones est une liste de contour.")

        for polygone in polygones:
            if not isinstance(polygone, Polygone):
                raise TypeError("polygones est une liste de contour.")

        if not (isinstance(id, int) or id is None):
            raise TypeError("id de type int ou None.")

        self._polygones = polygones
        self.__recherche_points_extremums()
        self.id = id

    def __recherche_points_extremums(self):
        """
        Determine les points du plus petit rectangle contenant le multipolygone
        et les enregistre dans l'atribut points_rectangle
        """
        # initialisation des variables
        x_min = y_min = float("inf")
        x_max = y_max = float("-inf")

        for polygone in self.polygones:
            x_p_min, y_p_min, x_p_max, y_p_max = polygone.coord_rectangle
            if x_p_min < x_min:
                x_min = x_p_min
            if x_p_max > x_max:
                x_max = x_p_max
            if y_p_min < y_min:
                y_min = y_p_min
            if y_p_max > y_max:
                y_max = y_p_max

        self.__points_rectangle = [x_min, y_min, x_max, y_max]

    def __point_dans_rectangle(self, point: Point) -> bool:
        """
        Determine si un point est dans le plus petit
        rectangle contenant le multipolygone.

        Parameters
        ----------
        point: Point
            Le point que l'on souhaite tester.

        Returns
        -------
        bool
            Vrai si le point est dedans, faux sinon.
        """

        return (
            self.coord_rectangle[0] <= point.x <= self.coord_rectangle[2]
            and self.coord_rectangle[1] <= point.y <= self.coord_rectangle[3]
        )

    def __point_dans_multipolygone(self, point: Point) -> bool:
        """
        Determine si un point est dans un contour en utilisant
        l'algorithme du lancer de rayons.

        Parameters
        ----------
        point: tuple
            Le point que l'on souhaite tester.

        Returns
        -------
        bool
            Vrai si le point est dedans, faux sinon.
        """

        for polygone in self.polygones:

            if polygone.est_dedans(point):
                # point dans le polygone principal ou exclave.
                return True

        # point n'est pas dans multipolygone
        return False

    def est_dedans(self, point: Point) -> bool:
        """
        Determine si un point est dans un polygone en utilisant
        l'algorithme du lancer de rayons.

        Parameters
        ----------
        point: tuple
            Le point que l'on souhaite tester.

        Returns
        -------
        bool
            Vrai si le point est dedans, faux sinon.

        Raises
        ------
            TypeError si point n'est pas de type Point.
        """

        if not isinstance(point, Point):
            raise TypeError("point doit être de type Point")

        if self.__point_dans_rectangle(point):
            return self.__point_dans_multipolygone(point)

        return False

    def __iter__(self):
        return iter(self.polygones)

    @property
    def polygones(self):
        """
        Renvoie la liste de polygones conformant le multipolygone

        Returns
        -------
            list[polygone]
        """
        return self._polygones

    @property
    def coord_rectangle(self) -> list[float]:
        """
        Retourne le plus petit rectangle contenant le multipolygone sur le
        format : [x_min, y_min, x_max, y_max].

        Returns
        -------
        list[float]
            liste de points conformant le rectangle.
        """
        return self.__points_rectangle
