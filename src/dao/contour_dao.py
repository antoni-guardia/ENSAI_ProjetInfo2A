import logging
from utils.log_decorator import log
from dao.bdd_connection import DBConnection

from b

class InsererContour():
    """
    Reinitialisation de la base de données
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y


    @log
    def inserer(self):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                     "INSERT INTO Point (x, y)"
                     "VALUES (%(x)s, %(y)s)",
                     {
                      "x": self.x,
                      "y": self.y
                     },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        return res["id"]
