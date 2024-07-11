from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk
from logic import Card, pokemonCard, starWarsCard, game_controller
from colors import *
from datetime import datetime

game_screen = None 
id_button = None
height_button = None
weight_button = None
extra_button = None
global score

score = {
    "You": {
        'total' : 0, 
        'rounds': [],
        'stat': [],
        'mode' : []
        },
    "AI": {
        'total' : 0, 
        'rounds': [],
        'stat': [],
        'mode' : []
    }
}

score_map = {
    "You won!" : (1, 0),
    "The AI won!" : (0, 1),
    "It's a draw!": (0, 0)
}

def export_score():
    global score

    files = [('All Files', '*.*'),  
             ('CSV Files', '*.csv'), 
             ('Text Document', '*.txt')] 
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    file = asksaveasfile(filetypes = files, defaultextension = files, initialfile=f'scores_{timestamp}.txt')

    if file is not None:
            file.write("Round\tYou\tAI\tStat\tMode\n")
            
            rounds = len(score['You']['rounds'])
            for i in range(rounds):
                you_score = score['You']['rounds'][i]
                ai_score = score['AI']['rounds'][i]
                stat = score['AI']['stat'][i]
                mode = score['AI']['mode'][i]
                file.write(f"{i+1}\t{you_score}\t{ai_score}\t{stat}\t{mode}\n")
            
            file.write(f"Total\t{score['You']['total']}\t{score['AI']['total']}")
            file.close()

def ask_score():
    popup = Toplevel()
    popup.title("Change Game Mode")
    popup.geometry("250x200+825+360")
    popup.resizable(False, False)
    popup.configure(background=bg_color)

    label = Label(popup, text="Do you want to keep the score?", padx=20, pady=20, bg=bg_color, font=("Helvetica", 12, "bold"))
    label.pack()

    def keep_score():
        main_menu(clear_content(game_screen))
        popup.destroy()

    def reset_score():
        global score
        score = {
            "You": {'total' : 0, 'rounds': [], 'stat': [], 'mode' : []},
            "AI": {'total' : 0, 'rounds': [],'stat': [],'mode' : []}
            }
        main_menu(clear_content(game_screen))
        popup.destroy()

    yes_btn = Button(popup, text="Yes, keep my score", width=20, height=1, font=("Helvetica", 10), justify=CENTER, command=keep_score, bg=blue, activebackground=dark_blue)
    yes_btn.pack(pady=10)

    no_btn = Button(popup, text="No, reset my score", width=20, height=1, font=("Helvetica", 10), justify=CENTER, command=reset_score, bg=soft_red, activebackground=dark_red)
    no_btn.pack(pady=10)

    popup.grab_set()
    popup.wait_window()

def display_scoreboard(score):
    frame = Frame(game_screen, height=50, width=660, bg=light_blue)
    frame.grid(row=0, column=0, columnspan=3, rowspan=1, padx=10, pady=10)

    label = Label(frame, text=f"YOU: {score['You']['total']}", font=("Helvetica", 16), justify=CENTER, bg=light_blue)
    label.grid(row=0, column=0, padx=10, pady=10)

    label = Label(frame, text=f"AI: {score['AI']['total']}", font=("Helvetica", 16), justify=CENTER, bg=light_blue)
    label.grid(row=0, column=1, padx=10, pady=10)

    export_btn = Button(frame, text="Export Score",  width=20, bg=blue, activebackground=dark_blue, borderwidth=1, command=export_score)
    export_btn.grid(row=0, column=2, padx=10, pady=10)

    change_mode_btn = Button(frame, text="Change Game Mode",  width=20, bg=blue, activebackground=dark_blue, borderwidth=1, command=ask_score)
    change_mode_btn.grid(row=0, column=3, padx=10, pady=10)

def score_tracker(result, stat, mode):
    global score

    score["You"]["total"] += result[0]
    score["You"]["rounds"].append(result[0])
    score["You"]["stat"].append(stat)
    score["You"]["mode"].append(mode)

    score["AI"]["total"] += result[1]
    score["AI"]["rounds"].append(result[1])
    score["AI"]["stat"].append(stat)
    score["AI"]["mode"].append(mode)
    
    return score

