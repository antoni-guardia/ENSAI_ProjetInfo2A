@startuml

class Zone {
 + {Static} id_zone : int
 + nom : str
 + id_multipolygone : int
 + id_zones_filles : list[int] or None
 + point_dans_zone(point: tuple) -> bool
 + surface_zone() -> float 
 }

class Zonage {
 + {Static} id_zonage : int
 + nom : str
 + id_zonage_mere : int or None
 + année : str
 + trouver_zone(point: tuple, type_coord: str) -> str
 + trouver_zones(point: list[tuple], type_coord: str) -> list[str]
 + trouver_zone_chemin(point: tuple, type_coord: str) -> str
 + trouver_zones_chemins(point: list[tuple], type_coord: str) -> list[str]
 }

class MultiPolygone{
 + {Static} id_multipolygone
 + contour : list[list[list[tuple]]]
 + est_dedans(point: tuple)
 - recherche_points_extremums()
 - point_dans_rectangle(point: tuple) -> bool
 - point_dans_polygone(point: tuple) -> bool
 - point_dans_multipolygone(point: tuple) -> bool
 }




Zone -down-* MultiPolygone
Zone *- Zonage


@enduml
