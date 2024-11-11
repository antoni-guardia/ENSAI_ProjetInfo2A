from utils.log_decorator import log
from business_object.zone import Zone
from dao.polygone_dao import PolygoneDAO
from dao.abstract_dao import AbstractDao
from business_object.multipolygone import MultiPolygone


class ZoneDAO(AbstractDao):

    @log
    def __inserer(self, id_zonage, nom, population, code_insee, annee, cle_hash) -> int:
        res = self.requete(
            "INSERT INTO Zone(id_zonage, nom, population, code_insee, annee, cle_hash) VALUES"
            " (%(id_zonage)s, %(nom)s, %(population)s, %(code_insee)s, %(annee)s, %(cle_hash)s)"
            "  RETURNING id;",
            {
                "id_zonage": id_zonage,
                "nom": nom,
                "population": population,
                "code_insee": code_insee,
                "annee": annee,
                "cle_hash": cle_hash
            },
        )

        if res:
            return res[0]["id"]
        return None

    @log
    def __CreerMultipolygone(self, id_zone: int, id_polygone: int) -> bool:
        res = self.__requete(
            "INSERT INTO MultiPolygone (id_zone, id_polygone)"
            " VALUES (%(id_zone)s, %(id_polygone)s)"
            "RETURNING cardinal;",
            {
                "id_zone": id_zone,
                "id_polygone": id_polygone,
            },
        )
        if res:
            return True
        return False

    @log
    def creer(self, zone: Zone, id_zonage) -> int:
        """Commencer à construire par les zones les plus petites"""

        # on crée la zone
        id_zone = self.__inserer(id_zonage,
                                 zone.nom,
                                 zone.population,
                                 zone.code_insee,
                                 zone.annee,
                                 hash(zone))

        for polygone in zone.multipolygone:
            id_polygone = PolygoneDAO().trouver_id(polygone)

            if id_polygone is None:
                id_polygone = PolygoneDAO().creer(polygone)

            self.__CreerMultipolygone(id_zone, id_polygone)

        if zone.zones_fille is not None:
            for zone_fille in zone.zones_fille:

                if zone_fille.id is None:
                    id_fille = self.trouver_id(zone_fille)

                else:
                    id_fille = zone_fille.id

                self.requete(
                    "INSERT INTO ZoneFille (id_zone_mere, id_zone_fille)"
                    " VALUES (%(id_zone_mere)s, %(id_zone_fille)s);",
                    {"id_zone_mere": id_zone, "id_zone_fille": id_fille},
                )

        zone.id = id_zone
        return id_zone

    @log
    def supprimer(self, id_zone: int):

        self.requete(
            "DELETE FROM MultiPolygone WHERE id_zone=%(id_zone)s;",
            {"id_zone": id_zone},
        )

        self.requete(
            "DELETE FROM ZoneFille WHERE id_zone_mere=%(id_zone)s;",
            {"id_zone": id_zone},
        )

        self.requete(
            "DELETE FROM ZoneFille WHERE id_zone_fille=%(id_zone)s;",
            {"id_zone": id_zone},
        )

        res = self.requete(
            "DELETE FROM Zone WHERE id=%(id_zone)s;",
            {"id_zone": id_zone},
        )
        return res > 0

    @log
    def trouver_zones_filles(self, id_zone_mere):
        id_filles = self.requete(
            "SELECT id_zone_fille FROM ZoneFille WHERE id_zone_mere = %(id_zone_mere)s;",
            {"id_zone_mere": id_zone_mere},
        )

        if id_filles is None:
            return None

        return [self.trouver_par_id(id_fille["id_zone_fille"]) for id_fille in id_filles]

    @log
    def trouver_par_id(self, id_zone: int, filles=True):

        res = self.requete(
            "SELECT id_polygone FROM MultiPolygone WHERE id_zone=%(id_zone)s;",
            {"id_zone": id_zone},
        )

        data_zone = self.requete(
            "SELECT nom, population, code_insee, annee FROM Zone WHERE id=%(id_zone)s;",
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

        if filles:
            zones_fille = self.trouver_zones_filles(id_zone)

            return Zone(nom, multipolygone, population, code_insee, annee, zones_fille, id_zone)

        return Zone(nom, multipolygone, population, code_insee, annee, None, id_zone)

    @log
    def trouver_id(self, zone: Zone):
        cle_hash = hash(zone)
        res = self.requete(
            f"SELECT id FROM Zone WHERE cle_hash={cle_hash}")

        if res is not None:
            return res[0]["id"]

        return None
