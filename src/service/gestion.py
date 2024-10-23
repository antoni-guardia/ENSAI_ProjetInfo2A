import os
import logging
import dotenv

from utils.log_decorator import log
from dao.bdd_connection import DBConnection

from dao.zonage_dao import ZonageDAO
from dao.zone_dao import ZoneDAO

from business_object.zonage import Zonage


class InsererZonage:
    """
    Reinitialisation de la base de données
    """

    def __init__(self):
        dotenv.load_dotenv()

    @log
    def creer(self, path):
        element = [name for name in os.listdir(self.path) if name.startswith("1_")]
        self.path_file = self.path + "/" + element[0]
        self.annee = self.path_file.split("_")[-1][:4]
        self.__creer_zonages()
        self.__creer_zones()

    @log
    def __creer_zonages(self):

        noms_zonages = [name[:-4] for name in os.listdir(self.path_file) if name.endswith(".shp")]
        self.zonages = []

        for nom_zonage in noms_zonages:
            zonage = Zonage(nom_zonage, None)

            ZonageDAO.creer(zonage)

            self.zonages.append(zonage)

    @log
    def __creer_zones(self):
        

    @log
    def recherche_hierarchie(self):
        hierarchie_dict = {}
        try:
            with open("data.txt", "r") as file:
                for line in file:
                    key, value = line.strip().split(":")  # Split by delimiter
                    hierarchie_dict[key] = value
        except Exception as e:
            logging.info(e)
            raise
        return hierarchie_dict

    @log
    def inserer(self):
        self.creer_zonage()
        self.creer_zonage_mere()

    @property
    def path(self):
        return self.__path
