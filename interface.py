from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import asksaveasfile
from PIL import Image, ImageTk
from logic import fetch_image, pokemonCard, game_controller
import pandas as pd

root = None 
id_button = None
height_button = None
weight_button = None

global score
score = {
    "You": {'sum' : 0, 'rounds': [0]},
    "AI": {'sum' : 0, 'rounds': [0]}
}

score_map = {
    "You won!" : (1, 0),
    "The AI won!" : (0, 1),
    "It's a draw!": (0, 0)
}

def restart_game():
    for widget in root.winfo_children():
        widget.destroy()
    view_controller()

def export_score():
    global score

    files = [('All Files', '*.*'),  
             ('CSV Files', '*.csv'), 
             ('Text Document', '*.txt')] 
    
    file = asksaveasfile(filetypes = files, defaultextension = files, initialfile='scores.txt')

    if file is not None:
            file.write("round\tYou\tAI\n")
            
            rounds = len(score['You']['rounds'])
            for i in range(rounds):
                you_score = score['You']['rounds'][i]
                ai_score = score['AI']['rounds'][i]
                file.write(f"{i+1}\t{you_score}\t{ai_score}\n")
            
            file.write(f"total\t{score['You']['sum']}\t{score['AI']['sum']}\n")
            file.close()

def display_scoreboard(score):
    frame = Frame(root, height=50, width=660, bg='#e0edf6')
    frame.grid(row=0, column=0, columnspan=3, rowspan=1, padx=10, pady=10)

    label = Label(frame, text=f"YOU: {score['You']['sum']}", font=("Helvetica", 16), justify=CENTER, bg="#e0edf6")
    label.grid(row=0, column=0, padx=10, pady=10)

    label = Label(frame, text=f"AI: {score['AI']['sum']}", font=("Helvetica", 16), justify=CENTER, bg="#e0edf6")
    label.grid(row=0, column=1, padx=10, pady=10)

    export_button = Button(frame, text="Export Score",  width=20, bg='#fee3ff', borderwidth=1, command=export_score)
    export_button.grid(row=0, column=2, padx=10, pady=10)

def score_tracker(result):
    global score

    score["You"]["rounds"].append(result[0])
    score["You"]["sum"] += result[0]

    score["AI"]["rounds"].append(result[1])
    score["AI"]["sum"] += result[1]
    
    return score

def battle_result(stat, user_card, ai_card):
    global root

    restart_button = Button(root, text="Play Another Round",  width=20, bg='#fee3ff', borderwidth=1, command=restart_game)
    restart_button.grid(row=9, column=1, padx=10, pady=10)

    result = user_card.battle(ai_card, stat)
    messagebox.showinfo("Battle Result", f"{result}\n\nAI's pokemon was: {ai_card.name}\nAI pokemon's stats:\nID: {ai_card.id}\nHeight: {ai_card.height}\nWeight: {ai_card.weight}\nHP: {ai_card.hp}")

    score = score_tracker(score_map[result])
    display_scoreboard(score)

def disable_battle_buttons():
    global id_button, height_button, weight_button
    id_button.config(state=DISABLED)
    height_button.config(state=DISABLED)
    weight_button.config(state=DISABLED)

def on_card_click(selected_index, user_choice_data, ai_card):
    global id_button, height_button, weight_button

    selected_card, selected_button = user_choice_data[selected_index]

    for card, button in user_choice_data:
        if button != selected_button:
            button.config(state=DISABLED)
        else:
            button.config(state=DISABLED, borderwidth=2)

    label = Label(root, text="What stat do you want to use for a battle?", font=("Helvetica", 16), justify=CENTER, bg='#fffcf5')
    label.grid(row=6, column=1, padx=10, pady=10)

    button_frame = Frame(root, bg='#e0edf6')
    button_frame.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

    id_button = Button(button_frame, text="ID", width=20, bg='#fffcf5', borderwidth=0, command=lambda index="id": (battle_result(index, selected_card, ai_card), disable_battle_buttons()))
    id_button.grid(row=7, column=0, padx=10, pady=10)

    height_button = Button(button_frame, text="Height", width=20, bg='#fffcf5', borderwidth=0, command=lambda index="height": (battle_result(index, selected_card, ai_card), disable_battle_buttons()))
    height_button.grid(row=7, column=1, padx=10, pady=10)

    weight_button = Button(button_frame, text="Weight", width=20, bg='#fffcf5', borderwidth=0, command=lambda index="weight": (battle_result(index, selected_card, ai_card), disable_battle_buttons()))
    weight_button.grid(row=7, column=2, padx=10, pady=10)

    hp_button = Button(button_frame, text="HP", width=20, bg='#fffcf5', borderwidth=0, command=lambda index="hp": (battle_result(index, selected_card, ai_card), disable_battle_buttons()))
    hp_button.grid(row=7, column=3, padx=10, pady=10)

def card_picker(user_cards, ai_card):
    global root
    user_choice_buttons = []

    card_frame = Frame(root, height=220, width=660, bg='#e0edf6')
    card_frame.grid(row=2, column=0, columnspan=3, rowspan=3, padx=10, pady=10)

    stat_frame = Frame(card_frame, height=50, width=50, bg='#e0edf6')
    stat_frame.grid(row=2, column=0, columnspan=3, rowspan=1, padx=10, pady=10)

    for i, card in enumerate(user_cards):
        image = fetch_image(card.image)
        photo = ImageTk.PhotoImage(image)

        button = Button(card_frame, image=photo, borderwidth=0,  bg="#fffcf5", activeforeground='#f3f0eb')
        button.image = photo
        button.grid(row=1, column=i, padx=10, pady=10)

        s = ttk.Style()
        s.theme_use('clam')

        tree_stat = ttk.Treeview(stat_frame, columns=("stat", "value"), show="headings", height="5", padding=10)
        tree_stat.column("stat", anchor=CENTER, width=85)
        tree_stat.heading("stat", text="STAT")
        tree_stat.column("value", anchor=CENTER, width=85)
        tree_stat.heading("value", text="VALUE")

        tree_stat.insert('', 'end', text=i, values=("Name", card.name.capitalize()))
        tree_stat.insert('', 'end', text=i, values=("ID", card.id))
        tree_stat.insert('', 'end', text=i, values=("Height", card.height))
        tree_stat.insert('', 'end', text=i, values=("Weight", card.weight))
        tree_stat.insert('', 'end', text=i, values=("HP", card.hp))

        tree_stat.grid(row=2, column=i, padx=10, pady=10)

        user_choice_buttons.append((card, button))
        button.config(command=lambda index=i: on_card_click(index, user_choice_buttons, ai_card))

    return user_choice_buttons

def view_controller():
    user_card, ai_card = game_controller()

    global root
    global score

    root.title("Top Trumps: Pokemon Edition")
    root.geometry("690x640+500+100")
    root.configure(background='#fffcf5')

    display_scoreboard(score)

    label = Label(root, text="Choose one of the Pokemon cards", font=("Helvetica", 18), justify=CENTER, bg='#fffcf5')
    label.grid(row=1, column=1, padx=10, pady=10)
    
    card_picker(user_card, ai_card)

    root.mainloop()

root = Tk()
view_controller()