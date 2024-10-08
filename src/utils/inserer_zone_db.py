import os
import logging
import dotenv
import fiona

from utils.log_decorator import log
from dao.bdd_connection import DBConnection


class InsererZone():
    """
    Reinitialisation de la base de données
    """
    def __init__(self, path):
        self.__path = path
        dotenv.load_dotenv()

    @log
    def pop_zones(self):
        hierarchie_dict = self.recherche_hierarchie()
        plus_grand_zonage = self.obtenir_top_meres(hierarchie_dict)

        while plus_grand_zonage != []:
            # On commence par les zones qui sont le plus haut dans la zone hierarchique
            for zonage_nom in plus_grand_zonage:

                self.pop_zone(self.path_file + "/" + zonage_nom + ".shp",
                              self.trouver_id_zonage(hierarchie_dict[zonage_nom]),
                              zonage_nom[:3].upper())
                hierarchie_dict.pop("zonage_nom")

            plus_grand_zonage = self.obtenir_top_meres(hierarchie_dict)

    @log
    def pop_zone(self, path, id_zonage, insee_prefixe):
        with fiona.open(path, "r") as raw_zones:
            # Ajout des points dans la table de points s'ils ne sont pas presents
            # tout en gardant leur id a fin de pouvoir coder le contour
            for raw_zone in raw_zones:
                # Construction de zone
                nom = raw_zone["properties"]["NOM"]

                if "INSEE_" + insee_prefixe in raw_zone["properties"]:
                    code_insee = raw_zone["properties"]["INSEE_" + insee_prefixe]
                else:
                    code_insee = None

                if "POPULATION" in raw_zone["properties"]:

                    population = raw_zone["properties"]["POPULATION"]
                else:
                    population = None
                try:
                    with DBConnection().connection as connection:
                        with connection.cursor() as cursor:
                            cursor.execute(
                                "INSERT INTO Zone (nom, population, code_insee, id_zonage)"
                                "VALUES (%(nom)s, %(population)s, %(code_insee)s, %(id_zonage)s)",
                                {
                                    "nom": nom,
                                    "population": population,
                                    "code_insee": code_insee,
                                    "id_zonage": id_zonage
                                },
                            )
                            # res = cursor.fetchone()
                except Exception as e:
                    logging.info(e)

            # utilitzar obtenir_id_zone

    def trouver_id_zonage(nom_zonage):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id FROM Zonage       "
                        "WHERE nom= %(nom_zonage)s",
                        {
                            "nom_zonage": nom_zonage,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        if res:
            return res["id"]
        else:
            raise SystemError("Zonage Non trouvé")

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
