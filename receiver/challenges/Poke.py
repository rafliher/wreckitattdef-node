from .Challenge import Challenge

import io
import requests
import random
import subprocess

class Poke(Challenge):
    flag_location = 'flags/poke.txt'
    history_location = 'history/poke.txt'

    def distribute(self, flag):
        try:
            with open(self.flag_location, 'w') as f:
                f.write(flag)
            
            with open(self.history_location, 'a') as f:
                f.write(flag + '\n')

            self.logger.info(f'Flag {flag} written to {self.flag_location}')
            return True

        except Exception as e:
            self.logger.error(f'Could not write flag to {self.flag_location}: {e}')
            return False

    def check(self):
        pokemon_names = [
            "pikachu", "bulbasaur", "charmander", "squirtle", "jigglypuff",
            "meowth", "psyduck", "machop", "gastly", "krabby",
            "mew", "charizard", "pidgey", "rattata", "vulpix",
            "eevee", "snorlax", "magikarp", "growlithe", "abra"
        ]

        try:
            # Step 1: Randomize the Pokémon name
            pokemon_name =  random.choice(pokemon_names)
            url = f'http://localhost:{self.port}/'
            data = {'pokemon_name': pokemon_name}
            r = requests.post(url, data=data, timeout=5)
            assert pokemon_name.lower() in r.text.lower(), 'Pokémon data not available'

            # Step 2: Check if the image is available
            image_url = f'http://localhost:{self.port}/?image={pokemon_name.lower()}.png'
            r = requests.get(image_url, timeout=5)
            assert r.status_code == 200 and 'image/png' in r.headers['Content-Type'], 'Pokémon image not available or incorrect content type'
            
            # Step 3: Check if the flag still exists and matches the one in the container
            with open(self.flag_location, 'r') as f:
                host_flag = f.read().strip()

            container_flag = subprocess.run(
                ["docker", "exec", "poke_container", "cat", "/flag.txt"],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            assert host_flag == container_flag, 'Flag mismatch between host and container'

            self.logger.info('Check passed for poke')
            return True

        except Exception as e:
            self.logger.error(f'Could not check poke: {e}')
            return False