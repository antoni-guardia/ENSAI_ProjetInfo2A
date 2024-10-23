import os
import logging
import dotenv

from utils.log_decorator import log
from dao.bdd_connection import DBConnection

from dao.zonage_dao import ZonageDAO
from dao.zone_dao import ZoneDAO

from business_object.zonage import Zonage


class RequetesAPI:
    """
    Reinitialisation de la base de données
    """

    def __init__(self):
        dotenv.load_dotenv()

    @log
    def creer(self, path):
        element = [name for name in os.listdir(self.path) if name.startswith("1_")]
        self.path_file = self.path + "/" + element[0]

        # noms de zonages presents dans le path
        noms_in_file = [name[:-4] for name in os.listdir(self.path_file) if name.endswith(".shp")]

        # on trouve l'annee grace au chemin
        self.annee = self.path_file.split("_")[-1][:4]

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

        noms_zones_plus_petites = set(hierarchie_dict.values()) - set(hierarchie_dict.keys())

        while len(noms_zones_plus_petites) > 0:
            # on prend un nom parmi ceux aui n'ont pas de fille
            nom_zone = noms_zones_plus_petites.pop()
            # on regarde si zone contient une zone fille
            if nom_zone in self.hierarchie_dict_reverse.keys():
                # on prend le nom de la zone fille
                nom_zone_fille = self.hierarchie_dict_reverse[nom_zone]
                # on prend le zonage mere
                zone_fille = self.zonages[nom_zone_mere]
            else:
                zone_mere = None
            # on cree le nouveau zonage, liste vide aui sera remplie avec la methode __creer_zone
            zone = Zonage(nom_zone, [], zone_mere)
            # on enregistre le zonage a la bdd
            ZonageDAO().creer(zonage)
            # on stcok le zonage dans le dict des zonages
            self.zonages[nom_zone] = zonage
            # on enleve les relations exposant la nouvelle mere
            hierarchie_dict = {
                key: val for key, val in hierarchie_dict.items() if val != nom_zonage
            }

            if len(noms_zones_plus_petites) == 0:
                noms_zones_plus_petites = set(hierarchie_dict.values()) - set(
                    hierarchie_dict.keys()
                )

    @log
    def recherche_hierarchie(self, noms_in_file):

        hierarchie_dict = {}
        try:
            with open("data.txt", "r") as file:
                for line in file:
                    key, value = line.strip().split(":")  # Split by delimiter
                    if key and value in noms_in_file:
                        hierarchie_dict[key] = value
        except Exception as e:
            logging.info(e)
            raise
        # key is fille, argument is mother
        self.__hierarchie_dict = hierarchie_dict
        self.__noms_dict = hierarchie_dict.keys()

        for i in hierarchie_dict.values():
            if i not in self.noms_dict:
                self.__noms_dict.append(i)

        self.__hierarchie_dict_revers = {v: k for k, v in hierarchie_dict.items()}

    @log
    def inserer(self):
        self.creer_zonage()
        self.creer_zonage_mere()

    @property
    def path(self):
        return self.__path

    @property
    def hierarchie_dict(self):
        return self.__hierarchie_dict

    @property
    def hierarchie_dict_reverse(self):
        return self.__hierarchie_dict_reverse
