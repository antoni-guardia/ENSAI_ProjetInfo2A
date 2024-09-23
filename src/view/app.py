import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from utils.log_init import initialiser_logs

from service.joueur_service import JoueurService

app = FastAPI(title="Vous êtes ici webservice")


initialiser_logs("Webservice")

joueur_service = JoueurService()


@app.get("/utilisateur/", tags=["Utilisateur"])
async def lister_tous_joueurs():
    """Lister tous les utilisateurs
    GET http://localhost/utilisateurs
    """
    logging.info("Lister tous les utilisateurs")
    liste_joueurs = joueur_service.lister_tous()

    liste_model = []
    for joueur in liste_joueurs:
        liste_model.append(joueur)

    return liste_model


@app.get("/joueur/{id_joueur}", tags=["Joueurs"])
async def joueur_par_id(id_joueur: int):
    """Trouver un joueur à partir de son id
    GET http://localhost/joueur/3
    """
    logging.info("Trouver un joueur à partir de son id")
    return joueur_service.trouver_par_id(id_joueur)


class JoueurModel(BaseModel):
    """Définir un modèle Pydantic pour les Joueurs"""

    id_joueur: int | None = None  # Champ optionnel
    pseudo: str
    mdp: str
    age: int
    mail: str
    fan_pokemon: bool


@app.post("/joueur/", tags=["Joueurs"])
async def creer_joueur(j: JoueurModel):
    """Créer un joueur"""
    logging.info("Créer un joueur")
    if joueur_service.pseudo_deja_utilise(j.pseudo):
        raise HTTPException(status_code=404, detail="Pseudo déjà utilisé")

    joueur = joueur_service.creer(j.pseudo, j.mdp, j.age, j.mail, j.fan_pokemon)
    if not joueur:
        raise HTTPException(status_code=404, detail="Erreur lors de la création du joueur")

    return joueur


@app.put("/joueur/{id_joueur}", tags=["Joueurs"])
def modifier_joueur(id_joueur: int, j: JoueurModel):
    """Modifier un joueur"""
    logging.info("Modifier un joueur")
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    joueur.pseudo = j.pseudo
    joueur.mdp = j.mdp
    joueur.age = j.age
    joueur.mail = j.mail
    joueur.fan_pokemon = j.fan_pokemon
    joueur = joueur_service.modifier(joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Erreur lors de la modification du joueur")

    return f"Joueur {j.pseudo} modifié"


@app.delete("/joueur/{id_joueur}", tags=["Joueurs"])
def supprimer_joueur(id_joueur: int):
    """Supprimer un joueur"""
    logging.info("Supprimer un joueur")
    joueur = joueur_service.trouver_par_id(id_joueur)
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    joueur_service.supprimer(joueur)
    return f"Joueur {joueur.pseudo} supprimé"


@app.get("/hello/{name}")
async def hello_name(name: str):
    """Afficher Hello"""
    logging.info("Afficher Hello")
    return f"message : Hello {name}"


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)

    logging.info("Arret du Webservice")