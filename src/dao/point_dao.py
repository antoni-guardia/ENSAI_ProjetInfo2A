from utils.log_decorator import log
from src.business_object.point import Point
from src.dao.abstract_dao import AbstractDao


class PointDao(AbstractDao):
    """
    Classe contenant les méthodes pour accéder aux Points de la base de données
    """

    @log
    def creer(self, point: Point):

        res = self.__requete(
            "INSERT INTO Point (x, y)" "VALUES (%(x)s, %(y)s)  RETURNING id;",
            {"x": point.x, "y": point.y},
        )

        if res:
            point.id = res["id"]
            return res["id"]

        return None

    @log
    def trouver_id(self, point: Point):

        res = self.__requete(
            "SELECT id FROM Point WHERE x = %(x)s  AND y = %(y)s RETURNING id;",
            {"x": point.x, "y": point.y},
        )

        id_point = None
        if res:
            point.id = res["id"]
            id_point = res["id"]

        return id_point

    @log
    def supprimer(self, id_point: Point):

        res = self.__requete(
            "DELETE FROM Point WHERE id=%(id_point)s ",
            {"id_point": id_point},
        )

        return res > 0

    @log
    def trouver_par_id(self, id_point):

        res = self.requete(
            "SELECT *                           "
            "  FROM Point                      "
            " WHERE id_joueur = %(id_point)s;  ",
            {"id_point": id_point},
        )

        point = None
        if res:
            point = Point(x=res["x"], y=res["y"], id=res["id"])

        return point
