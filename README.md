# Vous êtes ici 🎯
## Mise à jour du fichier requirements.txt
### Installation mode automatique
```
pip install -r requirements.txt
```

### Commande
```
pip freeze > requirements.txt
```
### Diagramme des Classes

![Diagramme des classes](doc/diagrammes/diagramme_classes.png)

## Sources de Données

Pour la réalisation de ce projet, nous nous appuyons sur le code officiel géographique de l'INSEE et sur les contours des différents zonages fournis par l'IGN au format Shapefile.

### Guide d'utilisation de l'interface

À son lancement, l'utilisateur est accueilli par un menu principal avec trois options :
1. Faire une requête
2. Modifier des données
3. Quitter l'application

----------------------------------------------------------
1. Faire une requête

Si l'utilisateur choisit l'option "Faire une requête", un sous-menu s'affiche, permettant de sélectionner une année et d'effectuer des recherches sur les zones en fonction de plusieurs critères :
    - Recherche par nom
    - Recherche par code INSEE
    - Recherche par coordonnées géographiques

1. 1. Sélection de l’année : L’utilisateur choisit une année parmi une liste prédéfinie. 
    
1. 2. Choix de la méthode de recherche : Après avoir sélectionné l'année, l'utilisateur peut choisir l'une des trois méthodes suivantes :
    - Recherche par nom de zone: L’utilisateur saisit le nom d’une zone géographique pour obtenir les informations associées.
    - Recherche par code INSEE : Permet de retrouver des données en entrant le code INSEE d'une zone spécifique.
    - Recherche par coordonnées géographiques : L’utilisateur fournit les coordonnées d’un point (latitude et longitude) pour identifier la zone géographique correspondante.

----------------------------------------------------------
2. Modifier des données

Dans cette section, l'utilisateur peut consulter la liste des utilisateurs existants, créer un nouvel utilisateur ou se connecter avec un utilisateur déjà enregistré. Une fois connecté, il peut accéder à plusieurs options pour gérer les données et les utilisateurs, telles que :
    - Modification du chemin d'accès aux fichiers
    - Gestion de la hiérarchie des zones géographiques
    - Insertion de nouvelles données géographiques

- Actions accessibles sans connexion :
    1. Lister les utilisateurs : Affiche la liste des utilisateurs enregistrés.
    2. Créer un utilisateur : Permet d’ajouter un nouvel utilisateur en saisissant les informations nécessaires.
    3. Se connecter : Permet à l'utilisateur de se connecter pour débloquer des options avancées.

- Actions réservées aux utilisateurs authentifiés :
    1. Changer le chemin d’accès aux données : Modifie l’emplacement des fichiers de données utilisés par l’application.
    2. Changer la hiérarchie des zones : Permet de réorganiser la structure hiérarchique des différentes zones géographiques.
    3. Insérer de nouvelles données : Ajoute des données supplémentaires dans le système, en respectant les formats et structures définis.

----------------------------------------------------------
3. Quitter l'application

L'utilisateur peut quitter l'application.