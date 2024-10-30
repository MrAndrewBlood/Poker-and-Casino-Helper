# gui.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import requests

current_version = "1.0.0"

def run_app():
    root = tk.Tk()
    root.title("Poker and Casino Helper from Andrewblood")
    window_width = 700
    window_height = 500

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_right = screen_width - window_width - 20
    position_bottom = screen_height - window_height - 100
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_bottom}")

    menubar = tk.Menu(root)
    start_menu = tk.Menu(menubar, tearoff=0)
    start_menu.add_command(label="Check for updates", command=lambda: check_for_updates(current_version))
    start_menu.add_command(label="About", command=lambda: show_about(current_version))
    menubar.add_cascade(label="Start", menu=start_menu)
    root.config(menu=menubar)

    label = tk.Label(root, text="How many opponents have cards in their hands?", font=("Arial", 12))
    label.pack(pady=(10, 0))

    selected_opponent = tk.IntVar(value=1)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    rb1 = tk.Radiobutton(frame, text="1 Opponent", variable=selected_opponent, value=1)
    rb2 = tk.Radiobutton(frame, text="2 Opponents", variable=selected_opponent, value=2)
    rb3 = tk.Radiobutton(frame, text="3 Opponents", variable=selected_opponent, value=3)

    rb1.grid(row=0, column=0, padx=10)
    rb2.grid(row=0, column=1, padx=10)
    rb3.grid(row=0, column=2, padx=10)

    card_selection_label = tk.Label(root, text="Choose Your Hand Cards", font=("Arial", 12))
    card_selection_label.pack(pady=10)

    cards_frame = tk.Frame(root)
    cards_frame.pack(pady=10)

    card_images = []
    card_buttons = []
    card_filenames = []

    def version_tuple(version):
        # Entferne 'v' und splitte die Versionsnummer in Teile
        return tuple(map(int, version.lstrip('v').split('.')))

    def check_for_updates(installed_version):
        # URL der GitHub-API für die Releases des Repositories
        url = "https://api.github.com/repos/MrAndrewBlood/Poker-and-Casino-Helper/releases/latest"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Überprüfen, ob der Request erfolgreich war
            latest_release = response.json()
            latest_version = latest_release["tag_name"]  # Die neueste Version aus dem Release

            # Vergleich der Versionen nach numerischem Wert
            if version_tuple(latest_version) > version_tuple(installed_version):
                print(f"Found a new version {latest_version}!")
                print("Please install it from: https://github.com/MrAndrewBlood/Poker-and-Casino-Helper")
            else:
                print(f"You have the newest version {installed_version} installed!")

        except requests.exceptions.RequestException as e:
            print(f"Error when connecting to the GitHub-API: {e}")

    def show_about(version):
        # Hier kannst du alle wichtigen Informationen zum Programm anzeigen
        about_text = (
            "Program name: Poker and Casino Helper from Andrewblood\n"
            f"Version: {version}\n\n"
            "Description: A Python-based automated Captcha Solver developed using OpenCV and PyAutoGUI.\n This tool can recognize and automatically solve various types of Captchas.\n\n"
            "GitHub: https://github.com/MrAndrewBlood/Captcha-Solver\n\n"
            "GGPoker Holdem All-in or Fold Helper"
            "Developer: Andrewblood"
        )
        messagebox.showinfo("Über dieses Programm", about_text)

    def load_card_images():
        suits = ['heart', 'diamond', 'club', 'spade']
        ranks = [2, 3, 4, 5, 6, 7, 8, 9, 'T', 'J', 'Q', 'K', 'A']

        for suit in suits:
            for rank in ranks:
                card_file = f"cards/{suit}_{rank}.png"
                try:
                    img = Image.open(card_file)
                    img = img.resize((40, 60))
                    img_tk = ImageTk.PhotoImage(img)
                    card_images.append(img_tk)
                    card_filenames.append(card_file)

                    card_button = tk.Button(cards_frame, image=img_tk, command=lambda f=card_file: select_card(f))
                    card_button.grid(row=len(card_buttons) // 13, column=len(card_buttons) % 13, padx=3, pady=3)
                    card_buttons.append(card_button)
                except FileNotFoundError:
                    print(f"File not found: {card_file}")

    selected_cards = []

    def select_card(card_file):
        if card_file in selected_cards:
            selected_cards.remove(card_file)
            index = card_filenames.index(card_file)
            card_buttons[index].config(relief=tk.RAISED, bg='SystemButtonFace')
        elif len(selected_cards) < 2:
            selected_cards.append(card_file)
            index = card_filenames.index(card_file)
            card_buttons[index].config(relief=tk.SUNKEN, bg='lightblue')
        else:
            messagebox.showinfo("Selection Error", "You can only select two cards.")

        # Automatically analyze the hand when two cards are selected
        if len(selected_cards) == 2:
            analyze_hand()

    def reset_cards():
        selected_cards.clear()
        for button in card_buttons:
            button.config(relief=tk.RAISED, bg='SystemButtonFace')

    def analyze_hand():
        if len(selected_cards) != 2:
            messagebox.showinfo("Selection Error", "Please select exactly two cards.")
            return

        num_opponents = selected_opponent.get()

        card_args = []
        for card in selected_cards:
            card_name = card.split('/')[-1].replace('.png', '')
            card_args.append(card_name)

        try:
            result = subprocess.run(
                ["python", "analyze.py", str(num_opponents)] + card_args,
                capture_output=True, text=True
            )
            output = result.stdout.strip()

            # Check if result contains 'All-in' or 'Fold' and change text color accordingly
            if "All-in" in output:
                result_label.config(text=output, fg="green")
            else:
                result_label.config(text=output, fg="red")

        except Exception as e:
            result_label.config(text=f"Error: {e}", fg="red")

        reset_cards()

    result_label = tk.Label(root, text="", font=("Arial", 14), fg="red")
    result_label.pack(pady=10)

    load_card_images()

    root.mainloop()
