from business_object.contour import Contour
from business_object.point import Point


class Polygone:

    """
    Classe définissant un polygone.
    """

    def __init__(self, contours: list[Contour], id: int = None) -> None:
        """
        Initialise un polygone avec ces liste de contours.
        Le premier contour reprèsente la forme principale, le reste ce sont
        des enclaves ("trous").

        Parameters
        ----------
        points : list[Contour]
            Liste de contour dans l'ordre conformant le polygone.

        Raises
        ------
        TypeError si contours n'est pas une liste de contours
        """

        if not isinstance(contours, list):
            raise TypeError("contours est une liste de contour")

        for contour in contours:
            if not isinstance(contour, Contour):
                raise TypeError("contours est une liste de contour")

        if not (isinstance(id, int) or id is None):
            raise TypeError("id de type int ou None.")

        self._contours = contours
        self.__recherche_points_extremums()
        self.id = id

    def __recherche_points_extremums(self):
        """
        Determine les points du plus petit rectangle contenant le polygone
        et les enregistre dans l'atribut points_rectangle
        """
        # initialisation des variables
        x_min = y_min = float("inf")
        x_max = y_max = float("-inf")

        for contour in self.contours:
            x_c_min, y_c_min, x_c_max, y_c_max = contour.coord_rectangle
            if x_c_min < x_min:
                x_min = x_c_min
            if x_c_max > x_max:
                x_max = x_c_max
            if y_c_min < y_min:
                y_min = y_c_min
            if y_c_max > y_max:
                y_max = y_c_max

        self.__points_rectangle = [x_min, y_min, x_max, y_max]

    def __point_dans_rectangle(self, point: Point) -> bool:
        """
        Determine si un point est dans le plus petit
        rectangle contenant le polygone.

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

    def __point_dans_polygone(self, point: Point) -> bool:
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

        # On regarde si le point est dans le contour principal

        if self.contours[0].est_dedans(point):
            # Si c'est le cas, on vérifie qu'il n'est pas dans une enclave
            for enclave in self.contours[1:]:
                if enclave.est_dedans(point):
                    # point dans une enclave
                    return False
            # point dans le polygone
            return True
        # point pas dnas le contour principal
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
            return self.__point_dans_polygone(point)

        return False

    def __hash__(self):

        FACTOR = 2017
        MOD = 173993
        print(sum(hash(contour) * FACTOR for contour in self.contours) % MOD)
        return sum(hash(contour) * FACTOR for contour in self.contours) % MOD

    @property
    def contours(self) -> list[Contour]:
        """
        Retourne la liste de contours conformant le polygone.

        Returns
        -------
        list[Contour]
            liste de contours conformant le polygone.
        """
        return self._contours

    @property
    def coord_rectangle(self) -> list[float]:
        """
        Retourne le plus petit rectangle contenant le polygone sur le
        format : [x_min, y_min, x_max, y_max].

        Returns
        -------
        list[float]
            liste de points conformant le rectangle.
        """
        return self.__points_rectangle
