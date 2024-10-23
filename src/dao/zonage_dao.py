from utils.log_decorator import log
from business_object.zonage import Zonage
from dao.zone_dao import ZoneDAO
from dao.abstract_dao import AbstractDao


class ZonageDAO(AbstractDao):

    @log
    def creer(self, zonage: Zonage) -> int:
        """Rentrer le zonage le plus petit possible"""

        # on crée le zonage
        id_zonage = self.requete(
            "INSERT INTO Zonage(nom) VALUES"
            " (%(nom)s)  RETURNING id;",
        )

        # si le zonage vient d'être ajouté
        if id_zonage is not None:
            id_zonage = id_zonage[0]["id"]
            zonage.id = id_zonage

            # on regarde par rappot a la table ZonageMere
            if zonage.zonage_mere is not None:
                id_zonage_mere = self.trouver_id(zonage)
                if id_zonage_mere is None:
                    id_zonage_mere = self.creer()

                self.requete(
                    "INSERT INTO ZonageMere(id_zonage_mere, id_zonage_fille) VALUES"
                    " (%(id_zonage_mere)s, %(id_zonage_fille)s)  RETURNING id;",
                    {"id_zonage_mere": id_zonage_mere,
                     "id_zonage_fille": id_zonage}
                        )

            return id_zonage

        return None

    @log
    def get_zones(self, id_zonage: int, filles=True):
        id_zones = self.requete(
            "SELECT id FROM Zone WHERE id_zonage=%(id_zonage)s;",
            {"id_zonage": id_zonage}
        )
        if id_zones is None:
            return None
        id_zones = [id_zone["id"] for id_zone in id_zones]

        zones = [ZoneDAO().trouver_par_id(id_zone, filles) for id_zone in id_zones]

        return zones

    @log
    def supprimer(self, id_zonage: int):

        zones = self.get_zones(id_zonage, filles=False)
        for zone in zones:
            if zone.id is not None:
                ZoneDAO().supprimer(zone.id)

        self.requete(
            "DELETE FROM ZonageMere WHERE id_zone_mere=%(id_zonage)s"
            " OR id_zone_fille=%(id_zonage)s",
            {"id_zonage": id_zonage},
        )

        res = self.requete(
            "DELETE FROM Zonage WHERE id=%(id_zonage)s ",
            {"id": id_zonage},
        )

        return res > 0

    @log
    def trouver_par_id(self, id_zonage: int):

        zones = self.get_zones(id_zonage)
        

        res = self.__requete(
            "SELECT id FROM MultiPolygone "
            "WHERE id_zone=%(id_zone)s ",
            {"id_zone": id_zone},
        )

        data_zone = self.__requete(
            "SELECT nom, population, code_insee, annee FROM Zone "
            "WHERE id_zone=%(id_zone)s ",
            {"id_zone": id_zone},
        )

        if res is None or data_zone is None:
            return None

        liste_polygones = []
        for id_polygone in res:
            liste_polygones.append(PolygoneDAO().trouver_par_id(id_polygone["id_polygone"]))

        multipolygone = MultiPolygone(liste_polygones)
        nom = data_zone[0]["nom"]
        population = data_zone[0]["population"]
        code_insee = data_zone[0]["code_insee"]
        annee = data_zone[0]["annee"]

        zones_fille = self.trouver_zones_filles(id_zone)

        return Zone(nom, multipolygone, population, code_insee, annee, zones_fille, id_zone)

    @log
    def trouver_id(self, zone: Zone):

        id_polygones = []

        for polygone in zone.multipolygone:
            id_polygones.append(PolygoneDAO().trouver_id(polygone))

        para_set = self.__zones_contenant_polygone(id_polygones.pop())

        while len(para_set) > 1 and id_polygones != []:
            para_set -= self.__zones_contenant_polygone(id_polygones.pop())

        return para_set.pop()

    @log
    def __zones_contenant_polygone(self, id_polygone):

        res = self.__requete(
            "SELECT id_zone FROM MultiPolygone WHERE id_polygone = %(id_polygone)s",
            {"id_polygone": id_polygone},
        )

        return {row["id_zone"] for row in res} if res else set()
