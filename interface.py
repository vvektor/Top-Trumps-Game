from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from logic import fetch_image, pokemonCard

def battle_result(stat, user_card, ai_card):
    result = user_card.battle(ai_card, stat)
    messagebox.showinfo("Battle Result", f"{result}\n\nAI's pokemon was: {ai_card.name}\nAI pokemon's stats:\nid: {ai_card.id}\nheight: {ai_card.height}\nweight: {ai_card.weight}")

def restart_game():
    from logic import game_controller
    user_card, ai_card = game_controller()
    root.destroy() 
    view_controller(user_card, ai_card)  

def view_controller(user_card, ai_card):
    global root  

    root = Tk()
    root.title("Top Trumps: Pokemon Edition")
    root.geometry("400x700+500+100")

    image = fetch_image(user_card.image)
    resized_image = image.resize((400, 400), Image.LANCZOS)
    photo = ImageTk.PhotoImage(resized_image)

    label = Label(root, image=photo)
    label.image = photo
    label.pack()

    text = f"Name: {user_card.name}\nID: {user_card.id}\nHeight: {user_card.height}\nWeight: {user_card.weight}"
    text_label = Label(root, text=text, font=("Helvetica", 14), justify=CENTER)
    text_label.pack(pady=10)

    text = "What stat do you want to use for a battle?"
    text_label = Label(root, text=text, font=("Helvetica", 16), justify=CENTER)
    text_label.pack(pady=10)

    button_frame = Frame(root)
    button_frame.pack(pady=10)

    id_button = Button(button_frame, text="ID", command=lambda: battle_result("id", user_card, ai_card))
    id_button.grid(row=0, column=0, padx=10)

    height_button = Button(button_frame, text="Height", command=lambda: battle_result("height", user_card, ai_card))
    height_button.grid(row=0, column=1, padx=10)

    weight_button = Button(button_frame, text="Weight", command=lambda: battle_result("weight", user_card, ai_card))
    weight_button.grid(row=0, column=2, padx=10)

    restart_button = Button(root, text="Restart Game", command=restart_game)
    restart_button.pack(pady=20)

    root.mainloop()