@startuml

|Utilisateur|

:Envoie requête à l'API;

 

|API|

:Vérification du type de requête;

 

switch (Type de requête)

    case (F1: URI de consultation)

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

        :Génère un fichier (csv, xlsx, json, etc.);

        :Renvoie le fichier avec les résultats;

        break

    case (Requête non reconnue)

        :Erreur - Requête non reconnue;

        break

endswitch

 

|Admin|

:Ajoute un zonage ou des années géographiques (FO1/FO2);

 

|API|

:Met à jour les données géographiques avec les nouveaux zonages ou années;

@enduml