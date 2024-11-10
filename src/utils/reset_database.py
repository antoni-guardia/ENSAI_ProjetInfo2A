from utils.singleton import Singleton
from dao.bdd_connection import DBConnection
import dotenv
import os


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    def lancer(self, test_dao=False):
        print("Ré-initialisation de la base de données")

        # Load environment variables
        dotenv.load_dotenv()
        schema = os.environ.get("POSTGRES_SCHEMA", "public")  # default to "public" if not set

        # Read SQL files
        with open("data/init_bdd.sql", encoding="utf-8") as init_db:
            init_db_as_string = init_db.read()

        if test_dao:
            with open("data/pop_bdd.sql", encoding="utf-8") as pop_db:
                pop_db_as_string = pop_db.read()
        else:
            pop_db_as_string = None

        create_schema = (
            f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA"
            f" {schema}; SET search_path TO {schema};"
        )

        # Database reset process
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Drop and recreate schema
                    cursor.execute(create_schema)

                    # Execute initialization SQL
                    cursor.execute(init_db_as_string)

                    if test_dao and pop_db_as_string:
                        cursor.execute(pop_db_as_string)

        except Exception as e:
            print(f"Error during database reinitialization: {e}")
            raise

        print("Ré-initialisation de la base de données - Terminée")
        return True


if __name__ == "__main__":
    ResetDatabase().lancer(True)
