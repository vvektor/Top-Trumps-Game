import requests
import random as rand
from io import BytesIO
from PIL import Image

class pokemonCard:
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

def get_stats(poke_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}/"
    response = requests.get(url)
    pokemon_data = response.json()

    return pokemon_data["name"],  pokemon_data["height"], pokemon_data["weight"], pokemon_data["sprites"]["front_default"]

def game_controller():
    user_poke_id = rand.randint(1, 500)
    ai_poke_id = rand.randint(1, 500)

    user_poke_name, user_poke_height, user_poke_weight, user_image = get_stats(user_poke_id)
    ai_poke_name, ai_poke_height, ai_poke_weight, ai_image = get_stats(ai_poke_id)

    user_card = pokemonCard(user_poke_id, user_poke_name, user_poke_height, user_poke_weight, user_image)
    ai_card = pokemonCard(ai_poke_id, ai_poke_name, ai_poke_height, ai_poke_weight, ai_image)

    return user_card, ai_card

def fetch_image(url):
    response = requests.get(url)
    image_data = response.content
    image = Image.open(BytesIO(image_data))
    return image