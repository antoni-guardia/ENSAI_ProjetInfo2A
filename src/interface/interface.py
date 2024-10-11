import typer
import inquirer
from pyfiglet import figlet_format
from tabulate import tabulate
import requests
from yaspin import yaspin

# Define a Typer app
app = typer.Typer()


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
            choices=["Fetch Data", "Exit"],
        )
    ]
    answers = inquirer.prompt(questions)
    return answers["action"]


@app.command()
def main():
    show_ascii_header("Vous etes ici !")
    while True:
        action = get_user_choice()

        if action == "Fetch Data":
            data = fetch_data()
            show_data_table(data)
        elif action == "Exit":
            print("Goodbye!")
            break


if __name__ == "__main__":
    app()

pip install tabulate pyfiglet yaspin inquirer typer requests
