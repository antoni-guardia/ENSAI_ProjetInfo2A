@startuml
|Utilisateur|

:Envoie requête à l'API;

|API|

:Vérification du type de requête;

switch (Type de requête)
    case (F1: Consultation par URI)
        :Cherche informations de la zone;
        :Renvoie les informations sur la zone demandée;
        break

    case (F2: Localisation d'un point)
        :Identifie la zone correspondant aux coordonnées fournies;
        :Renvoie les informations sur la zone où se trouve le point;
        break

    case (F3: Localisation d'une liste de points)
        :Traite la liste de points;
        :Détermine les zones pour chaque point;
        :Génère et renvoie un fichier (csv, xlsx, json, etc.);
        break
endswitch

|Utilisateur|

:Reçoit les informations demandées;
@enduml