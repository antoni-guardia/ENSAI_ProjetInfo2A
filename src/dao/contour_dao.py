from utils.log_decorator import log
from src.business_object.contour import Contour
from src.dao.point_dao import PointDao
from src.dao.abstract_dao import AbstractDao


class ContourDao(AbstractDao):
    """
    Classe contenant les méthodes pour accéder aux Contours de la base de données
    """

    @log
    def __inserer(self):

        res = self.__requete("INSERT INTO Contour DEFAULT VALUES RETURNING id;")

        if res:
            return res[0][0]
        return None

    @log
    def __CreerOrdrePointContour(self, id_point: int, id_contour: int, cardinal: int):
        res = self.__requete(
            "INSERT INTO OrdrePointContour (cardinal, id_point, id_contour)"
            " VALUES (%(cardinal)s, %(id_point)s, %(id_contour)s)"
            "RETURNING cardinal;",
            {"cardinal": cardinal, "id_point": id_point, "id_contour": id_contour},
        )

        if res is not None:
            res[0][0]
            return True

        return False

    @log
    def trouver_par_id(self, id_contour: int):
        res = self.requete(
            "SELECT id_point FROM OrdrePointContour"
            "WHERE id_contour=%(id_contour)s "
            "ORDER BY cardinal",
            {"id_contour": id_contour},
        )
        if res is None:
            return None

        liste_points = []
        res = [i["id_point"] for i in res]
        for id_point in res:
            liste_points.append(PointDao().trouver_par_id(id_point))

        return Contour(points=liste_points, id=id_contour)

    @log
    def creer(self, contour: Contour):

        # on crée le contour
        id_contour = self.__inserer()

        for cardinal, point in enumerate(contour.points):
            if PointDao().trouver_id(point) is None:
                id_point = PointDao().creer(point)

            self.__CreerOrdrePointContour(id_point, id_contour, cardinal)

        contour.id = id_contour
        return id_contour

    @log
    def trouver_id(self, contour: Contour):

        id_points = []

        for point in contour.points:
            id_points.append(PointDao().trouver_id(point))

        para_set = self.__contours_contenat_point(id_points.pop())

        while len(para_set) > 1 and id_points != []:
            para_set -= self.__contours_contenat_point(id_points.pop())

        return para_set.pop()

    @log
    def __contours_contenat_point(self, id_point):

        res = self.__requete(
            "SELECT id_contour FROM OrdrePointContour WHERE id_point = %(id_point)s",
            {"id_point": id_point},
        )

        return {row[0][0] for row in res} if res else set()

    @log
    def supprimer(self, id_contour):
        res1 = self.__requete(
            "DELETE FROM Contour WHERE id=%(id_contour)s ",
            {"id_contour": id_contour},
        )

        res2 = self.__requete(
            "DELETE FROM OrdrePointContour WHERE id_contour=%(id_contour)s ",
            {"id_contour": id_contour},
        )

        return res1 > 0 and res2 > 0
