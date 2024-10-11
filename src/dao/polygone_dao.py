from utils.log_decorator import log
from src.business_object.polygone import Polygone
from src.dao.contour_dao import ContourDao
from src.dao.abstract_dao import AbstractDao


class PolygoneDAO(AbstractDao):

    @log
    def __inserer(self) -> int:
        res = self.__requete(
            "INSERT INTO Polygone DEFAULT VALUES RETURNING id;",
        )

        if res:
            return res["id"]
        return None

    @log
    def __CreerEstEnclave(self, id_contour: int, id_polygone: int, est_enclave: bool) -> bool:
        res = self.__requete(
            "INSERT INTO OrdrePointContour (est_enclave, id_contour, id_polygone)"
            " VALUES (%(est_enclave)s, %(id_contour)s, %(id_polygone)s)"
            "RETURNING cardinal;",
            {
                "est_enclave": est_enclave,
                "id_contour": id_contour,
                "id_polygone": id_polygone,
            },
        )

        if res:
            res["est_enclave"]
            return True
        return False

    @log
    def creer(self, polygone: Polygone) -> int:

        # on crée le polygone
        id_polygone = self.__inserer()

        for index, contour in enumerate(polygone.contours):
            if ContourDao().trouver_id(contour) is None:
                id_contour = ContourDao().creer(contour)
                self.__CreerEstEnclave(id_contour, id_polygone, bool(index))

            self.__CreerEstEnclave(contour.id, id_polygone, bool(index))

        contour.id = id_contour
        return id_contour

    @log
    def supprimer(self):
        pass

    @log
    def trouver_par_id(self):
        pass

    @log
    def trouver_id(self):
        pass
