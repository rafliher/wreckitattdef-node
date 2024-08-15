from .Challenge import Challenge

import io
import requests
import random
import subprocess
import requests

class Naraka(Challenge):
    flag_location = 'flags/naraka.txt'
    history_location = 'history/naraka.txt'

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
        random_name = [
            "nael", "mufat", "rayhan", "wicak", "Kingggg",
            "osdie", "udin", "memet", "entong", "krabby",
            "mew", "charizard", "pidgey", "rattata", "vulpix",
            "eevee", "snorlax", "magikarp", "growlithe", "abra"
        ]

        math_expression = "+-*/"

        python_programs = [
            "a = 10;b = 5;print(a+b)", "a = 'add'; b='string';print(a+b)"
        ]

        programs_result = ["b&#39;15","b&#39;addstring",]
        try:
            # Step 1: Chekc Greetings return name
            name =  random.choice(random_name)
            url = f'http://localhost:{self.port}/render?name={name}'
            r = requests.get(url, timeout=5)
            assert name in r.text, 'Greetings is not greetings my name :('

            # Step 2: Check eval calculator using random math expression
            math = f'{random.randint(1,100)}{random.choice(math_expression)}{random.randint(1,100)}'
            math_result = eval(math)
            data = {'chall': '2','userinput':math}
            url = f'http://localhost:{self.port}/chall'
            r = requests.post(url, data=data, timeout=5)
            assert math_result in r.text, 'Eval calculator is not working :('
            
            # Step 3: Check flag
            with open(self.flag_location, 'r') as f:
                host_flag = f.read().strip()

            container_flag = subprocess.run(
                ["docker", "exec", "naraka_container", "cat", "/flag.txt"],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            assert host_flag == container_flag, 'Flag mismatch between host and container'

            self.logger.info('Check passed for naraka')
            return True

        except Exception as e:
            self.logger.error(f'Could not check naraka: {e}')
            return False