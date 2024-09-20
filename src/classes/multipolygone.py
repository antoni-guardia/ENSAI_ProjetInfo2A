# Optimisation possible, lors de regarder si le point est dans les exclaves,
# vérifier d'abord s'il est dans le rectangle
class MultiPolygone:
    """
    Répresentation d'un multipolygone
    """

    def __init__(self, contour: list[list[list[tuple]]]):
        """
        Initialisation de la classe MultiPolygone.

        Parameters
        ----------
        contour: list[tuple]
            Ensemble des points conformant les sommets du mutlipolygone.
            Première liste contient l'ensemble des exclaves suivi par ces inclaves.

            E.g. Si P1 est le contour principal, P2 un inclave et P3 un exclave, alors
            contour = [[P1, P2], [P3]] Avec P1 = [(x1, x2), ...]

        """
        if not isinstance(contour, list) or not contour:
            raise TypeError("Contour est de type list[list[list[tuple]]].")

        for anneau in contour:
            if not isinstance(anneau, list) or not anneau:
                raise TypeError("Contour est de type list[list[list[tuple]]].")
            for polygone in anneau:
                if not isinstance(polygone, list) or not polygone:
                    raise TypeError("Contour est de type list[list[list[tuple]]].")
                for point in polygone:
                    if not isinstance(point, tuple):
                        raise TypeError("Contour est de type list[list[list[tuple]]].")

        self.__contour = contour
        self.__cherche_points_rectangle()

    def __cherche_points_rectangle(self):
        """
        Determine les points du plus petit rectangle contenant le multipolygone
        et les enregistre dans l'atribut points_rectangle
        """

        # initialisation des variables
        x_min = y_min = float("inf")
        x_max = y_max = float("-inf")
        # On ne regarde que la figure principale et les exclaves car
        # les inclaves y sont dedans
        for polygone in self.contour:
            polygone = polygone[0]
            for point in polygone:
                x, y = point
                if x < x_min:
                    x_min = x
                if x > x_max:
                    x_max = x
                if y < y_min:
                    y_min = y
                if y > y_max:
                    y_max = y

        self.__points_rectangle = [x_min, y_min, x_max, y_max]

    def __point_dans_rectangle(self, point: tuple):
        """
        Determine si un point est dans le plus petit
        rectangle contenant le multipolygone

        Parameters
        ----------
        point: tuple
            Le point que l'on souhaite tester.

        Returns
        -------
        bool
            Vrai si le point est dedans, faux sinon.
        """

        x, y = point

        return (
            self.points_rectangle[0] <= x <= self.points_rectangle[2]
            and self.points_rectangle[1] <= y <= self.points_rectangle[3]
        )

    def __point_dans_polygone(self, point: tuple, polygone: list[tuple]):
        """
        Determine si un point est dans un polygone en utilisant
        l'algorithme du lancer de rayons.

        Parameters
        ----------
        point: tuple
            Le point que l'on souhaite tester.

        polygone : list[tuple]
            Polygone dont on regarde l'appartnance du point

        Returns
        -------
        bool
            Vrai si le point est dedans, faux sinon.
        """

        # Décompose prend les valeurs du point
        x, y = point

        # calcule le nombre de points du polygone
        n = len(polygone)
        # initialisation du flag inside
        dedans = False

        for i in range(n):
            # On prend les coord du premier point et celui qui le suit
            # Rq, j = i + 1 [mod n]
            xi, yi = polygone[i]
            xj, yj = polygone[(i + 1) % n]

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

    def __point_dans_multipolygone(self, point, multipolygone):
        """
        Determine si un point est dans un multipolygone en utilisant
        la fonction point_dans_polygone

        Parameters
        ----------
        point: tuple
            Le point que l'on souhaite tester.

        multipolygone: list[list[list[tuple]]]
            Multipolygone dont on teste l'appartenance du point

        Returns
        -------
        bool
            Vrai si le point est dedans, faux sinon.
        """
        # On s'assure que le polygone n'est pas vide
        if not multipolygone or not multipolygone[0]:
            return False

        # On selectionne le polynome principale
        multipolygone_principale = multipolygone[0][0]

        # O regarde si le point es dans le multipolygone
        if self.__point_dans_polygone(point, multipolygone_principale):
            # On regarde les inclaves
            inclaves = multipolygone[0][1:]

            # On regarde si le point est dans les inclaves
            for inclave in inclaves:

                if self.__point_dans_polygone(point, inclave):

                    # On s'assure qu'il n'y a pas d'exclave dans l'inclave
                    return self.__point_dans_multipolygone(point, multipolygone[1:])

            # S'il n'y a pas d'inclaves ou n'est pas dans ceux ci, le point est bien dedans
            return True

        # Le point n'est pas dans le polynome principale
        else:
            # On obtient les exclaves
            exclaves = multipolygone[1:]

            # On regarde si le point est dans les exclaves
            for exclave in exclaves:
                if self.__point_dans_polygone(point, exclave[0]):
                    # Si le point est dans l'exclave, on vérifie son appartenance aux inclaves de
                    # l'exclave recursivement
                    return self.__point_dans_multipolygone(point, [exclave])

            return False

    def _est_dedans(self, point: tuple):
        """
        Determine si un point est dans un multipolygone en
        regardant d'abord s'il est dans le plus petit rectangle qui le contient

        Parameters
        ----------
        point: tuple
            Le point que l'on souhaite tester.

        Returns
        -------
        bool
            Vrai si le point est dedans, faux sinon.
        """
        self.__erreur_point(point)
        if self.__point_dans_rectangle(point):
            return self.__point_dans_multipolygone(point, self.contour)

        return False

    def __erreur_point(self, point):
        if not isinstance(point, tuple):
            raise ValueError("Point est de type tuple.")

    # -----------------------------------------------------------------------
    # property methods ------------------------------------------------------
    # -----------------------------------------------------------------------

    @property
    def contour(self):
        """
        Renvoie le contour du multipolygone

        Returns
        -------
            list[list[tuple]]
        """
        return self.__contour

    @property
    def points_rectangle(self):
        """
        Renvoie les points du plus petit rectangle sous la forme
        [x_min, y_min, x_max, y_max]

        Returns
        -------
            list[float]
        """
        return self.__points_rectangle
