from .Challenge import Challenge

import io
import requests
import random

class Niko(Challenge):
    flag_location = 'flags/niko.txt'
    history_location = 'history/niko.txt'

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
            self.logger.info('Check passed for niko')
            return True

        except Exception as e:
            self.logger.error(f'Could not check niko: {e}')
            return False