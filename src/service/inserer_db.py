import dotenv

from utils.log_decorator import log
from src.utils.inserer_zonage_db import InsererZonage


class PopDB():
    """
    Reinitialisation de la base de données
    """
    def __init__(self, path):
        self.__path = path
        dotenv.load_dotenv()

    @log
    def inserer(self):
        # initialisation des classes d'insertition de données
        inserer_zonage = InsererZonage(self.path)

        # éxecution des fonctions d'insertion
        inserer_zonage.inserer()

    @property
    def path(self):
        return self.__path
