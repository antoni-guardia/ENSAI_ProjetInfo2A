@startuml

start

:Entrer les coordonnées;

if (Point Unique?) then (oui)
    :Appeler Zonage.trouver_zone(point);
    :Récupérer les informations de la zone;
    :Retourner les informations sur la zone;

else (non)
    :Appeler Zonage.trouver_zones(points);
    :Récupérer les informations pour chaque point;
    :Formatter les résultats (CSV, JSON, etc.);
    :Retourner le fichier formaté;
endif

if (Ajouter des zonages ou des années?) then (oui)
    :Appeler les méthodes respectives pour ajouter des zonages ou des années;
endif

end

@enduml
