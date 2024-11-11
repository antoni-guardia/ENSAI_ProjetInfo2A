from abc import ABC
from business_object.multipolygone import MultiPolygone


class Zone(ABC):
    """
    Répresentation d'une délimitation géographique
    """

    def __init__(
        self,
        nom: str,
        mutipolygone: MultiPolygone,
        population: int = None,
        code_insee: int = None,
        annee: int = None,
        zones_fille: list["Zone"] | None = None,
        id: int = None,
    ):

        self._nom = nom
        self._multipolygone = mutipolygone
        self._zones_fille = zones_fille
        self.population = population
        self.annee = annee
        self.code_insee = code_insee
        self._surface = self.__surface_zone()

        if not (isinstance(id, int) or id is None):
            raise TypeError("id de type int ou None.")

        self.id = id

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
        return self._multipolygone.est_dedans(point)

    def __surface_zone(self):
        """
        Determine la surface de la zone en km².

        Returns
        -------
        float
            Surface de la zone en km²
        """
        pass

    def __hash__(self):

        return hash(self.multipolygone)
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
    def zones_fille(self):
        return self._zones_fille

    @property
    def surface(self):
        return self._surface
