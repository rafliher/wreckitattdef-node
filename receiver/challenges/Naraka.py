from .Challenge import Challenge

import io
import requests
import random
import subprocess
import requests
import re

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

        math_expression = "+-*"

        python_programs = [
            "a = 10;b = 5;print(a+b)", "a = 'add'; b='string';print(a+b)","x = [1,2,3,4,5,6,7,8];print(max(x))"
        ]

        programs_result = ["b&#39;15","b&#39;addstring","b&#39;8"]
        try:
            # Step 1: Chekc Greetings return name
            name =  random.choice(random_name)
            url = f'http://localhost:{self.port}/render?name={name}'
            r = requests.get(url, timeout=5)
            assert name in r.text, 'Greetings is not greetings my name :('

            # Step 2: Check eval calculator using random math expression
            math = f'{random.randint(1,100)}{random.choice(math_expression)}{random.randint(1,100)}'
            math_result = eval(math)
            data = {'chall': '2','input':math}
            url = f'http://localhost:{self.port}/chall'
            r = requests.post(url, data=data, timeout=5)
            assert str(math_result) in r.text, 'Eval calculator is not working :('
            
            # Step 3: Check exec that execute python program
            ind = random.randint(0,2)
            pythononeline = python_programs[ind]
            pythonresult = programs_result[ind]
            data = {'chall': '1','input':pythononeline}
            url = f'http://localhost:{self.port}/chall'
            r = requests.post(url, data=data, timeout=5)
            assert pythonresult in r.text, 'My code line is not execute :('

            # Step 4: Check execute FLAG declaration execute
            url = f'http://localhost:{self.port}/sourcecode/1'
            r = requests.get(url, timeout=5)
            flag_assignments = re.findall(r'^\s*FLAG\s*=\s*sys\.argv\[2\]\s*$', r.text, re.MULTILINE)
            flag_assignments_num =  flag_assignments = re.findall(r'^\s*FLAG\s*=\s*.+$', r.text, re.MULTILINE)
            assert flag_assignments != 1 or flag_assignments_num != 1, "execute FLAG declared incorrectly"

            # Step 5: Check evaluate FLAG declaration execute
            url = f'http://localhost:{self.port}/sourcecode/1'
            r = requests.get(url, timeout=5)
            flag_assignments = re.findall(r'^\s*FLAG\s*=\s*sys\.argv\[2\]\s*$', r.text, re.MULTILINE)
            flag_assignments_num =  flag_assignments = re.findall(r'^\s*FLAG\s*=\s*.+$', r.text, re.MULTILINE)
            assert flag_assignments != 1 or flag_assignments_num != 1, "evaluate FLAG declared incorrectly"

            # Step 6: Check flag
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