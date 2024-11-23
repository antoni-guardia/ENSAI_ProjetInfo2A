import logging
import fiona
import json

from utils.log_decorator import log

from dao.zonage_dao import ZonageDAO
from dao.zone_dao import ZoneDAO

from business_object.zonage import Zonage
from business_object.zone import Zone
from business_object.multipolygone import MultiPolygone as Mpoly
from business_object.polygone import Polygone as Poly
from business_object.contour import Contour as C
from business_object.point import Point as P

from dao.bdd_connection import DBConnection
from utils.reset_database import ResetDatabase


class AjouterDonneesParPath:
    """
    Ajouter des données à travers un fichier de .shp et une année
    """

    @log
    def verification_existance_bdd(self):
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT tablename FROM pg_tables WHERE schemaname = 'vous_etes_ici';"
                    )
                    res = cursor.fetchall()
                    return bool(res)

        except Exception as e:
            logging.error(f"Query failed: {e}")
            return None

    @log
    def creer(
        self,
        path,
        annee,
        reinitialiser=False,
        attrib_zones_zonages=False,
        precision=7,
        given_dict=dict(),
    ):
        """
        Ajoute à la base de données le cotenu des fichiers .shp du path
        ATTENTION La classe fonctionne qu'avec les fichiers issus de l'IGN

        Parameters
        ----------
        path : str
            Chemin où se situent les fichiers .shp

        annee : int
            Année de création du fichier .shp

        reinitialiser : bool
            Si vrai, réinitialise toutes les données de la bdd

        attrib_zones_zonages : bool
            Si vrai, on attribu au zonages leurs zones, pas besoin si on ne veut que crée la bdd

        precision : int
            nombre de décimaux gardés lors du stockage, maximum 7

        given_dict : dict
            S'il n'est pas vide, il fournit l'information de l'hiérarchie des zones se situant
            dans le fichier data.txt. Exemple : {"REGION": "DEPARTEMENT"}

        """
        self.precision = precision

        self.path_file = path

        # on trouve l'annee grace au chemin
        self.annee = annee

        # on regarde la structure hierarchique par rapport aux noms qui sont dans la base
        # ainsi que ceux aui sont au fichier
        if given_dict == dict():
            hierarchie_dict = self.recherche_hierarchie()
            self.create_hierarchie(hierarchie_dict)
        else:
            self.create_hierarchie(given_dict)
        if not self.verification_existance_bdd() or reinitialiser:
            ResetDatabase().lancer()

        # on créee les zonages
        self.__creer_zonages()

        # on créee les zones
        self.__creer_zones(attrib_zones_zonages)

    @log
    def __creer_zonages(self):
        """Crée les zonages presents dans le dict hierarchique et les fichiers .shp fournis"""
        # init dic stockant zonages
        self.zonages = dict()
        # init dict qui a nom zonage associe id
        self.__dict_nom_zonage_id = dict()
        # on prend copie dict hierarchique
        hierarchie_dict = self.hierarchie_dict
        # on obtient les noms qui ne possedent pas de mere et on stocke
        noms_zonage_mere_traitee = set(hierarchie_dict.values()) - set(hierarchie_dict.keys())
        # on initialise une variable flag
        FLAG = True
        # tant qu'il reste des noms de zonage sans traité on fait:
        while len(noms_zonage_mere_traitee) > 0:

            # on prend un nom parmi ceux dont la mere à était traité
            nom_zonage = noms_zonage_mere_traitee.pop()
            print(f"Rentrant zonage: {nom_zonage}")
            # on regarde si le zonage contient un zonage mere (déjà traité par def de la var)
            if nom_zonage in self.hierarchie_dict.keys():

                # on prend le nom du zonage mere
                nom_zonage_mere = self.hierarchie_dict[nom_zonage]
                # on prend le zonage mere
                zonage_mere = self.zonages[nom_zonage_mere]
            else:
                # sinon, pas de zonage mere
                zonage_mere = None

            # on cree le nouveau zonage, on ne lui affecte pas de zones,
            # pas besoin pour creer la table
            zonage = Zonage(nom_zonage, [], zonage_mere)
            # on enregistre le zonage a la bdd
            id_zonage = ZonageDAO().creer(zonage)
            # on stocke l'id zonage dans le dict __dict_nom_zonage_id
            self.__dict_nom_zonage_id[nom_zonage] = id_zonage
            # on stcok le zonage dans le dict des zonages
            self.zonages[nom_zonage] = zonage

            # on enleve les relations exposant la nouvelle mere
            if len(hierarchie_dict) == 1 and FLAG:
                # on est a la tête du graph, il ne reste aue la variable sans fille
                noms_zonage_mere_traitee = set(hierarchie_dict.keys())
                hierarchie_dict = {}
                # on change la valeur du FLAG
                FLAG = False
            # on enleve les entrées du dict dont la valeur est nom_zonnage, car déjà traité"
            hierarchie_dict = {
                key: val for key, val in hierarchie_dict.items() if val != nom_zonage
            }

            if len(noms_zonage_mere_traitee) == 0 and FLAG:
                noms_zonage_mere_traitee = set(hierarchie_dict.values()) - set(
                    hierarchie_dict.keys()
                )

    @log
    def __creer_zones(self, attrib_zones_zonages: bool):
        """Crée les zones presents dans le dict hierarchique et les fichiers .shp fournis"""

        # initialisation du dict donnant l'ordre de traitement des zonages
        hierarchie_dict = self.hierarchie_dict_reverse
        # init dict stockant les zones déjà traités
        self.zones = dict()
        # init variable des zonages uniques
        unique_values = {item for sublist in hierarchie_dict.values() for item in sublist}
        # init variable des zonages les plus petits, au sense de l'hierarchie, non traitées
        noms_zonages_plus_petits = unique_values - set(hierarchie_dict.keys())
        # init du flag
        FLAG = True
        while len(noms_zonages_plus_petits) > 0:
            # on prend un nom parmi ceux aui n'ont pas de fille
            nom_zonage = noms_zonages_plus_petits.pop()

            # on ouvre la nouvelle zone avec fiona
            # on obtient le multipolygone, population, code_insee et annee
            with fiona.open(self.path_file + "/" + nom_zonage + ".shp", "r") as raw_zones:

                # Ajout des points dans la table de points s'ils ne sont pas presents
                # tout en gardant leur id a fin de pouvoir coder le contour

                insee_prefixe = nom_zonage[:3].upper()
                if nom_zonage in self.hierarchie_dict:
                    insee_prefixe_mere = self.hierarchie_dict[nom_zonage][:3].upper()
                else:
                    insee_prefixe_mere = None

                for raw_zone in raw_zones:

                    # Construction de la zone
                    if "NOM" in raw_zone["properties"]:
                        nom = raw_zone["properties"]["NOM"]
                        print(f"Rentrant zone: {nom} du zonage: {nom_zonage}")
                    elif "NOM_DEPT" in raw_zone["properties"]:
                        nom = raw_zone["properties"]["NOM_DEPT"]
                    else:
                        nom = None

                    if "INSEE_" + insee_prefixe in raw_zone["properties"]:
                        code_insee = raw_zone["properties"]["INSEE_" + insee_prefixe]
                    elif "CODE_DEPT" in raw_zone["properties"]:
                        code_insee = raw_zone["properties"]["CODE_DEPT"]
                        insee_prefixe = "CODE_DEPT"
                    else:
                        code_insee = None

                    if "POPULATION" in raw_zone["properties"]:

                        population = raw_zone["properties"]["POPULATION"]
                    else:
                        population = None

                    if raw_zone["geometry"]["type"] == "Polygon":
                        raw_multipolygone = [raw_zone["geometry"]["coordinates"]]
                    elif raw_zone["geometry"]["type"] == "MultiPolygon":
                        raw_multipolygone = raw_zone["geometry"]["coordinates"]
                    else:
                        raw_multipolygone = None

                    # on transforme le raw multipolygone en multipolygone objet
                    multipolygone = self.get_multipolygone(raw_multipolygone)

                    # on s'interesse ensuite a la zone mere, pour cela, seules infos:
                    # l'année et insee mere dont on regarde l'existance
                    if insee_prefixe_mere is not None:
                        if "INSEE_" + insee_prefixe_mere in raw_zone["properties"]:
                            code_insee_mere = raw_zone["properties"]["INSEE_" + insee_prefixe_mere]
                        else:
                            code_insee_mere = None

                    if str(code_insee) in self.zones:
                        # sont stockées dans la bdd
                        zones_fille = self.zones[str(code_insee)]
                    else:
                        # sont pas dans la bdd
                        zones_fille = None

                    zone = Zone(nom, multipolygone, population, code_insee, self.annee, zones_fille)

                    # on enregistre la zone dans les zonages
                    if isinstance(self.zonages[nom_zonage], Zonage) and attrib_zones_zonages:
                        self.zonages[nom_zonage]._zones.append(zone)

                    # on enregistre le zonage a la bdd
                    if nom_zonage not in ["REGION", "DEPARTEMENT"]:
                        if self.__dict_nom_zonage_id[nom_zonage] is not None:
                            ZoneDAO().creer(zone, self.__dict_nom_zonage_id[nom_zonage])
                        else:
                            ZoneDAO().creer(zone, None)

                    # on enregistre zone dans 'ensemble de zones pour qu'elle puiss etre reutiliser
                    # dans la suite
                    if code_insee_mere is not None:
                        if code_insee_mere in self.zones:
                            zone._multipolygone = None
                            self.zones[code_insee_mere].append(zone)
                        else:
                            self.zones[code_insee_mere] = [zone]

            # on enleve les relations exposant la nouvelle mere, même procedure aue zonage
            if len(hierarchie_dict) == 1 and FLAG:
                noms_zonages_plus_petits = {list(hierarchie_dict.keys())[0]}
                FLAG = False
            elif FLAG:
                new_hierarchie_dict = dict()

                for key, val in hierarchie_dict.items():
                    if nom_zonage in val:
                        val.remove(nom_zonage)
                    if val != []:
                        new_hierarchie_dict[key] = val

                hierarchie_dict = new_hierarchie_dict

                if len(noms_zonages_plus_petits) == 0:
                    noms_zonages_plus_petits = set(i[0] for i in hierarchie_dict.values()) - set(
                        hierarchie_dict.keys()
                    )
            else:
                noms_zonages_plus_petits = {}

    def get_multipolygone(self, raw_multipolygone):
        """renvoie un raw_multipolygone en type multipolygone (list list list tuple)"""
        if raw_multipolygone is None:
            return None

        liste_polygones = []

        n = len(raw_multipolygone)
        i = 1
        for polygone in raw_multipolygone:
            print(f"Polygone {i}/{n}")
            i += 1

            liste_cotours = []
            for contour in polygone:
                liste_points = []

                for point in contour:
                    x = round(float(point[0]), self.precision)
                    y = round(float(point[1]), self.precision)
                    liste_points.append(P(x, y))

                liste_cotours.append(C(points=liste_points))

            liste_polygones.append(Poly(contours=liste_cotours))
        return Mpoly(polygones=liste_polygones)

    @log
    def recherche_hierarchie(self):
        """
        Constitue le dict hierarchique des données presentes dans le path (fichiers .shp)
        à l'aide des infos fournies dans le fichier hierarchie_zonages.txt
        """

        hierarchie_dict = {}
        try:
            with open(
                "//filer-eleves2/id2475/ENSAI_ProjetInfo2A/data/hierarchie_zonages.txt", "r"
            ) as file:
                hierarchie_dict = json.load(file)
        except Exception as e:
            logging.info(e)
            raise

        return hierarchie_dict

    @log
    def create_hierarchie(self, hierarchie_dict):
        # key est la fille, argument est la mere
        self.__hierarchie_dict = hierarchie_dict
        self.__noms_dict = list(hierarchie_dict.keys())

        for i in hierarchie_dict.values():
            if i not in self.noms_dict:
                self.__noms_dict.append(i)

        hierarchie_dict_revers = dict()
        # on decide d'inversée le dict, cette fois ci, on aura du str -> list[str]
        for k, v in hierarchie_dict.items():
            if v not in hierarchie_dict_revers:
                hierarchie_dict_revers[v] = [k]  # Init nouvelle liste avec les arguments
            else:
                hierarchie_dict_revers[v].append(k)

        self.__hierarchie_dict_revers = hierarchie_dict_revers

    @log
    def inserer(self):
        """
        Fonction
        """
        self.creer_zonage()
        self.creer_zonage_mere()

    @property
    def hierarchie_dict(self):
        return self.__hierarchie_dict

    @property
    def hierarchie_dict_reverse(self):
        return self.__hierarchie_dict_revers

    @property
    def noms_dict(self):

        return self.__noms_dict


if __name__ == "__main__":
    test_class = AjouterDonneesParPath()
    path = "//filer-eleves2/id2475/ENSAI_ProjetInfo2A/ADE_3-2_SHP_WGS84G_FRA-ED2024-10-16"
    test_class.creer(path, 2024, True, precision=6)