def battle_result(mode, stat, user_card, ai_card):
    global game_screen

    restart_btn = Button(game_screen, text="Play Another Round",  width=20, bg=blue, activebackground=dark_blue, borderwidth=1, command=lambda arg=mode : start_game(game_screen, arg))
    restart_btn.grid(row=9, column=1, padx=10, pady=10)

    result = user_card.battle(ai_card, stat)
    if mode == "pokemon":
        messagebox.showinfo("Battle Result", f"{result}\n\nAI's Pokemon was: {ai_card.name.capitalize()}\nAI Pokemon's stats:\nID: {ai_card.id}\nHeight: {ai_card.height}\nWeight: {ai_card.weight}\nHP: {ai_card.hp}")
    elif mode == "star wars":
        messagebox.showinfo("Battle Result", f"{result}\n\nAI's Character was: {ai_card.name.title()}\nAI Character's stats:\nID: {ai_card.id}\nHeight: {ai_card.height}\nWeight: {ai_card.weight}\nFilms: {ai_card.films}")

    score = score_tracker(score_map[result], stat, mode)
    display_scoreboard(score)

def disable_battle_buttons():
    global id_button, height_button, weight_button, extra_button
    id_button.config(state=DISABLED)
    height_button.config(state=DISABLED)
    weight_button.config(state=DISABLED)
    extra_button.config(state=DISABLED)

def on_card_click(mode, selected_index, user_choice_data, ai_card):
    global id_button, height_button, weight_button, extra_button

    selected_card, selected_button = user_choice_data[selected_index]

    for card, button in user_choice_data:
        if button != selected_button:
            button.config(state=DISABLED)
        else:
            button.config(state=DISABLED, borderwidth=2)

    label = Label(game_screen, text="What stat do you want to use for a battle?", font=("Helvetica", 16), justify=CENTER, bg=bg_color)
    label.grid(row=6, column=1, padx=10, pady=10)

    button_frame = Frame(game_screen, bg=light_blue)
    button_frame.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

    id_button = Button(button_frame, text="ID", width=20, bg=bg_color, borderwidth=0, command=lambda stat="id": (battle_result(mode, stat, selected_card, ai_card), disable_battle_buttons()))
    id_button.grid(row=7, column=0, padx=10, pady=10)

    height_button = Button(button_frame, text="Height", width=20, bg=bg_color, borderwidth=0, command=lambda stat="height": (battle_result(mode, stat, selected_card, ai_card), disable_battle_buttons()))
    height_button.grid(row=7, column=1, padx=10, pady=10)

    weight_button = Button(button_frame, text="Weight", width=20, bg=bg_color, borderwidth=0, command=lambda stat="weight": (battle_result(mode, stat, selected_card, ai_card), disable_battle_buttons()))
    weight_button.grid(row=7, column=2, padx=10, pady=10)

    if mode == "pokemon":
        extra_button = Button(button_frame, text="HP", width=20, bg=bg_color, borderwidth=0, command=lambda stat="hp": (battle_result(mode, stat, selected_card, ai_card), disable_battle_buttons()))
        extra_button.grid(row=7, column=3, padx=10, pady=10)
    elif mode == "star wars":
        extra_button = Button(button_frame, text="Films", width=20, bg=bg_color, borderwidth=0, command=lambda stat="films": (battle_result(mode, stat, selected_card, ai_card), disable_battle_buttons()))
        extra_button.grid(row=7, column=3, padx=10, pady=10)

