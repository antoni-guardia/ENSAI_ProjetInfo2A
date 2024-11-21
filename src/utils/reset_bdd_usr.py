from utils.singleton import Singleton
from dao.bdd_connection import DBConnection


class ResetDatabaseUSR(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    def lancer(self):
        print("Ré-initialisation de la base de données usrs")

        with open("data/init_bdd_utlis.sql", encoding="utf-8") as init_db:
            init_db_as_string = init_db.read()

        # Database reset process
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Execute initialization SQL
                    cursor.execute(init_db_as_string)

        except Exception as e:
            print(f"Error during database reinitialization: {e}")
            raise

        print("Ré-initialisation de la base de données - Terminée")
        return True


if __name__ == "__main__":
    ResetDatabaseUSR().lancer()
