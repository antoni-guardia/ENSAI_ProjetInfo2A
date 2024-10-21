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
    url = "https://jsonplaceholder.typicode.com/todos/1"  # Example API for testing
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
    return answers["action"]


def enter_coordinates():
    try:
        x = float(typer.prompt("Enter the X coordinate"))
        y = float(typer.prompt("Enter the Y coordinate"))
        point = Point(x, y)  # Use your existing Point class
        points.append(point)  # Store the point in the list
        print(f"Point created: (x={point.x}, y={point.y}) and stored successfully!")
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
    show_ascii_header("Vous etes ici !")
    while True:
        action = get_user_choice()

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
