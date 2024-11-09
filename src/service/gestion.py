import os
import logging
import fiona
import json

from utils.log_decorator import log

from dao.zonage_dao import ZonageDAO
from dao.zone_dao import ZoneDAO

from business_object.zonage import Zonage
from business_object.zone import Zone
from business_object.multipolygone import MultiPolygone as Mpoly
from business_object.polygone import Polygone as Poly
from business_object.contour import Contour as C
from business_object.point import Point as P


class RequetesAPI:
    """
    Reinitialisation de la base de données
    """

    @log
    def creer(self, path, annee):

        self.path_file = path

        # noms de zonages presents dans le path
        noms_in_file = [name[:-4] for name in os.listdir(self.path_file) if name.endswith(".shp")]

        # on trouve l'annee grace au chemin
        self.annee = annee

        # on regarde la structure hierarchique par rapport aux noms qui sont dans la base
        # ainsi que ceux aui sont au fichier

        self.recherche_hierarchie(noms_in_file)

        # on créee les zonages
        self.__creer_zonages()

        # on créee les zones
        self.__creer_zones()

    @log
    def __creer_zonages(self):

        self.zonages = dict()
        hierarchie_dict = self.hierarchie_dict

        noms_zonage_sans_mere = set(hierarchie_dict.values()) - set(hierarchie_dict.keys())
        while len(noms_zonage_sans_mere) > 0:
            # on prend un nom parmi ceux aui n'ont pas de mere
            nom_zonage = noms_zonage_sans_mere.pop()
            # on regarde si le zonage contient un zonage mere
            if nom_zonage in self.hierarchie_dict.keys():
                # on prend le nom du zonage mere
                nom_zonage_mere = self.hierarchie_dict[nom_zonage]
                # on prend le zonage mere
                zonage_mere = self.zonages[nom_zonage_mere]
            else:
                zonage_mere = None
            # on cree le nouveau zonage, liste vide aui sera remplie avec la methode __creer_zone
            zonage = Zonage(nom_zonage, [], zonage_mere)
            # on enregistre le zonage a la bdd
            ZonageDAO().creer(zonage)
            # on stcok le zonage dans le dict des zonages
            self.zonages[nom_zonage] = zonage
            # on enleve les relations exposant la nouvelle mere
            hierarchie_dict = {
                key: val for key, val in hierarchie_dict.items() if val != nom_zonage
            }

            if len(noms_zonage_sans_mere) == 0:
                noms_zonage_sans_mere = set(hierarchie_dict.values()) - set(hierarchie_dict.keys())

    @log
    def __creer_zones(self):
        # A Refaire tout
        hierarchie_dict = self.hierarchie_dict_reverse
        zones = dict()
        unique_values = {item for sublist in hierarchie_dict.values() for item in sublist}

        noms_zonages_plus_petits = unique_values - set(hierarchie_dict.keys())

        while len(noms_zonages_plus_petits) > 0:
            # on prend un nom parmi ceux aui n'ont pas de fille
            nom_zonage = noms_zonages_plus_petits.pop()

            # on regarde si zonage contient un zonage fils
            if nom_zonage in self.hierarchie_dict_reverse.keys():
                # on prend le nom de la zone fille
                nom_zonage_fils = self.hierarchie_dict_reverse[nom_zonage]

            else:
                nom_zonage_fils = None
            # on ouvre la nouvelle zone avec fiona
            # on obtient le multipolygone, population, code_insee et annee
            with fiona.open(self.path_file + "/" + nom_zonage + ".shp", "r") as raw_zones:
                # Ajout des points dans la table de points s'ils ne sont pas presents
                # tout en gardant leur id a fin de pouvoir coder le contour
                insee_prefixe = nom_zonage[:3].upper()
                for raw_zone in raw_zones:
                    # Construction de zone
                    if "NOM" in raw_zone["properties"]:
                        nom = raw_zone["properties"]["NOM"]
                    else:
                        nom = None
                    if "INSEE_" + insee_prefixe in raw_zone["properties"]:
                        code_insee = raw_zone["properties"]["INSEE_" + insee_prefixe]
                    else:
                        code_insee = None

                    if "POPULATION" in raw_zone["properties"]:

                        population = raw_zone["properties"]["POPULATION"]
                    else:
                        population = None

                    if raw_zone["geometry"]["type"] == "Polygon":
                        raw_multipolygone = [raw_zone["geometry"]["coordinates"]]

                    elif raw_zone["geometry"]["type"] == "MultiPolygon":
                        raw_multipolygone = raw_zone["geometry"]["coordinates"]

                    else:
                        raw_multipolygone = None

                    multipolygone = self.get_multipolygone(raw_multipolygone)

            if nom_zonage_fils is None:
                zones_fille = None

            else:
                zones_fille = zones[nom]

            zone = Zone(nom, multipolygone, population, code_insee, self.annee, zones_fille)
            # mirar exemple

            # on enregistre le zonage a la bdd
            ZoneDAO().creer(zone, 1)
            # on stcok le zonage dans le dict des zonages
            nom_zone_mere = None
            if self.zones[nom_zone_mere] is None:
                self.zones[nom_zone_mere] = [zone]
            else:
                self.zones[nom_zone_mere].append(zone)
            # on enleve les relations exposant la nouvelle mere
            hierarchie_dict = {
                key: val for key, val in hierarchie_dict.items() if val != nom_zonage
            }

            if len(noms_zonages_plus_petits) == 0:
                noms_zonages_plus_petits = set(hierarchie_dict.values()) - set(
                    hierarchie_dict.keys()
                )

    def get_multipolygone(self, raw_mltipolygone):
        """renvoie un raw_multipolygone en type multipolygone (list list list tuple)"""
        liste_polygones = []
        for polygone in raw_mltipolygone:
            liste_cotours = []
            for contour in polygone:
                liste_points = []

                for point in contour:
                    liste_points.append(P(x=float(point[0]), y=float(point[1])))

                liste_cotours.append(C(points=liste_points))

            liste_polygones.append(Poly(contours=liste_cotours))
        return Mpoly(polygones=liste_polygones)

    @log
    def recherche_hierarchie(self, noms_in_file):

        hierarchie_dict = {}
        try:
            with open(
                "//filer-eleves2/id2475/ENSAI_ProjetInfo2A/data/hierarchie_zonages.txt", "r"
            ) as file:
                hierarchie_dict = json.load(file)
        except Exception as e:
            logging.info(e)
            raise
        # key is fille, argument is mother
        self.__hierarchie_dict = hierarchie_dict
        self.__noms_dict = list(hierarchie_dict.keys())

        for i in hierarchie_dict.values():
            if i not in self.noms_dict:
                self.__noms_dict.append(i)

        hierarchie_dict_revers = dict()

        for k, v in hierarchie_dict.items():
            if v not in hierarchie_dict_revers:
                hierarchie_dict_revers[v] = [k]  # Init nouvelle liste avec les arguments
            else:
                hierarchie_dict_revers[v].append(k)

        self.__hierarchie_dict_revers = hierarchie_dict_revers

    @log
    def inserer(self):
        self.creer_zonage()
        self.creer_zonage_mere()

    @property
    def hierarchie_dict(self):
        return self.__hierarchie_dict

    @property
    def hierarchie_dict_reverse(self):
        return self.__hierarchie_dict_revers

    @property
    def noms_dict(self):

        return self.__noms_dict


if __name__ == "__main__":
    test_class = RequetesAPI()
    test_class.creer(
        "//filer-eleves2\id2475\ENSAI_ProjetInfo2A/ADMIN-EXPRESS_3-2__SHP_LAMB93_FXX_2024-10-16/ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2024-10-00105/ADE_3-2_SHP_LAMB93_FXX-ED2024-10-16",
        2024,
    )
