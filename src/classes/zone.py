from abc import ABC
from multipolygone import MultiPolygone


class Zone(ABC):
    """
    Répresentation d'une délimitation géographique
    """

    def __init__(
        self,
        nom: str,
        MultiPolygone: MultiPolygone,
        zone_mere: "Zone" | None = None,
        zone_fille: "Zone" | None = None,
    ):

        self._nom = nom
        self._multi_polygone = MultiPolygone
        self._id_zone_mere = id_zone_mere
        self._id_zone_fille = id_zone_fille
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
        self._multi_polygone._est_dedans(point)

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
        return self._multi_polygone

    @property
    def type_coord(self):
        return self._type_coord

    @property
    def id_zone_mere(self):
        return self._id_zone_mere

    @property
    def id_zone_fille(self):
        return self._id_zone_fille

    @property
    def centre(self):
        return self._centre

    @property
    def surface(self):
        return self._surface
