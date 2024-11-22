from business_object.point import Point


class Contour:
    """
    Classe définissant un contour.
    """

    def __init__(self, points: list[Point], id: int = None) -> None:
        """
        Initialise un contour avecces points dans le bon ordre.

        Parameters
        ----------
        points : list[Point]
            Liste de points dans l'ordre conformant le contour.

        Raises
        ------
        TypeError si points n'est pas une liste de points
        """
        if not isinstance(points, list):
            raise TypeError("points est une liste de Point")

        for point in points:
            if not isinstance(point, Point):
                raise TypeError("points est une liste de Point")

        if not (isinstance(id, int) or id is None):
            raise TypeError("id de type int ou None.")

        self._points = points
        self.__recherche_points_extremums()
        self.id = id

    def __recherche_points_extremums(self):
        """
        Determine les points du plus petit rectangle contenant le contour
        et les enregistre dans l'atribut points_rectangle
        """
        # initialisation des variables
        x_min = y_min = float("inf")
        x_max = y_max = float("-inf")

        for point in self._points:
            x, y = point.x, point.y
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y

        self.__points_rectangle = [x_min, y_min, x_max, y_max]

    def __point_dans_rectangle(self, point: Point) -> bool:
        """
        Determine si un point est dans le plus petit
        rectangle contenant le contour.

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

    def __point_dans_contour(self, point: Point) -> bool:
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

        # Décompose prend les valeurs du point
        x, y = point.x, point.y

        # calcule le nombre de points du polygone
        n = len(self.points)

        if self.points[0] == self.points[-1]:
            n_reg = len(self.points) - 1
        else:
            n_reg = len(self.points)

        # initialisation du flag inside
        dedans = False

        for i in range(n_reg):
            # On prend les coord du premier point et celui qui le suit
            # Rq, j = i + 1 [mod n]
            xi, yi = self.points[i].x, self.points[i].y
            xj, yj = self.points[(i + 1) % n].x, self.points[(i + 1) % n].y

            # On regarde si y est entre yi et yj
            if (yi > y) != (yj > y):
                # On verifie qu'il n'y a pas de divisio par 0

                intersection = (xj - xi) * (y - yi) / (yj - yi) + xi
                if x < intersection:
                    # Inegalité des pentes des droites (P,Pi) vs (Pj, Pi)
                    # Sachant que Pi -> Pj, si Pi_y > Pj_y, comme on sait que
                    # le polygone se trouve à droite de la droite comprise
                    # entre les y_i et Y_j (déjà testé)
                    # Il suffit donc que la pente (P,Pi) > (Pj, Pi)
                    dedans = not dedans
                    # Comme modulo 2, il suffit de changer la valeur de dedans

        return dedans

    def est_dedans(self, point: Point) -> bool:
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

        Raises
        ------
            TypeError si point n'est pas de type Point.
        """
        if not isinstance(point, Point):
            raise TypeError("point doit être de type Point")

        if self.__point_dans_rectangle(point):
            return self.__point_dans_contour(point)

        return False

    def __hash__(self):
        somme_x = sum(round(pt.x * 10e6) * (100003 ^ i) for i, pt in enumerate(self.points))
        somme_y = sum(round(pt.y * 10e6) * (200003 ^ i) for i, pt in enumerate(self.points))
        return (somme_x - somme_y) % 10**8 + 19

    @property
    def points(self) -> list[Point]:
        """
        Retourne la liste de points conformant le contour.

        Returns
        -------
        list[Point]
            liste de points conformant le contour.
        """
        return self._points

    @property
    def coord_rectangle(self) -> list[Point]:
        """
        Retourne le plus petit rectangle contenant le contour sur le
        format : [x_min, y_min, x_max, y_max].

        Returns
        -------
        list[float]
            liste de points conformant le rectangle.
        """
        return self.__points_rectangle
