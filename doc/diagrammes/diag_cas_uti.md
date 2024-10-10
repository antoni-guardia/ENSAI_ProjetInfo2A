@startuml
left to right direction
actor "Utilisateur" as usr
actor "Administrateur" as admin
rectangle API {
  usecase "Informations sur les subdivisions" as UC1
  usecase "Zone d'appartenance d'un point" as UC2
  usecase "Zones d'appartenance d'un ensemble de points" as UC3
  usecase "Télechargement carte" as UC3
}
usr --> UC1
usr --> UC2
UC2 --> UC3

@enduml