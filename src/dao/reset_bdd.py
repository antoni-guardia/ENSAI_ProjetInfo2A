import os
import logging
import dotenv

from utils.log_decorator import log
from dao.bdd_connection import DBConnection

from service.joueur_service import JoueurService


class ResetDatabase():
    """
    Reinitialisation de la base de données
    """

    @log
    def lancer(self):

        dotenv.load_dotenv()

        schema = os.environ["POSTGRES_SCHEMA"]

        create_schema = f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"

        init_db = open("data/init_bdd.sql", encoding="utf-8")
        init_db_as_string = init_db.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(create_schema)
                    cursor.execute(init_db_as_string)
        except Exception as e:
            logging.info(e)
            raise

        # Appliquer le hashage des mots de passe à chaque joueur
        joueur_service = JoueurService()
        for j in joueur_service.lister_tous(inclure_mdp=True):
            joueur_service.modifier(j)

        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
    ResetDatabase().lancer(True)
