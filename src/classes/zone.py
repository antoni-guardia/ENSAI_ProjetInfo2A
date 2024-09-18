from abc import ABC
from multipolygone import MultiPolygone


class Zone(ABC):
    """
    Répresentation d'une délimitation géographique
    """

    def __init__(self,
                 nom: str,
                 MultiPolygone: MultiPolygone,
                 zone_mere: "Zone" | None = None,
                 zone_fille: "Zone" | None = None):

        self._nom = nom
        self._MultiPolygone = MultiPolygone
        self._zone_mere = zone_mere
        self._zone_fille = zone_fille
        self._surface = self.__surface_zone()

    def point_dans_poly(self,
                        polygone: MultiPolygone,
                        point: tuple):
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

    def point_dans_zone(self,
                        point: tuple):
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

    def __surface_zone(self):
        """
        Determine la surface de la zone en km².

        Returns
        -------
        float
            Surface de la zone en km²
        """
        pass

    # -----------------------------------------------------------------------
    # property methods ------------------------------------------------------
    # -----------------------------------------------------------------------

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
