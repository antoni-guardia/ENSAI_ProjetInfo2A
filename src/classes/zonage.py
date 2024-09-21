from zone import Zone


class Zonage:
    """
    Répresentation d'un découpage géographique.
    """

    def __init__(
        self,
        nom: str,
        zones: list[Zone],
        annee: int,
        zonage_fille: "Zonage" | None = None,
    ):
        """
        Initialisation de la classe zonage.

        Parameters
        ----------
        nom: str
            Nom du zonage.

        zones: list[Zone]
            Ensemble de zones qui constituent le zonage

        annee: int
            Année de publication du découpage.

        zonage_fille: Zonage | None
            Le découpage de niveau inférieur auquel appartient le zonage actuel.

        """

        self._nom = nom
        self._zones = zones
        self._annee = annee
        self._zonage_fille = zonage_fille

    def trouver_zone(self, point: tuple, type_coord: str | None = None):
        """
        Fonction qui renvoie la zone d'appartenance d'un point en
        fonction de son type de coordonnées.

        Parameters
        ----------
        point: str
            Point dont on veut connaitre la zone.

        type_coord: str | None
            Type de coordonnées du point rentré.
            None si type GPS.

        Returns
        -------
        Zone
            La zone où appartient le point.
        """

        pass

    # -----------------------------------------------------------------------
    # property methods ------------------------------------------------------
    # -----------------------------------------------------------------------

    @property
    def nom(self):
        return self._nom

    @property
    def type_coord(self):
        return self._type_coord

    @property
    def zones(self):
        return self.zones

    @property
    def annee(self):
        return self.annee

    @property
    def zonage_fille(self):
        return self.zonage_fille
