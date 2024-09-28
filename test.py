import fiona


class traitement_data:
    def __init__(self, path=("/home/rogerbernat/Documents/ENSAI_ProjetInfo2A/ADMIN-EXPRESS_3-2__"
                             "SHP_LAMB93_FXX_2024-09-18/ADMIN-EXPRESS/1_DONNEES_LIVRAISON_2024-09"
                             "-00118/ADE_3-2_SHP_LAMB93_FXX-ED2024-09-18/")):

        self.path = path
        self.__multipolygones = dict()
        self.__multipolygones_id = 0
        self.__zones = dict()
        self.__zones_id = 0
        self.__zonages = dict()
        self.__annee = self.trouver_annee()

    def trouver_annee(self):
        pass

    def cahrgement_zones_commune(self):

        self.__zonages[0] = {"nom": "communes",
                             "id_zonage_mere": 1,
                             "annee": self.__annee
                             }

        self.__arrondissement_commune = dict()

        with fiona.open(self.path + "COMMUNE.shp", 'r') as shp:

            for feature in shp:
                if feature["geometry"]["type"] == "Polygon":
                    commune_multi = [feature["geometry"]["coordinates"]]
                else:
                    commune_multi = feature["geometry"]["coordinates"]

                self.__multipolygones[self.__multipolygones_id] = commune_multi
                commune_nom = feature["properties"]["NOM"]


                print(feature)
                commune_arrodissement = int(feature["properties"]["INSEE_ARR"])

                self.__zones[self.__zones_id] = {"id_zone": self.__zones_id,
                                            "nom": commune_nom,
                                            "id_multipolygone": self.__multipolygones_id,
                                            "id_zones_filles": None,
                                            "id_zonage": 0
                                            }

                if commune_arrodissement not in self.__arrondissement_commune.keys():
                    self.__arrondissement_commune[commune_arrodissement] = [self.__zones_id]
                else:
                    self.__arrondissement_commune[commune_arrodissement].append(commune_id)

                self.__multipolygones_id += 1


if __name__ == "__main__":
    bdd = traitement_data()
    bdd.cahrgement_zones_commune()