def card_picker(mode, user_cards, ai_card):
    global game_screen
    user_choice_buttons = []

    frame = Frame(game_screen, height=220, width=660, bg=light_blue)
    frame.grid(row=2, column=0, columnspan=3, rowspan=3, pady=10)

    card_frame = Frame(frame, height=50, width=50, bg=light_blue)
    card_frame.grid(row=2, column=0, columnspan=3, rowspan=2, padx=10, pady=10)

    for i, card in enumerate(user_cards):
        image = card.get_image()
        photo = ImageTk.PhotoImage(image)

        button = Button(card_frame, image=photo, borderwidth=0,  bg=bg_color, activebackground=dark_blue)
        button.image = photo
        button.grid(row=1, column=i, padx=10, pady=10)

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("Treeview.Heading", background=dark_blue, foreground="white", font=("TkDefaultFont", 10, "bold"))
        s.configure("Treeview.Item", background=white)
        
        tree_stat = ttk.Treeview(card_frame, columns=("stat", "value"), show="", height="5", padding=5)
        tree_stat.tag_configure("value_field", background=bg_color)
        tree_stat.tag_configure("name_field", background=blue)

        tree_stat.column("stat", anchor=CENTER, width=95)
        tree_stat.heading("stat", text="STAT")
        tree_stat.column("value", anchor=CENTER, width=95)
        tree_stat.heading("value", text="VALUE")

        tree_stat.insert('', 'end', text=i, values=("Name", card.name.title()), tags=("name_field",))
        tree_stat.insert('', 'end', text=i, values=("ID", card.id), tags=("value_field",))
        tree_stat.insert('', 'end', text=i, values=("Height", card.height), tags=("value_field",))
        tree_stat.insert('', 'end', text=i, values=("Weight", card.weight), tags=("value_field",))
        if mode == "pokemon":
            tree_stat.insert('', 'end', text=i, values=("HP", card.hp), tags=("value_field",))
        elif mode == "star wars":
            tree_stat.insert('', 'end', text=i, values=("Films", card.films), tags=("value_field",))

        tree_stat.grid(row=2, column=i, padx=10)

        user_choice_buttons.append((card, button))
        button.config(command=lambda index=i: on_card_click(mode, index, user_choice_buttons, ai_card))

    return user_choice_buttons

def view_controller(screen, mode, user_cards, ai_card):
    global game_screen
    game_screen = screen

    game_screen.title("Top Trumps Game")
    game_screen.geometry("690x680+500+100")
    game_screen.resizable(False, False)
    game_screen.configure(background=bg_color)

    display_scoreboard(score)

    label = Label(game_screen, text=f"Choose one of the {mode.title()} cards", font=("Helvetica", 18), justify=CENTER, bg=bg_color)
    label.grid(row=1, column=1, padx=10, pady=10)
    
    card_picker(mode, user_cards, ai_card)

def clear_content(screen):
    for widget in screen.winfo_children():
        widget.destroy()
    return screen

def start_game(screen, mode):
    clear_content(screen)
    user_cards, ai_card = game_controller(mode)
    view_controller(screen, mode, user_cards, ai_card)

def main_menu(screen):
    global menu_screen
    menu_screen = screen
    menu_screen.title("Top Trumps Game: Main Menu")
    menu_screen.geometry(("250x230+825+360"))
    menu_screen.resizable(False, False)
    menu_screen.configure(background=bg_color)

    intro_frame = Frame(menu_screen, bg=bg_color)
    intro_frame.grid(row=2, column=3, rowspan=1, columnspan=1, padx=10, pady=10)

    label = Label(intro_frame, text="Dear Player,\nhave fun playing this game!", font=("Helvetica", 12, "bold"), justify=CENTER, bg=bg_color)
    label.grid(row=2, column=3, padx=10, pady=10)

    btn_frame = Frame(menu_screen, bg=bg_color)
    btn_frame.grid(row=3, column=3, rowspan=4, columnspan=3, padx=10, pady=10)

    poke_mode = Button(btn_frame, text="Pokemon Mode", width=20, height=1, font=("Helvetica", 10), justify=CENTER, command=lambda mode="pokemon": start_game(menu_screen, mode), bg=blue, activebackground=dark_blue)
    poke_mode.grid(row=4, column=3, padx=10, pady=5)

    sw_mode = Button(btn_frame, text="Star Wars Mode", width=20, height=1, font=("Helvetica", 10), justify=CENTER, command=lambda mode="star wars": start_game(menu_screen, mode), bg=blue, activebackground=dark_blue)
    sw_mode.grid(row=5, column=3, padx=10, pady=5)

    exit_game = Button(btn_frame, text="Exit Game", width=20, height=1, font=("Helvetica", 10), justify=CENTER, command=lambda mode="exit": menu_screen.destroy(), bg=soft_red, activebackground=dark_red)
    exit_game.grid(row=6, column=3, padx=10, pady=5)