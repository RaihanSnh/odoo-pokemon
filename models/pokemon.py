from odoo import models, fields, api
import requests
import random
import time

class Pokemon(models.Model):
    _inherit = 'res.partner'

    pokemon_id = fields.Char('Pokémon ID')
    pokemon_name = fields.Char('Pokémon Name')
    pokemon_moves = fields.Text('Pokémon Moves')  # new field to store the moves

    assigned_pokemon = {}

    def get_pokemon(self):
        try:
            if self.is_company:
                time.sleep(1)
                response = requests.get('https://pokeapi.co/api/v2/pokemon/')
                if response.status_code != 200:
                    return
                total_pokemon = response.json().get('count')
                pokemon_id = random.randint(1, total_pokemon)
                while pokemon_id in self.assigned_pokemon.values():
                    pokemon_id = random.randint(1, total_pokemon)
                if self.pokemon_id and self.pokemon_id in self.assigned_pokemon:
                    del self.assigned_pokemon[self.pokemon_id]
                time.sleep(1)
                response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
                if response.status_code != 200:
                    return
                data = response.json()
                self.pokemon_id = data.get('id')
                self.pokemon_name = data.get('name')
                self.pokemon_moves = ', '.join([move['move']['name'] for move in data.get('moves', [])])  # get the moves
                self.assigned_pokemon[self.pokemon_id] = self.id
        except Exception as e:
            pass 
    
    def unlink(self):
        if self.pokemon_id in self.assigned_pokemon:
            del self.assigned_pokemon[self.pokemon_id]
        return super(Pokemon, self).unlink()