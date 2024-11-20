import typer
import inquirer
from pyfiglet import figlet_format
from yaspin import yaspin
import requests
from service.joueur_service import JoueurService

# Define a Typer app
app = typer.Typer()


def show_ascii_header(text):
    """
    Affiche une en-tête ASCII stylisée.
    """
    ascii_art = figlet_format(text)
    print(ascii_art)


def fetch_data():
    """
    Simule une requête pour récupérer des données.
    """
    url = "https://jsonplaceholder.typicode.com/todos/1"  # Exemple d'API
    with yaspin(text="Fetching data...", color="cyan") as spinner:
        response = requests.get(url)
        spinner.ok("✔")  # Stop spinner with success mark
        return response.json()


def modify_database(action):
    """
    Simule une action de modification de la base de données en fonction du choix.
    """
    if action == "Utilisateur":
        print("Modification des utilisateurs dans la BDD.")
    elif action == "Login":
        print("Mise à jour des informations de connexion.")
    elif action == "Réinitialiser la BDD":
        print("Base de données réinitialisée.")
    elif action == "Ajouter des données dans la BDD":
        add_data_options = [
            "Modifier Path",
            "Modifier Hiérarchie",
            "Lancer",
            "(Retour)",
        ]
        answer = inquirer.prompt([
            inquirer.List(
                "add_action",
                message="Choisissez une action pour ajouter des données :",
                choices=add_data_options,
            )
        ])
        if answer and answer["add_action"] == "(Retour)":
            return
        elif answer:
            print(f"Action sélectionnée : {answer['add_action']}")


def service_functions(action):
    """
    Simule une fonction de service en fonction du choix.
    """
    if action == "Joueur":
        print("Traitement de la fonctionnalité joueur.")
    elif action == "Carte":
        print("Traitement de la fonctionnalité carte.")
    elif action == "Fichier":
        print("Gestion des fichiers.")
    elif action == "Recherche Point":
        print("Exécution de la recherche de points.")
    elif action == "(Retour)":
        return


def main_menu():
    """
    Affiche le menu principal avec deux couches d'options.
    """
    while True:
        # Premier Layer
        first_layer_options = [
            "Faire une requête dans la BDD",
            "Modifier la BDD",
            "Quitter",
        ]
        first_layer_answer = inquirer.prompt([
            inquirer.List(
                "first_layer_action",
                message="Que voulez-vous faire ?",
                choices=first_layer_options,
            )
        ])

        if first_layer_answer["first_layer_action"] == "Quitter":
            print("Au revoir !")
            return False

        # Deuxième Layer
        if first_layer_answer["first_layer_action"] == "Faire une requête dans la BDD":
            while True:
                service_options = [
                    "Joueur",
                    "Carte",
                    "Fichier",
                    "Recherche Point",
                    "(Retour)",
                ]
                service_answer = inquirer.prompt([
                    inquirer.List(
                        "service_action",
                        message="Choisissez une fonction de service :",
                        choices=service_options,
                    )
                ])
                if service_answer and service_answer["service_action"] == "(Retour)":
                    break
                elif service_answer:
                    service_functions(service_answer["service_action"])

        elif first_layer_answer["first_layer_action"] == "Modifier la BDD":
            while True:
                modify_options = [
                    "Utilisateur",
                    "Login",
                    "Réinitialiser la BDD",
                    "Ajouter des données dans la BDD",
                    "(Retour)",
                ]
                modify_answer = inquirer.prompt([
                    inquirer.List(
                        "modify_action",
                        message="Choisissez une action de modification :",
                        choices=modify_options,
                    )
                ])
                if modify_answer and modify_answer["modify_action"] == "(Retour)":
                    break
                elif modify_answer:
                    modify_database(modify_answer["modify_action"])

    return True


@app.command()
def main():
    """
    Point d'entrée principal de l'application.
    """
    show_ascii_header("Vous êtes ici")
    running = True
    while running:
        running = main_menu()


if __name__ == "__main__":
    app()
