from src.classes.zone import Zone


class Zonage:
    """
    Répresentation d'un découpage géographique.
    """

    def __init__(
        self,
        nom: str,
        zones: list[Zone],
        annee: int,
        zonage_mere: "Zonage" = None,
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

        zonage_mere: Zonage | None
            Le découpage de niveau supérieur auquel appartient le zonage actuel.

        """

        self._nom = nom
        self._zones = zones
        self._annee = annee
        self._zonage_mere = zonage_mere

    def trouver_zone(self,
                     point: tuple,
                     type_coord: str | None = None):
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
            None s'il n'y a pas de zone d'appartenance.
        """
        if type_coord is not None:
            # coder ou appeler fonction changement coords
            pass

        if self.zonage_mere is None:
            for zone in self.zones:
                if zone.point_dans_zone(point):

                    return zone
        else:
            zone_mere = self.zonage_mere.trouver_zone(point)

            if zone_mere is not None:
                for zone in zone_mere.zone_fille:
                    if zone.point_dans_zone(point):

                        return zone

        return None

    # -----------------------------------------------------------------------
    # property methods ------------------------------------------------------
    # -----------------------------------------------------------------------

    @property
    def nom(self):
        return self._nom

    @property
    def zones(self):
        return self._zones

    @property
    def annee(self):
        return self.annee

    @property
    def zonage_mere(self):
        return self._zonage_mere
