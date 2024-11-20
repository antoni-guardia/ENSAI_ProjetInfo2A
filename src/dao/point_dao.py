from utils.log_decorator import log
from business_object.point import Point
from dao.abstract_dao import AbstractDao


class PointDao(AbstractDao):
    """
    Classe contenant les méthodes pour accéder aux Points de la base de données
    """

    @log
    def creer(self, point: Point):

        if point.id is not None:
            return point.id

        res = self.requete(
            """
        WITH ins AS (
            INSERT INTO Point (x, y)
            SELECT %(x)s, %(y)s
            WHERE NOT EXISTS (
                SELECT 1 FROM Point WHERE x = %(x)s AND y = %(y)s
            )
            RETURNING id
        ),
        existing AS (
            SELECT id FROM Point WHERE x = %(x)s AND y = %(y)s
        )
        SELECT id FROM ins
        UNION
        SELECT id FROM existing LIMIT 1;
        """,
            {"x": point.x, "y": point.y},
        )

        point.id = res[0]["id"]
        return res[0]["id"]

    @log
    def trouver_id(self, point: Point):

        res = self.requete(
            "SELECT id FROM Point WHERE x = %(x)s  AND y = %(y)s;",
            {"x": point.x, "y": point.y},
        )

        id_point = None
        if res:
            point.id = res[0]["id"]
            id_point = res[0]["id"]

        return id_point

    @log
    def supprimer(self, id_point: Point):

        res = self.requete_row_count(
            "DELETE FROM Point WHERE id=%(id_point)s;",
            {"id_point": id_point},
        )

        return res > 0

    @log
    def trouver_par_id(self, id_point):

        res = self.requete(
            "SELECT *                           "
            "  FROM Point                      "
            " WHERE id = %(id_point)s;  ",
            {"id_point": id_point},
        )

        point = None
        if res:
            x = float(res[0]["x"])
            y = float(res[0]["y"])

            point = Point(x, y, id_point)

        return point
