import requests
import random as rand
from io import BytesIO
from PIL import Image, ImageTk

class Card:
    def __init__(self, id, name, height, weight, image):
        self.id = id
        self.name = name 
        self.height = height
        self.weight = weight
        self.image = image 

    def battle(self, other, option):
        self_value = getattr(self, option)
        other_value = getattr(other, option)
        
        if self_value > other_value:
            return "You won!"
        elif self_value < other_value:
            return "The AI won!"
        else:
            return "It's a draw!"

class pokemonCard(Card):
    def __init__(self, id, name, height, weight, hp, image):
        super().__init__(id, name, height, weight, image)
        self.hp = hp

    def get_image(self):
        url = self.image
        response = requests.get(url)
        image_data = response.content
        photo = Image.open(BytesIO(image_data))
        resized_image = photo.resize((200, 200), Image.LANCZOS)
        return resized_image
    
class starWarsCard(Card):
    def __init__(self, id, name, height, weight, films, image):
        super().__init__(id, name, height, weight, image)
        self.films = films

    def battle(self, other, option):
            self_value = getattr(self, option)
            other_value = getattr(other, option)

            if option == "weight":
                if self_value == "unknown" and other_value == "unknown":
                    return "It's a draw!"
                elif self_value == "unknown":
                    return "The AI won!"
                elif other_value == "unknown":
                    return "You won!"

            if self_value > other_value:
                return "You won!"
            elif self_value < other_value:
                return "The AI won!"
            else:
                return "It's a draw!"
        
    def get_image(self):
        url = self.image
        photo = Image.open(url)
        resized_image = photo.resize((200, 200), Image.LANCZOS)
        return resized_image

def get_stats(mode, id_):
    if mode == "pokemon":
        url = f"https://pokeapi.co/api/v2/pokemon/{id_}/"
        response = requests.get(url)
        data = response.json()
        card = pokemonCard(id_, data["name"],  data["height"], data["weight"], data["stats"][0]["base_stat"], data["sprites"]["front_default"])
        return card
    
    elif mode == "star wars":
        url = f"https://swapi.dev/api/people/{id_}"
        response = requests.get(url)
        data = response.json()

        image = fr"Top-Trumps-Game\images\{id_}.jpg"
        card = starWarsCard(id_, data["name"], data["height"], data["mass"], len(data["films"]), image)
        return card
    
def game_controller(mode):
    if mode == "pokemon":
        card_range = range(1, 600)
    elif mode == "star wars":
        card_range = range(1, 60)

    user_cards = []
    for _ in range(3):
        user_id = rand.sample(card_range, 1)[0]
        user_card = get_stats(mode, user_id)
        user_cards.append(user_card)

    ai_id = rand.sample(card_range, 1)[0]
    ai_card = get_stats(mode, ai_id)

    return user_cards, ai_card