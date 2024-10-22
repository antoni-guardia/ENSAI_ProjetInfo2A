from utils.singleton import Singleton
from dao.bdd_connection import DBConnection


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    def lancer(self, test_dao=False):
        print("Ré-initialisation de la base de données")

        init_db = open("data/init_bdd.sql", encoding="utf-8")
        init_db_as_string = init_db.read()

        pop_db = open("data/pop_bdd.sql", encoding="utf-8")
        pop_db_as_string = pop_db.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(init_db_as_string)
                    if test_dao:
                        cursor.execute(pop_db_as_string)
        except Exception as e:
            print(e)
            raise

        print("Ré-initialisation de la base de données - Terminée")

        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
