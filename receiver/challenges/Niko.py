from .Challenge import Challenge

import io
import requests
import random
import subprocess

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
        error_messages = [
            "あなたはどんなオタクですか",
            "冗談じゃないよ！",
            "ｔｃｈ なんだよ こいつ",
            "どうしてそんなことが可能でしょうか…不可能です",
            "本当のあなたは何ですか？",
            "うわー、ごめんなさい",
            "御心のままに、主よ",
            "もういいよ、やめて！",
            "時間です",
            "悪くないよ。"
        ]
        try:
            # Step 1: Check if the flag still exists and matches the one in the container
            with open(self.flag_location, 'r') as f:
                host_flag = f.read().strip()

            container_flag = subprocess.run(
                ["docker", "exec", "niko_container", "cat", "/flag.txt"],
                capture_output=True,
                text=True
            ).stdout.strip()                    

            assert host_flag == container_flag, 'Flag mismatch between host and container'
            
            self.logger.info('Flag check passed for niko')
            
            # Step 2: Check if the webpage can be accessed
            url = f'http://localhost:{self.port}/'
            response = requests.get(url)
            assert response.status_code == 200, 'Webpage is not accessible'
            self.logger.info('Webpage accessibility check passed for niko')

            # Step 3: Check if the output of the specific URL equals the expected string
            urlFlag = f'http://localhost:{self.port}/api/getFlag?flag=1'
            expected_output = "(⋟﹏⋞) 私をバカにしようとしているのか (´ ͡༎ຶ ͜ʖ ͡༎ຶ `)︵‿︵"
            response = requests.get(urlFlag)
            assert response.text.strip() == expected_output, 'Webpage output does not match expected output'
            self.logger.info('Webpage output check passed for niko')
            
            # Step 4: Check if the chat endpoint is working
            try:
                urlChat = f'http://localhost:{self.port}/api/chat'
                data = 'test'
                response = requests.post(urlChat, data=data)
                assert response.text.strip() in error_messages, 'Webpage is not accessible'
                self.logger.info('Webpage delay check passed for niko')
            except requests.exceptions.Timeout:
                self.logger.error('Webpage request timed out')
                return False

            return True

        except Exception as e:
            self.logger.error(f'Could not check niko: {e}')
            return False