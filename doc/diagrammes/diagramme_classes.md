@startuml

class Zone {
 +nom : str
 +id_zone : str
 -extension : Multipolygone
 +id_zone_mere : int or None
 +id_zone_fille : int or None
 +est_dans_rectangle()
 +surface_zone()
 +est_dedans(points, type_coord)
 }
 
 class Zonage {
 +nom : str
 #id_zonage : int
 #id_zones : list[int]
 +id_zonage_mere : int or None
 +id_zonage_fille : int or None
 +année : str
 +trouver_zone(points, type_coord)
 }
 
 class Multipolygone{
 + contour : list[tuple]
 + exclaves : list[Multipolygone] or None 
 + est_dedans(points)
 }
 
 Zone *- Zonage
 Zone -* Multipolygone
@enduml