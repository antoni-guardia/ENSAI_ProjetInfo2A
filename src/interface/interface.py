import typer
import inquirer
from pyfiglet import figlet_format
from tabulate import tabulate
import requests
from yaspin import yaspin
from business_object.point import Point

# Define a Typer app
app = typer.Typer()

points = []


def show_ascii_header(text):
    ascii_art = figlet_format(text)
    print(ascii_art)


def fetch_data():
    url = "https://jsonplaceholder.typicode.com/todos/1"  # Exemple d'API
    with yaspin(text="Fetching data...", color="cyan") as spinner:
        response = requests.get(url)
        spinner.ok("✔")  # Stop spinner with success mark
        return response.json()


def show_data_table(data):
    table_data = [[key, value] for key, value in data.items()]
    headers = ["Key", "Value"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


def get_user_choice():
    questions = [
        inquirer.List(
            "action",
            message="What would you like to do?",
            choices=["Fetch Data", "Enter Coordinates", "Show Stored Points", "Exit"],
        )
    ]
    answers = inquirer.prompt(questions)

    if answers:
        return answers.get("action")
    else:
        print("No input received. Please try again.")
        return None


def convert_to_dms(coord):
    """
    Convertit une coordonnée en degrés, minutes et secondes (DMS).

    Parameters
    ----------
    coord : float
        La coordonnée à convertir.

    Returns
    -------
    tuple
        Un tuple contenant les coordonnées en DMS : (degrés, minutes, secondes).
    """
    degrees = int(coord)
    minutes = int((abs(coord) - abs(degrees)) * 60)
    seconds = (abs(coord) - abs(degrees) - minutes / 60) * 3600
    return degrees, minutes, seconds


def enter_coordinates():
    try:
        x = float(typer.prompt("Enter the X coordinate (latitude)"))
        y = float(typer.prompt("Enter the Y coordinate (longitude)"))
        point = Point(x, y)  # Utilisez votre classe Point existante
        points.append(point)  # Stockez le point dans la liste
        print(f"Point created: (x={point.x}, y={point.y}) and stored successfully!")

        # Convertir les coordonnées en DMS
        dms_lat = convert_to_dms(x)  # Convertir latitude en DMS
        dms_lon = convert_to_dms(y)  # Convertir longitude en DMS

        print(f"Converted Coordinates in DMS: Latitude: {dms_lat}, Longitude: {dms_lon}")

    except ValueError:
        print("Invalid input. Please enter valid float values for the coordinates.")
    except TypeError as e:
        print(f"Error: {e}")


def show_stored_points():
    if points:
        print("\nStored Points:")
        for i, point in enumerate(points, 1):
            print(f"{i}. Point(x={point.x}, y={point.y})")
    else:
        print("No points stored yet.")


@app.command()
def main():
    show_ascii_header("Vous êtes ici !")
    while True:
        action = get_user_choice()

        if action is None:
            continue

        if action == "Fetch Data":
            data = fetch_data()
            show_data_table(data)
        elif action == "Enter Coordinates":
            enter_coordinates()
        elif action == "Show Stored Points":
            show_stored_points()
        elif action == "Exit":
            print("Goodbye!")
            break


if __name__ == "__main__":
    app()
