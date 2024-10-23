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

        noms_zonage_sans_mere = set(self.hierarchie_dict.values()) - set(
            self.hierarchie_dict.keys()
        )

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
            # on cree le ouveau zonage
            zonage = Zonage(nom_zonage, None, zonage_mere)
            # on enregistre le zonage a la bdd
            ZonageDAO.creer(zonage)
            # on stcok le zonage dans le dict des zonages
            self.zonages[nom_zonage] = zonage

    @log
    def __creer_zones(self):
        pass

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
        self.hierarchie_dict = hierarchie_dict
        self.noms_dict = hierarchie_dict.keys()

        for i in hierarchie_dict.values():
            if i not in self.noms_dict:
                self.noms_dict.append(i)

        self.hierarchie_dict_revers = {v: k for k, v in hierarchie_dict.iteritems()}

    @log
    def inserer(self):
        self.creer_zonage()
        self.creer_zonage_mere()

    @property
    def path(self):
        return self.__path
