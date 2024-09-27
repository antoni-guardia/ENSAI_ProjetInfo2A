@startuml

class Zone {
 - {Static} id_zone : int
 - nom : str
 - id_zones_filles : list[int] or None
 - point_dans_zone(point: tuple) -> bool
 - surface_zone() -> float 
 }

class Zonage {
 - {Static} id_zonage : int
 - nom : str
 - id_zonage_mere : int or None
 - année : str
 - trouver_zone(point: tuple, type_coord: str) -> str
 - trouver_zones(point: list[tuple], type_coord: str) -> list[str]
 - trouver_zone_chemin(point: tuple, type_coord: str) -> str
 - trouver_zones_chemins(point: list[tuple], type_coord: str) -> list[str]
 }

class MultiPolygone{
 - {Static} id_multipolygone
 - est_dedans(point: tuple) -> bool
 }


class Polygone{
 - {Static} id_polygone

 - est_dedans(point: tuple) -> bool
 - recherche_points_extremums()
 - point_dans_rectangle(point: tuple) -> bool
}

class Contour{
 - {Static} id_contour
 - est_dedans(point: tuple) -> bool
}

class Point{
 - {Static} id_point
 - x 
 - y
}

class DAO{
  - creer_classes()
  - trouver_zonage_par_annee(annee: int) -> List(Zonage)
  - trouver_zone_par_id(id: int) -> Zone
  - mettre_a_jour(Zonage) -> Zonage
  - supprimer(Zonage) -> bool
}



class DBConnection{
- connection()
}

class LecteurFichierSHP{
- lecture(chemin :str)
}

class Service{
- reinitialiser_bdd()
- ajouter_donnes()
- recherche_zonage(point: tuple, annee: int, type_cord: str)
}

Contour -right-* Point
Contour --* Polygone
Polygone "1"-down-*"1" MultiPolygone
Polygone "*"-down-"1" MultiPolygone

Zone *-left- MultiPolygone
Zone -right-* Zonage

Zonage <|.. DAO : Crée

DBConnection <|.up. DAO : Utilise
LecteurFichierSHP <|.up. Service : Utilise
Service -> DAO : Appel
@enduml
