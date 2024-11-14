from service.services_recherche_point import ServicesRecherchePoint as SRP
import os


class ServicesFichierLecture:
    def trouver_multiple_zone_point(
        self,
        path_enregistrement,
        nom_zonage: str,
        annee: int,
        liste_points: list[tuple],
        type_coord=None,
        type_fichier=".txt",
    ):

        resultats = SRP().trouver_multiple_zone_point(
            nom_zonage, annee, liste_points, type_coord=None
        )

        os.makedirs(path_enregistrement, exist_ok=True)

        # Find the next available file number
        existing_files = os.listdir(path_enregistrement)
        requete_numbers = [
            int(f.split("_")[1].split(".")[0])
            for f in existing_files
            if f.startswith("requete_") and f.endswith(type_fichier)
        ]
        next_index = max(requete_numbers) + 1 if requete_numbers else 1
        filename = f"requete_{next_index}{type_fichier}"
        file_path = os.path.join(path_enregistrement, filename)

        # Write results to the file
        with open(file_path, "w") as file:
            for result in resultats:
                file.write(f"{result}\n")
