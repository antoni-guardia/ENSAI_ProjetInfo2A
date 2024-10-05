import os
import logging
import dotenv
import fiona

from utils.log_decorator import log
from dao.bdd_connection import DBConnection


class PopDB():
    """
    Reinitialisation de la base de données
    """
    def __init__(self, path):
        self.__path = path
        dotenv.load_dotenv()

    @log
    def pop_zonage(self):

        element = [name for name in os.listdir(self.path) if name.startswith('1_')]
        self.path_file = self.path + "/" + element[0]
        # annee = path_file.split("_")[-1][:4]

        noms_zonages = [name[:-4] for name in os.listdir(self.path_file) if name.endswith('.shp')]

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Insert each zonage name into the database
                    for nom in noms_zonages:
                        cursor.execute(
                            """
                            INSERT INTO Zonage(nom) VALUES (%s)
                            """,
                            (nom,)
                        )
        except Exception as e:
            logging.info(e)
            raise

    @log
    def pop_zonage_mere(self):
        # on commence par se connecter a la bdd et obtenir
        # les zonages présents dans la bdd ainsi que son id
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id, nom FROM Zonage
                        """
                    )

                    # On enregistre les zonages sous forme de dictionnaire
                    # afin de faciliter la création de la table ZonageMere
                    zonages = {nom: id for id, nom in cursor.fetchall()}

        except Exception as e:
            logging.info(e)
            raise

        hierarchie_dict = self.recherche_hierarchie()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:

                    for zonage_fille in hierarchie_dict.keys():
                        # on obtient les id des zonages mere et fille
                        # si elles sont dans le dict d'hierarchie
                        if zonage_fille in zonages and hierarchie_dict[zonage_fille]:
                            id_zonage_fille = zonages[zonage_fille]
                            id_zonage_mere = zonages[hierarchie_dict[zonage_fille]]

                            # on les ajoute sur la table
                            cursor.execute(
                                """
                                INSERT INTO ZonageMere(id_zonage_mere, id_zonage_fille)
                                    VALUES (%(mere)s, %(fille)s)
                                """,
                                {"mere": id_zonage_mere,
                                 "fille": id_zonage_fille}
                            )
        except Exception as e:
            logging.info(e)
            raise

    @log
    def recherche_hierarchie(self):
        hierarchie_dict = {}
        try:
            with open('data.txt', 'r') as file:
                for line in file:
                    key, value = line.strip().split(':')  # Split by delimiter
                    hierarchie_dict[key] = value
        except Exception as e:
            logging.info(e)
            raise
        return hierarchie_dict

    @log
    def pop_zones(self):
        hierarchie_dict = self.recherche_hierarchie()
        plus_grand_zonage = self.obtenir_top_meres(hierarchie_dict)

        while plus_grand_zonage != []:
            # On commence par les zones qui sont le plus haut dans la zone hierarchique
            for zonage_nom in plus_grand_zonage:
                self.pop_zone(self.path_file + "/" + zonage_nom + ".shp",
                              hierarchie_dict[zonage_nom])
                hierarchie_dict.pop("zonage_nom")

            plus_grand_zonage = self.obtenir_top_meres(hierarchie_dict)

    def pop_zone(self, path, zonage_mere):
        with fiona.open(path):
            # Ajout des points dans la table de points s'ils ne sont pas presents
            # tout en gardant leur id a fin de pouvoir coder le contour
            pass
            # utilitzar obtenir_id_zone

    def obtenir_id_zone(code_insee):
        pass

    def obtenir_top_meres(self, dictionaire):
        # On regarde les enfants
        children = set(dictionaire.values())

        # On identifie les parents
        parents = set(dictionaire.keys())

        # On obtient les elements les plus hauts dans la chaine
        top_mothers = list(children - parents)

        return top_mothers

    @property
    def path(self):
        return self.__path


if __name__ == "__main__":
    pass
