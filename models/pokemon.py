from odoo import models, fields, api
import requests
import random

class Pokemon(models.Model):
    _inherit = 'res.partner'

    pokemon_id = fields.Char('Pokémon ID')
    pokemon_name = fields.Char('Pokémon Name')

    def get_pokemon(self):
        if self.is_company:
            response = requests.get('https://pokeapi.co/api/v2/pokemon/')
            total_pokemon = response.json().get('count')
            pokemon_id = random.randint(1, total_pokemon)
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
            data = response.json()
            self.pokemon_id = data.get('id')
            self.pokemon_name = data.get('name')
