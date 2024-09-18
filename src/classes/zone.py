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

    def point_dans_zone(self,
                        point: tuple):
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
