from abc import ABC
from src.classes.multipolygone import MultiPolygone


class Zone(ABC):
    """
    Répresentation d'une délimitation géographique
    """

    def __init__(
        self,
        nom: str,
        mutipolygone: MultiPolygone,
        zone_fille: list["Zone"] | None = None,
    ):

        self._nom = nom
        self._multipolygone = mutipolygone
        self._zone_fille = zone_fille
        self._surface = self.__surface_zone()

    def point_dans_zone(self, point: tuple):
        """
        Determine si un point est dans la zone en utilisant
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
        return self._multipolygone._est_dedans(point)

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
    def multipolygone(self):
        return self._multipolygone

    @property
    def zone_fille(self):
        return self._zone_fille

    @property
    def surface(self):
        return self._surface
