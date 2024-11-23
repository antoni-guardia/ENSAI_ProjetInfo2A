from business_object.zone import Zone
from business_object.point import Point as P


class Zonage:
    """
    Répresentation d'un découpage géographique.
    """

    def __init__(self, nom: str, zones: list[Zone], zonage_mere: "Zonage" = None, id: int = None):
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
        self._zonage_mere = zonage_mere

        if not (isinstance(id, int) or id is None):
            raise TypeError("id de type int ou None.")

        self.id = id

    def trouver_zone(self, point: P):
        """
        Fonction qui renvoie la zone d'appartenance d'un point en
        fonction de son type de coordonnées.

        Parameters
        ----------
        point: Point
            Point dont on veut connaitre la zone.

        Returns
        -------
        Zone
            La zone où appartient le point.
            None s'il n'y a pas de zone d'appartenance.
        """
        self.__erreur_point(point)

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

    def trouver_zone_chemin(self, point: P):
        """
        Fonction qui renvoie le chemin des zones d'appartenance d'un point en
        fonction de son type de coordonnées.

        Parameters
        ----------
        point: Point
            Point dont on veut connaitre la zone.

        Returns
        -------
        str
            Le chemin des zones où appartient le point.
            "" s'il n'y a pas de zone d'appartenance.
        """
        self.__erreur_point(point)

        if self.zonage_mere is None:
            for zone in self.zones:
                if zone.point_dans_zone(point):

                    return zone.nom
        else:

            zone_mere = self.zonage_mere.trouver_zone(point)

            if zone_mere is not None:
                for zone in zone_mere.zone_fille:
                    if zone.point_dans_zone(point):

                        return self.zonage_mere.trouver_zone_chemin() + "/" + zone.nom

        return ""

    def __erreur_point(self, point):
        """
        Detecte si un point est de type tuple.

        Parameters
        ----------
        point: tuple
            Le point que l'on souhaite tester.

        Raises
        ------
            ValueError si point n'est pas un tuple.
        """
        if not isinstance(point, P):
            raise TypeError("point est de type Point.")

    # -----------------------------------------------------------------------
    # property methods ------------------------------------------------------
    # -----------------------------------------------------------------------
    # not tested
    @property
    def nom(self):
        return self._nom

    @property
    def zones(self):
        return self._zones

    @property
    def zonage_mere(self):
        return self._zonage_mere
