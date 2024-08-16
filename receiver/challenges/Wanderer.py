from .Challenge import Challenge

import io
import requests
import random
import subprocess
import requests

class Naraka(Challenge):
    flag_location = 'flags/wanderer.txt'
    history_location = 'history/wanderer.txt'

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
            # Step 4: Check flag
            with open(self.flag_location, 'r') as f:
                host_flag = f.read().strip()

            container_flag = subprocess.run(
                ["docker", "exec", "wanderer_container", "cat", "/flag.txt"],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            assert host_flag == container_flag, 'Flag mismatch between host and container'

            self.logger.info('Check passed for naraka')
            return True

        except Exception as e:
            self.logger.error(f'Could not check naraka: {e}')
            return False