skinparam linetype polyline
skinparam linetype ortho

@startuml
object Zonage{
<b> {Static} id: int
nom: str
}

object Zone{
<b> {Static} id: int 
{Static}//#id_zonage//
nom: str
population: int
code_insee: int or None
année: int
cle_hash: int

}

object MultiPolygone{
{Static}//#id_polygone: int//
{Static}//#id_zone: int//

}



object Polygone{
<b> {Static} id: int
cle_hash: int
}

object Contour{
<b> {Static} id: int
cle_hash: int
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
{Static}//#id_zonage_mere: int//
{Static}//#id_zonage_fille: int//
}
Zonage "1"-- "0, 1" ZonageMere

Polygone "*" -- "1" Zone
(Polygone, Zone) .. MultiPolygone

Contour "*" -- "*" Polygone
(Contour, Polygone) .. EstEnclave

Contour "*" -right- "*" Point
(Contour, Point) .. Ordre

Zone "1" -down- " * " ZoneFille
Zone "1" -right- "*" Zonage


@enduml