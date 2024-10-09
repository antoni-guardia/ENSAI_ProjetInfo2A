import logging
from utils.log_decorator import log
from dao.bdd_connection import DBConnection
from src.business_object.contour import Contour
from src.dao.point_dao import PointDao


class ContourDao():
    """
    Classe contenant les méthodes pour accéder aux Contours de la base de données
    """

    @log
    def __inserer(self) -> int:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                     "INSERT INTO Contour DEFAULT VALUES RETURNING id;",
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logging.info(e)
        if res:
            return res["id"]
        return None

    @log
    def __CreerOrdrePointContour(self, id_point: int, id_contour: int, cardinal: int) -> bool:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                     "INSERT INTO OrdrePointContour (cardinal, id_point, id_contour)"
                     " VALUES (%(cardinal)s, %(id_point)s, %(id_contour)s)"
                     "RETURNING cardinal;",
                     {
                      "cardinal": cardinal,
                      "id_point": id_point,
                      "id_contour": id_contour
                     },
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logging.info(e)

        if res:
            res["cardinal"]
            return True

        return False

    @log
    def creer(self, contour: Contour) -> int:

        # on crée le contour
        id_contour = self.__inserer()

        for cardinal, point in enumerate(contour.points):
            id_point = PointDao().creer(point)
            self.__CreerOrdrePointContour(id_point, id_contour, cardinal)

        contour.id = id_contour
        return id_contour

    @log
    def trouver_par_id(self, id_contour: int) -> Contour:
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                     "SELECT id_point FROM OrdrePointContour"
                     "WHERE id_contour=%(id_contour)s "
                     "ORDER BY cardinal",
                     {
                        "id_contour": id_contour
                     }

                    )
                    res = cursor.fetchall()

        except Exception as e:
            logging.info(e)

        if res is None:
            return None

        liste_points = []
        for id_point in res:
            liste_points.append(PointDao().trouver_par_id(id_point))

        return Contour(points=liste_points, id=id_contour)

    def trouver_id(self, contour: Contour) -> int:
        pass