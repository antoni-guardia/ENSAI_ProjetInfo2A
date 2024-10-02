skinparam linetype polyline
skinparam linetype ortho

@startuml
object Zonage{
<b> {Static} id: int
nom: str
}

object Zone{
<b> {Static} id: int 
nom: str
population: int
code_insee: int or None
}

object MultiPolygone{
{Static}//#id_polygone: int//
{Static}//#id_zone: int//
année: int
}



object Polygone{
<b> {Static} id: int
}

object Contour{
<b> {Static} id: int
}

object Point{
<b> {Static} id: int
x: float
y: float
}
object EstEnclave{
{Static}//#id_contour: int//
{Static}//#id_polygone: int//
est_enclave: bool
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

Polygone "*" -- "*" Zone
(Polygone, Zone) .. MultiPolygone

Contour "*" -- "1" Polygone
(Contour, Polygone) .. EstEnclave

Contour "1" -right- "*" Point
(Contour, Point) .. Ordre

Zone "1" -down- " * " ZoneFille
Zone "1" -right- "*" Zonage


@enduml