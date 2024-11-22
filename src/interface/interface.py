import typer
import inquirer
import os
from pyfiglet import figlet_format

from dao.zone_dao import ZoneDAO
from dao.utilisateur_dao import UtilisateurDao
from service.services_trouver_zone_par import ServicesRechercheZone
from service.services_recherche_point import ServicesRecherchePoint
from service.modifier_hierarchie_dict import gestion_fichier_hierarchique
from business_object.utilisateur import Utilisateur

app = typer.Typer()


class Interface:
    def __init__(self):
        self.annee = None
        self.path_entered = None

    def show_ascii_header(self, text):
        """
        Display a stylized ASCII header.
        """
        ascii_art = figlet_format(text)
        print(ascii_art)

    def clear_screen(self):
        """
        Clears the terminal screen.
        Works for Windows, macOS, and Linux.
        """
        os.system("cls" if os.name == "nt" else "clear")

    def main_menu(self):
        """
        Main menu: allows the user to choose between "Faire une requête" or "Modifier des données".
        """
        self.clear_screen()
        self.show_ascii_header("VOUS ETES ICI")
        questions = [
            inquirer.List(
                "main_action",
                message="Que souhaitez-vous faire ?",
                choices=[
                    "Faire une requête",
                    "Modifier des données",
                    "Exit",
                ],
            )
        ]
        answers = inquirer.prompt(questions)
        return answers.get("main_action") if answers else None

    def request_menu(self):
        """
        Submenu for "Faire une requête".
        """
        self.clear_screen()
        questions = [
            inquirer.List(
                "request_action",
                message="Que souhaitez-vous faire ?",
                choices=[
                    "Sélectionner une année",
                    "Retour",
                ],
            )
        ]
        answers = inquirer.prompt(questions)
        return answers.get("request_action") if answers else None

    def modify_data_menu(self):
        """
        Submenu for "Modifier des données".
        """
        self.clear_screen()
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

    def after_login_menu(self):
        """
        Submenu displayed after logging in.
        """
        self.clear_screen()
        questions = [
            inquirer.List(
                "post_login_action",
                message="Que souhaitez-vous faire ?",
                choices=[
                    "Modifier path",
                    "Modifier hiérarchie",
                    "Insérer des données",
                    "Retour",
                ],
            )
        ]
        answers = inquirer.prompt(questions)
        return answers.get("post_login_action") if answers else None

    def annee_menu(self):
        """
        Menu displayed to select a year.
        """
        self.clear_screen()
        questions = [
            inquirer.List(
                "menu_action",
                message="Quelle année voulez-vous choisir ?",
                choices=ZoneDAO().annees_disponibles() + ["Retour"],
            )
        ]
        answers = inquirer.prompt(questions)
        return answers.get("menu_action") if answers else None

    def sub_annee_menu(self):
        """
        Submenu displayed after selecting a year.
        """
        self.clear_screen()
        questions = [
            inquirer.List(
                "post_menu_action",
                message="Que souhaitez-vous faire ?",
                choices=[
                    "Recherche zone par nom",
                    "Recherche info. zone par code INSEE",
                    "Trouver zone appartenant à un point",
                    "Retour",
                ],
            )
        ]
        answers = inquirer.prompt(questions)
        return answers.get("post_menu_action") if answers else None

    def create_user(self):
        """
        Submenu for creating a user: prompts for name and password.
        """
        name = typer.prompt("Entrez le nom de l'utilisateur")
        password = typer.prompt("Entrez le mot de passe", hide_input=True)
        if UtilisateurDao().creer(name, password):
            print("Utlisateur crée avec succès")
        else:
            print("Erreur dans la création de l'utilisateur")

    def login(self):
        """
        Handle user login.
        """
        username = typer.prompt("Entrez votre nom d'utilisateur")
        password = typer.prompt("Entrez votre mot de passe", hide_input=True)

        if UtilisateurDao().connection_reusie(Utilisateur(username, password)):
            while True:
                post_login_action = self.after_login_menu()
                if post_login_action == "Modifier path":
                    self.path_entered = typer.prompt("Entrez le path jusqu'au fichier .shp")
                elif post_login_action == "Modifier hiérarchie":
                    gestion_fichier_hierarchique().open_file_in_editor()  # Placeholder
                elif post_login_action == "Insérer des données":
                    print("Fonctionnalité : Insérer des données.")  # Placeholder
                elif post_login_action == "Retour":
                    break
        else:
            print("Mot de passe incorect veuillez le remettre")

    def annee_choisi(self):
        """
        Handles the actions related to selecting a year and performing the queries.
        """
        while True:
            annee = self.annee_menu()
            if annee == "Retour":
                break
            else:
                while True:
                    self.annee = int(annee)
                    post_menu_action = self.sub_annee_menu()
                    if post_menu_action == "Recherche zone par nom":
                        nom = typer.prompt("Entrez nom de zone")
                        resultat_zone = ServicesRechercheZone().tout_par_nom(nom, self.annee)
                        print(resultat_zone)
                    elif post_menu_action == "Recherche info. zone par code INSEE":
                        code_insee = typer.prompt("Entrez un code INSEE")
                        resultat_zone = ServicesRechercheZone().tout_par_code_insee(
                            code_insee, self.annee
                        )
                        print(resultat_zone)
                    elif post_menu_action == "Trouver zone appartenant à un point":
                        resultat_zonage = typer.prompt("Entrez nom de zonage")
                        coord_x = typer.prompt("Entrez la latitude")
                        coord_y = typer.prompt("Entrez la longitude")
                        resultat_zone = ServicesRecherchePoint().trouver_zone_point(
                            resultat_zonage, float(coord_x), float(coord_y), self.annee
                        )
                        print(resultat_zone)
                    elif post_menu_action == "Retour":
                        break

    @app.command()
    def main(self):
        """
        Main entry point for the CLI application.
        """
        while True:
            main_choice = self.main_menu()
            if main_choice == "Faire une requête":
                while True:
                    request_choice = self.request_menu()
                    if request_choice == "Sélectionner une année":
                        self.annee_choisi()
                    elif request_choice == "Retour":
                        break

            elif main_choice == "Modifier des données":
                while True:
                    modify_choice = self.modify_data_menu()
                    if modify_choice == "Afficher les utilisateurs":
                        listeuser = UtilisateurDao().lister_tous()
                        print(listeuser)
                    elif modify_choice == "Créer un utilisateur":
                        self.create_user()
                    elif modify_choice == "Se connecter":
                        self.login()
                    elif modify_choice == "Retour":
                        break

            elif main_choice == "Exit":
                typer.echo("Au revoir !")
                break


if __name__ == "__main__":
    Interface().main()
