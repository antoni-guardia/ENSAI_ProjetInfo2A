from business_object.point import Point as P
from business_object.zonage import Zonage
from business_object.zone import Zone

from dao.zonage_dao import ZonageDAO


class ServicesRecherchePoint:

    def trouver_zone_point(
        self, nom_zonage: str, annee: int, x: float, y: float, type_coord: str = None
    ):
        point = P(x, y)
        zonage = ZonageDAO().trouver_id_par_nom_annee(nom_zonage, annee)
        if not isinstance(zonage, Zonage):
            return None
        zone = zonage.trouver_zone(point)
        if not isinstance(zone, Zone):
            return None
        return zone.nom

    def trouver_chemin_zones_point(
        self, nom_zonage: str, annee: int, x: float, y: float, type_coord: str = None
    ):
        point = P(x, y)
        zonage = ZonageDAO().trouver_id_par_nom_annee(nom_zonage, annee)

        if not isinstance(zonage, Zonage):
            return None

        zones_path = zonage.trouver_zone_chemin(point)

        if not isinstance(zones_path, str) or zones_path == "":
            return None
        return zones_path

    def trouver_multiple_zone_point(
        self, nom_zonage: str, annee: int, liste_points: list[tuple], type_coord=None
    ):
        liste_aux = []
        for x, y in liste_points:
            liste_aux.append(self.trouver_zone_point(nom_zonage, annee, x, y, type_coord))

        return liste_aux
