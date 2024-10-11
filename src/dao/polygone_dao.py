import logging
from utils.log_decorator import log
from dao.bdd_connection import DBConnection
from src.business_object.polygone import Polygone
from src.dao.contour_dao import ContourDao


class PolygoneDAO:
    """
    Classe contenant les méthodes pour accéder aux Contours de la base de données
    """

    @log
    def __inserer(self) -> int:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO Polygone DEFAULT VALUES RETURNING id;",
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logging.info(e)
        if res:
            return res["id"]
        return None

    @log
    def __CreerEstEnclave(self, id_contour: int, id_polygone: int, est_enclave: bool) -> bool:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO OrdrePointContour (est_enclave, id_contour, id_polygone)"
                        " VALUES (%(est_enclave)s, %(id_contour)s, %(id_polygone)s)"
                        "RETURNING cardinal;",
                        {
                            "est_enclave": est_enclave,
                            "id_contour": id_contour,
                            "id_polygone": id_polygone,
                        },
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logging.info(e)

        if res:
            res["est_enclave"]
            return True

        return False

    @log
    def creer(self, polygone: Polygone) -> int:

        # on crée le polygone
        id_polygone = self.__inserer()

        for index, contour in enumerate(polygone.contours):

            id_contour = ContourDao().creer(contour)
            self.__CreerOrdrePointContour(id_contour, id_polygone, bool(index))

        contour.id = id_contour
        return id_contour
