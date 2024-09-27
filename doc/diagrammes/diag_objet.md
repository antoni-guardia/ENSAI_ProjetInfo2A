@startuml
object Zonage{
id: int
nom: str
id_zonage_mere: int
}

object Zone{
id: int 
id_zones_fils: int
id_polygone: int

}

object ZonageZone{
id_zonage: int
id_zone: int
année: int
}

object MultiPolygone{
id: int
id_polygone: int
}

object Polygone{
id: int
id_contour: int
}

object Contour{
id: int
id_point: int
}

object Point{
id: int
x: float
y: float
}
object EstCreux{
id_contour: int
id_polygone: int
est_creux: bool
}

object Ordre{
id_point
id_contour
cardinal

}

Zonage "1"--> "0, 1" Zonage

MultiPolygone "*" - "*" Zone
(MultiPolygone, Zone) .. ZonageZone

Contour "*" -- "1" Polygone
(Contour, Polygone) .. EstCreux

Contour "1" -- "*" Point
(Contour, Point) .. Ordre

Zone "1" -> "*" Zone
Zone "1" -> "*" Zonage
MultiPolygone "1"--"*" Polygone


@enduml