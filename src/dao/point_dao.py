import logging
from utils.log_decorator import log
from dao.bdd_connection import DBConnection
from src.business_object.point import Point


class PointDao():
    """
    Classe contenant les méthodes pour accéder aux Points de la base de données
    """

    @log
    def creer(self, point: Point) -> bool:
        """Creation d'un point dans la base de données

        Parameters
        ----------
        point : Point

        Returns
        -------
        created : bool
            True si la création est un succès
            False sinon
        """
        res = None

        if self.trouver_id(point) is not None:
            return True

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                     "INSERT INTO Point (x, y)"
                     "VALUES (%(x)s, %(y)s)",
                     {
                      "x": point.x,
                      "y": point.y
                     },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)

        if res:
            point.id = res[id]
            return True

        return False

    @log
    def trouver_id(self, point: Point) -> int:
        """trouver un point grace à ces coordonnées

        Parameters
        ----------
        point : Point
            point que dont on cherche l'id

        y : float
            numéro coord. y du point que l'on souhaite trouver

        Returns
        -------
        id_point : int
            renvoie l'id du point que l'on cherche par ces coordonnées
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id                           "
                        "FROM Point                         "
                        " WHERE x = %(x)s  AND y = %(y)s;   ",
                        {"x": point.x,
                         "y": point.y},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        id_point = None
        if res:
            point.id = res["id"]
            id_point = res["id"]

        return id_point

    @log
    def supprimer(self, point: Point) -> bool:
        """Suppression d'un point dans la base de données

        Parameters
        ----------
        point : Point
            point à supprimer de la base de données

        Returns
        -------
            True si le point a bien été supprimé
        """

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    # Supprimer le compte d'un joueur
                    cursor.execute(
                        "DELETE FROM Point                  "
                        " WHERE id=%(id_point)s      ",
                        {"id_point": point.id_joueur},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.info(e)
            raise

        return res > 0

    @log
    def trouver_par_id(self, id_point) -> Point:
        """trouver un point grace à son id

        Parameters
        ----------
        id_point : int
            numéro id du poin que l'on souhaite trouver

        Returns
        -------
        point : Point
            renvoie le point que l'on cherche par id
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM Point                      "
                        " WHERE id_joueur = %(id_point)s;  ",
                        {"id_point": id_point},
                    )
                    res = cursor.fetchone()

        except Exception as e:
            logging.info(e)
            raise

        point = None
        if res:
            point = Point(
                x=res["x"],
                y=res["y"],
                id=res["id"]
            )

        return point
