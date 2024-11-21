import typer
import inquirer
from pyfiglet import figlet_format

from dao.zone_dao import ZoneDAO

from service.services_trouver_zone_par import ServicesRechercheZone
from service.services_recherche_point import ServicesRecherchePoint

app = typer.Typer()


def show_ascii_header(text):
    """
    Display a stylized ASCII header.
    """
    ascii_art = figlet_format(text)
    print(ascii_art)


def main_menu():
    """
    Main menu: allows the user to choose between "Faire une requête" or "Modifier des données".
    """
    questions = [
        inquirer.List(
            "main_action",
            message="Que souhaitez-vous faire ?",
            choices=["Faire une requête", "Modifier des données", "Exit"],
        )
    ]
    answers = inquirer.prompt(questions)
    return answers.get("main_action") if answers else None


def request_menu():
    """
    Submenu for "Faire une requête".
    """
    questions = [
        inquirer.List(
            "request_action",
            message="Que souhaitez-vous faire ?",
            choices=["Sélectionner une année", "Retour"],
        )
    ]
    answers = inquirer.prompt(questions)
    return answers.get("request_action") if answers else None


def modify_data_menu():
    """
    Submenu for "Modifier des données".
    """
    questions = [
        inquirer.List(
            "modify_action",
            message="Que souhaitez-vous faire ?",
            choices=[
                "Afficher les utilisateurs",
                "Créer un utilisateur",
                "Se connecter",
                "Retour",
            ],
        )
    ]
    answers = inquirer.prompt(questions)
    return answers.get("modify_action") if answers else None


def after_login_menu():
    """
    Submenu displayed after logging in.
    """
    questions = [
        inquirer.List(
            "post_login_action",
            message="Que souhaitez-vous faire ?",
            choices=["Modifier path", "Modifier hiérarchie", "Insérer des données", "Retour"],
        )
    ]
    answers = inquirer.prompt(questions)
    return answers.get("post_login_action") if answers else None


def annee_menu():
    """
    Menu displayed at annee.
    """
    questions = [
        inquirer.List(
            "menu_action",
            message="Quelle année voulez-vous choisir ?",
            choices=ZoneDAO().annees_disponibles() + ["Retour"],
        )
    ]
    answers = inquirer.prompt(questions)
    return answers.get("menu_action") if answers else None


def sub_annee_menu():
    """
    Submenu displayed after menu.
    """
    questions = [
        inquirer.List(
            "post_menu_action",
            message="Que souhaitez-vous faire ?",
            choices=[
                "Recherche zone par nom",
                "Recherche info. zone par code INSEE",
                "Trouver zone appartenant à un point",
                "Enregistrer une zone dans un fichier",
                "Retour",
            ],
        )
    ]
    answers = inquirer.prompt(questions)
    return answers.get("post_menu_action") if answers else None


def create_user():
    """
    Submenu for creating a user: prompts for name and password.
    """
    name = typer.prompt("Entrez le nom de l'utilisateur")
    password = typer.prompt("Entrez le mot de passe", hide_input=True)
    print(f"Création de l'utilisateur : {name} avec le mot de passe : {password}")  # Placeholder


def login():
    """
    Handle user login.
    """
    username = typer.prompt("Entrez votre nom d'utilisateur")
    password = typer.prompt("Entrez votre mot de passe", hide_input=True)
    print(f"Connexion réussie pour : {username}")  # Placeholder for actual login validation

    while True:
        post_login_action = after_login_menu()
        if post_login_action == "Modifier path":
            print("Fonctionnalité : Modifier path.")  # Placeholder
        elif post_login_action == "Modifier hiérarchie":
            print("Fonctionnalité : Modifier hiérarchie.")  # Placeholder
        elif post_login_action == "Insérer des données":
            print("Fonctionnalité : Insérer des données.")  # Placeholder
        elif post_login_action == "Retour":
            break


def annee_choisi():
    while True:
        annee = int(annee_menu())
        if annee == "Retour":
            break
        else:
            while True:
                post_menu_action = sub_annee_menu()
                if post_menu_action == "Recherche zone par nom":
                    nom = typer.prompt("Entrez nom de zone")
                    resultat_zone = ServicesRechercheZone().tout_par_nom(nom, annee)
                    print(resultat_zone)
                elif post_menu_action == "Recherche info. zone par code INSEE":
                    code_insee = typer.prompt("Entrez un code INSEE")
                    resultat_zone = ServicesRechercheZone().tout_par_code_insee(code_insee, annee)
                    print(resultat_zone)
                elif post_menu_action == "Trouver zone appartenant à un point":
                    resultat_zonage = typer.prompt("Entrez nom de zonage")
                    coord_x = typer.prompt("Entrez la latitude")
                    coord_y = typer.prompt("Entrez la longitude")
                    resultat_zone = ServicesRecherchePoint().trouver_zone_point(
                        resultat_zonage, float(coord_x), float(coord_y)
                    )
                    print(resultat_zone)
                elif post_menu_action == "Enregistrer une zone dans un fichier":
                    print("aores")  # Après
                elif post_menu_action == "Retour":
                    break


@app.command()
def main():
    """
    Main entry point for the CLI application.
    """
    show_ascii_header("VOUS ETES ICI")
    while True:
        main_choice = main_menu()
        if main_choice == "Faire une requête":
            while True:
                request_choice = request_menu()  # Placeholder
                if request_choice == "Sélectionner une année":
                    annee_choisi()
                elif request_choice == "Retour":
                    break

        elif main_choice == "Modifier des données":
            while True:
                modify_choice = modify_data_menu()
                if modify_choice == "Afficher les utilisateurs":
                    print("Fonctionnalité : Afficher les utilisateurs.")  # Placeholder
                elif modify_choice == "Créer un utilisateur":
                    create_user()
                elif modify_choice == "Se connecter":
                    login()
                elif modify_choice == "Retour":
                    break

        elif main_choice == "Exit":
            typer.echo("Au revoir !")
            break


if __name__ == "__main__":
    app()
