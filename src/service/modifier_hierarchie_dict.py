import subprocess
import json
import os


class gestion_fichier_hierarchique:

    def __init__(self, file_path="data\hierarchie_zonages.txt"):
        print("Current path:", os.getcwd())
        script_dir = os.path.dirname(
            os.path.realpath(__file__)
        )  # Get the directory where the script is stored
        parent_dir = os.path.dirname((os.path.dirname(script_dir)))
        self.file_path = os.path.join(parent_dir, file_path)
        print(self.file_path)

    def open_file_in_editor(self):
        """
        fonction qui permet de lire et editer le fichier hierarchique
        """
        try:
            # Check if the file exists
            contenu = self.copier_contenu_fichier()
        except FileNotFoundError:
            print(f"Error: The file '{self.file_path}' does not exist.")
            return

        # Open the file in nano or vim (or another editor of your choice)
        editor = "nano"  # You can replace with "vim" or another terminal editor
        subprocess.run([editor, self.file_path])
        if not self.is_json_compatible():
            self.vider_fichier()
            self.ajouter_contenu_fichier(contenu)

    def is_json_compatible(self):
        """
        Vérifie si le fichier est compatible avec JSON.
        """
        try:
            with open(self.file_path, "r") as f:
                # Essayer de charger le fichier JSON
                json.load(f)
            return True
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Erreur lors de la lecture JSON du fichier: {e}")
            return False

    def copier_contenu_fichier(self):
        """
        Fonction pour copier le contenu d'un fichier.
        Renvoie le contenu du fichier sous forme de chaîne de caractères.
        """
        try:
            with open(self.file_path, "r") as f:
                contenu = f.read()
            return contenu
        except FileNotFoundError:
            print(f"Erreur: Le fichier '{self.file_path}' n'existe pas.")
            return None
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier '{self.file_path}': {e}")
            return None

    def ajouter_contenu_fichier(self, contenu_ajouter):
        """
        Fonction pour ajouter du contenu à un fichier.
        Ajoute 'contenu_ajouter' à la fin du fichier spécifié par 'file_path'.
        """
        try:
            with open(self.file_path, "a") as f:
                f.write(contenu_ajouter)
            print(f"Le contenu a été ajouté avec succès à '{self.file_path}'.")
        except Exception as e:
            print(f"Erreur lors de l'ajout au fichier '{self.file_path}': {e}")

    def vider_fichier(self):
        """
        Fonction pour supprimer tout le contenu d'un fichier.
        Le fichier sera vidé mais il restera existant.
        """
        try:
            with open(self.file_path, "w") as f:
                # Ouvrir le fichier en mode 'w' va écraser son contenu
                f.truncate(0)  # Truncate est optionnel, car 'w' vide déjà le fichier.
            print(f"Le fichier '{self.file_path}' a été vidé avec succès.")
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{self.file_path}' n'existe pas.")
        except Exception as e:
            print(f"Erreur lors de la suppression du contenu du fichier '{self.file_path}': {e}")


if __name__ == "__main__":
    gestion_fichier_hierarchique().open_file_in_editor()
