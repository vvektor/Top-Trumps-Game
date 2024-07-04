'''
Topic: Top Trumps Game
Author: Julia Hryn
'''
from interface import view_controller
from logic import game_controller

def main():
    user_card, ai_card = game_controller()
    print(f"Your pokemon is: {user_card.name} \nYour pokemon's stats:\nid: {user_card.id}\nheight: {user_card.height}\nweight: {user_card.weight}")
    view_controller(user_card, ai_card)

if __name__ == '__main__':
    main()