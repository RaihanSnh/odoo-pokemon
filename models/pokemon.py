from odoo import models, fields, api
import requests
import random
import time

class Pokemon(models.Model):
    _inherit = 'res.partner'

    pokemon_id = fields.Char('Pokémon ID')
    pokemon_name = fields.Char('Pokémon Name')
    pokemon_moves = fields.Text('Pokémon Moves')

    has_pokemon = fields.Boolean('Has Pokémon', compute='_compute_has_pokemon')

    @api.depends('pokemon_id')
    def _compute_has_pokemon(self):
        for record in self:
            record.has_pokemon = bool(record.pokemon_id)

    
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
                self.pokemon_moves = ', '.join([move['move']['name'] for move in data.get('moves', [])[:3]])
                self.assigned_pokemon[self.pokemon_id] = self.id
        except Exception as e:
            pass 

    def unlink(self):
        if self.pokemon_id in self.assigned_pokemon:
            del self.assigned_pokemon[self.pokemon_id]
        return super(Pokemon, self).unlink()

    @api.model
    def get_pokemon_data(self, limit=10, offset=0):
        try:
            response = requests.get(f'https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}')
            if response.status_code != 200:
                return
            data = response.json().get('results', [])
            for pokemon_data in data:
                pokemon_id = pokemon_data['url'].split('/')[-2]
                time.sleep(1)
                response = requests.get(pokemon_data['url'])
                if response.status_code != 200:
                    continue
                pokemon_detail = response.json()
                self.create({
                    'pokemon_id': pokemon_detail.get('id'),
                    'pokemon_name': pokemon_detail.get('name'),
                    'pokemon_moves': ', '.join([move['move']['name'] for move in pokemon_detail.get('moves', [])[:3]]),
                    'name': self.name
                })
        except Exception as e:
            pass