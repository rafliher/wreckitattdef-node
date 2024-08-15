from .Challenge import Challenge

import io
import requests
import random
import subprocess

class Poke(Challenge):
    flag_location = 'flags/blinkpdf.txt'
    history_location = 'history/blinkpdf.txt'

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

        try:
            # Getting private key
            container_env = subprocess.run(
                ["docker", "exec", "blinkpdf_container", "cat", "/opt/.env"],
                capture_output=True,
                text=True
            ).stdout.strip()
            private_key = container_env.split("\n")[1].split('PRIVATE_KEY')[1]

            sess = requests.Session()
            # Checking C1: Login as user
            url = f'http://localhost:{self.port}/login'
            data = {'username': "user", "password": "user"}
            r = sess.post(url, data=data, timeout=5)
            assert 'Welcome to PDF Signature App'.lower() in r.text.lower(), 'Cannot login as user'

            # Checking C2: Sign as user
            sign_url = f'http://localhost:{self.port}/sign'
            r = sess.post(sign_url, timeout=5)
            assert r.status_code == 200 and 'image/png' in r.headers['Content-Type'], 'Pokémon image not available or incorrect content type'
            
            # Checking C3: Verify as user
            verify_url = f'http://localhost:{self.port}/verify'
            r = sess.post(verify_url, timeout=5)
            
            
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