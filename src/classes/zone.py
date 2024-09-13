class zone:
    """
    Répresentation d'une délimitation géographique
    """

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self,
                 nom,
                 type_coord,
                 MultiPolygone,
                 zone_mere=None,
                 zone_fille=None):
        # -----------------------------
        # Attributes
        # -----------------------------

        self._nom: str = nom
        self._MultiPolygone: list(tuple) = MultiPolygone
        self._type_coord: str = type_coord
        self._zone_mere = zone_mere
        self._zone_fille = zone_fille
        self._centre = self.__centre_multipolygone()
        self._surface = self.__surface_multipolygone()

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def point_dans_poly(self, polygone, point):
        """
        Determine si un point est dans un polygone en utilisant
        l'algorithme du lancer de rayons.

        Parameters
        ----------
        point : tuple
            Le point que l'on souhaite tester.

        polygon : list[tuple]
            Liste de tuples représentant les sommets du polygone.

        Returns
        -------
        bool
            Vrai si le point est dedans, faux sinon.
        """
        # prend les valeurs du point
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

    def point_dans_zone(self, point):
        """
        Determine si un point est dans la zone en utilisant
        l'algorithme du lancer de rayons.

        Parameters
        ----------
        point : tuple
            Le point que l'on souhaite tester.

        Returns
        -------
        bool
            Vrai si le point est dedans, faux sinon.
        """
        pass

    def __centre_multipolygone(self):
        pass

    def __surface_mulipolygone(self):
        pass

    @property
    def nom(self):
        return self._nom

    @property
    def MultiPolygone(self):
        return self._MultiPolygone

    @property
    def type_coord(self):
        return self._type_coord

    @property
    def zone_mere(self):
        return self._zone_mere

    @property
    def zone_fille(self):
        return self._zone_fille

    @property
    def centre(self):
        return self._centre

    @property
    def surface(self):
        return self._surface
