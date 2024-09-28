skinparam linetype polyline
skinparam linetype ortho

@startuml
object Zonage{
<b> {Static} id: int
nom: str
}

object Zone{
<b> {Static} id: int 
{Static}//#id_polygone: int //
nom: str
population: int
}

object ZoneMultipolygone{
{Static}//#id_multipolygone: int//
{Static}//#id_zone: int//
année: int
}

object MultiPolygone{
<b> {Static} id: int
{Static}//#id_polygone: int//
}

object Polygone{
<b> {Static} id: int
{Static}//#id_contour: int//
}

object Contour{
<b> {Static} id: int
{Static}//#id_point: int//
}

object Point{
<b> {Static} id: int
x: float
y: float
}
object EstCreux{
{Static}//#id_contour: int//
{Static}//#id_polygone: int//
est_creux: bool
}

object Ordre{
{Static}//#id_point: int//
{Static}//#id_contour: int//
cardinal: int

}

object ZoneFille{
{Static}//#id_zone_mere: int//
{Static}//#id_zone_fille: int//
}

object ZonageMere{
{Static}//#id_zone_mere: int//
{Static}//#id_zone_fille: int//
}
Zonage "1"-- "0, 1" ZonageMere

MultiPolygone "*" -- "*" Zone
(MultiPolygone, Zone) .. ZoneMultipolygone

Contour "*" -- "1" Polygone
(Contour, Polygone) .. EstCreux

Contour "1" -right- "*" Point
(Contour, Point) .. Ordre

Zone "1" -down- " * " ZoneFille
Zone "1" -right- "*" Zonage
MultiPolygone "1"-right-"*" Polygone


@enduml