@startuml

class Zone {
 - nom : str
 - multipolygone : MultiPolygone
 - zones_filles : list[Zone] or None
 - code_insee : int or None
 - point_dans_zone(point: tuple) -> bool
 - surface_zone() -> float 
 }

class Zonage {
 - nom : str
 - zonage_mere : Zonage or None
 - année : str
 - zones : List[Zone]
 - trouver_zone(point: tuple, type_coord: str) -> str
 - trouver_zones(point: list[tuple], type_coord: str) -> list[str]
 - trouver_zone_chemin(point: tuple, type_coord: str) -> str
 - trouver_zones_chemins(point: list[tuple], type_coord: str) -> list[str]
 }

class MultiPolygone{
 - polygones : List[Polygone]
 - est_dedans(point: tuple) -> bool
 }


class Polygone{
 - contours : List[Contour] 
 - est_dedans(point: tuple) -> bool
 - recherche_points_extremums()
 - point_dans_rectangle(point: tuple) -> bool
}

class Contour{
 - points : List[Point]
 - est_dedans(point: tuple) -> bool
}

class Point{
 - x : float
 - y : float
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
Polygone "*"-down->"1, 0" MultiPolygone



Zone "*"-down->"1, 0" Zone
Zonage "1"-down->"1, 0" Zonage


Zone *-left- MultiPolygone
Zone -right-* Zonage

Zonage <|.. DAO : Crée

DBConnection <|.up. DAO : Utilise
LecteurFichierSHP <|.up. Service : Utilise
Service -> DAO : Appel
@enduml
