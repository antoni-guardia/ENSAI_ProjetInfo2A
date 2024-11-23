import copy as c
from business_object.point import Point as P
from business_object.zonage import Zonage
from business_object.zone import Zone

from dao.zonage_dao import ZonageDAO
from dao.zone_dao import ZoneDAO


class ServicesRecherchePoint:

    def trouver_zone_point(
        self, nom_zonage: str, x: float, y: float, annee, type_coord: str = None
    ):
        recherche_indirecte = False
        if nom_zonage in ["REGION", "DEPARTEMENT"]:
            vrai_nom_zonage = c.copy(nom_zonage)
            nom_zonage = "COMMUNE"
            recherche_indirecte = True

        point = P(x, y)
        id_zonage = ZonageDAO().trouver_id_par_nom_annee(nom_zonage, annee)
        if id_zonage is not None:
            id_zones_possibles = ZoneDAO().trouver_id_zones_par_rectangles(x, y, id_zonage)

        else:
            return None

        if id_zones_possibles is not None:
            for id_zone in id_zones_possibles:
                zone = ZoneDAO().trouver_par_id(id_zone, False)
                if isinstance(zone, Zone):
                    if zone.point_dans_zone(point):
                        if not recherche_indirecte:
                            return zone.nom

                        id_departement = ZoneDAO().trouver_id_mere(id_zone)
                        if vrai_nom_zonage == "DEPARTEMENT":
                            return ZoneDAO().trouver_nom_par_id(id_departement)

                        id_region = ZoneDAO().trouver_id_mere(id_zone)
                        return ZoneDAO().trouver_nom_par_id(id_region)

        return None

    def trouver_chemin_zones_point(
        self, nom_zonage: str, x: float, y: float, type_coord: str = None
    ):
        point = P(x, y)
        zonage = ZonageDAO().trouver_id_par_nom_annee(nom_zonage)

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


if __name__ == "__main__":
    print(ServicesRecherchePoint().trouver_zone_point("DEPARTEMENT", 5.85, 43.82,2003)) 
