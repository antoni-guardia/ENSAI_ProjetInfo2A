import copy as c
from business_object.point import Point as P
from business_object.zone import Zone

from dao.zonage_dao import ZonageDAO
from dao.zone_dao import ZoneDAO
from utils.transformateur_coord import TransformerCoordonnees


class ServicesRecherchePoint:

    def trouver_zone_point(
        self,
        nom_zonage: str,
        x: float,
        y: float,
        annee: int,
        type_coord: str = None,
        id_return: bool = False,
    ):
        """
        Trouve la zone d'appartenance du point (x, y) dans une année particuliere
        tout en especifiant dans quel systeme de coordonnées il appartient.

        Parameters
        ----------

        nom_zonage : str
            nom du zonage dont on fait la requete.

        x : float
            premier parametre du point.

        y : float
            deuxieme parametre du point.

        annee : int
            année où on effectue la recherche.

        type_coord : str
            coordonnées du point (x, y). Si None : WGS84G

        id_return : bool
            renvoie l'id a la place du nom si vrai.

        Returns
        -------
            str
                nom de la zone d'appartenance ou None si échec.

        """
        recherche_indirecte = False
        if nom_zonage in ["REGION", "DEPARTEMENT"]:
            vrai_nom_zonage = c.copy(nom_zonage)
            nom_zonage = "COMMUNE"
            recherche_indirecte = True
        x, y = TransformerCoordonnees().transformer(x, y, type_coord)
        point = P(x, y)
        id_zonage = ZonageDAO().trouver_id_par_nom_annee(nom_zonage)
        # print(f"id zonage {id_zonage}")
        if id_zonage is not None:
            id_zones_possibles = ZoneDAO().trouver_id_zones_par_rectangles(x, y, id_zonage)
            # print(f"possibles id : {id_zones_possibles}")

        else:
            return None

        if id_zones_possibles is not None:
            for id_zone in id_zones_possibles:
                zone = ZoneDAO().trouver_par_id(id_zone, False)
                if isinstance(zone, Zone):
                    if zone.point_dans_zone(point):
                        if not recherche_indirecte:
                            if id_return:
                                return zone.id
                            return zone.nom

                        id_departement = ZoneDAO().trouver_id_mere(id_zone, 2)
                        if vrai_nom_zonage == "DEPARTEMENT":
                            if id_return:
                                return id_departement
                            return ZoneDAO().trouver_nom_par_id(id_departement)
                        id_region = ZoneDAO().trouver_id_mere(id_departement, 1)
                        if id_return:
                            return id_region
                        return ZoneDAO().trouver_nom_par_id(id_region)

        return None

    def trouver_chemin_zones_point(self, x: float, y: float, annee, type_coord: str = None):
        """
        Trouve le chemin des zones d'appartenance du point (x, y) dans une année particuliere
        tout en especifiant dans quel systeme de coordonnées il appartient.

        Parameters
        ----------

        x : float
            premier parametre du point.

        y : float
            deuxieme parametre du point.

        annee : int
            année où on effectue la recherche.

        type_coord : str
            coordonnées du point (x, y). Si None : WGS84G

        Returns
        -------
            str
                chemin des zones d'appartenance ou None si échec.

        """
        id_zone_plus_petite = self.trouver_zone_point("COMMUNE", x, y, annee, type_coord, True)
        if id_zone_plus_petite is None:
            return None
        zone_path = ZoneDAO().trouver_nom_par_id(id_zone_plus_petite) + "/"
        id_mere = ZoneDAO().trouver_id_mere(id_zone_plus_petite, 2)
        zone_path += ZoneDAO().trouver_nom_par_id(id_mere) + "/"
        id_grand_mere = ZoneDAO().trouver_id_mere(id_mere, 1)
        zone_path += ZoneDAO().trouver_nom_par_id(id_grand_mere)

        return zone_path

    def trouver_multiple_zone_point(
        self, nom_zonage: str, annee: int, liste_points: list[tuple], type_coord=None
    ):
        """
        Trouve les zone d'appartenance d'une liste de points (x, y) dans une année particuliere
        tout en especifiant dans quel systeme de coordonnées il appartient.

        Parameters
        ----------

        nom_zonage : str
            nom du zonage dont on fait la requete.

        liste_points : list[tuple]
            liste de points dont on cherche les zones respectives d'appartenance.

        annee : int
            année où on effectue la recherche.

        type_coord : str
            coordonnées du point (x, y). Si None : WGS84G

        Returns
        -------
            list[str]
                liste des noms des zones d'appartenance ou None si échec.

        """

        liste_aux = []
        for x, y in liste_points:
            liste_aux.append(self.trouver_zone_point(nom_zonage, annee, x, y, type_coord))

        return liste_aux


if __name__ == "__main__":
    print(ServicesRecherchePoint().trouver_chemin_zones_point(2.883, 42.6833, 2024))
