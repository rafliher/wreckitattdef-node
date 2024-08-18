from .Challenge import Challenge

import io
import requests
import random
import subprocess
import requests
import re

class Wanderer(Challenge):
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
            session = requests.Session()
            # Step 1: Check Register
            register_url = f'http://localhost:{self.port}/index.php?module=user&action=register'
            registration_data = {'username': 'adminwreckitchecker','password': 'adminwreckitchecker'}
            response = session.post(register_url, data=registration_data)
            assert "username already exists" in response.text or "Registration Success" in response.text or response.status_code == 200 , 'Function Register Failed'

            # Step 2: Check Login
            login_url = f'http://localhost:{self.port}/index.php?module=user&action=login'
            login_data = {'username': 'adminwreckitchecker', 'password': 'adminwreckitchecker'}
            response = session.post(login_url, data=login_data)
            assert "Login Success" in response.text or response.status_code == 200, 'Login function failed'

            # Step 3: Check UUID Not hidden
            view_page_url = f'http://localhost:{self.port}/index.php?module=page&action=viewPage'
            response = session.get(view_page_url)
            uuid_pattern = re.compile(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
            found_uuids = uuid_pattern.findall(response.text)
            assert found_uuids, 'UUID not found'

            # Step 4: Check create sample page
            sample_page_url = f'http://localhost:{self.port}/index.php?module=page&action=samplePage'
            response = session.get(sample_page_url)
            assert "Create Success" in response.text or response.status_code == 200, 'Create Sample Failed'

            # Step 5: Check Edit HTML Functionality
            edit_url_html = f'http://localhost:{self.port}/index.php?module=user&action=edit&type=html'
            response = session.get(edit_url_html)
            assert response.status_code == 200, 'Edit html page not accessible'

            # Step 6: Check Edit JS Functionality
            edit_url_js = f'http://localhost:{self.port}/index.php?module=user&action=edit&type=js'
            response = session.get(edit_url_js)
            assert response.status_code == 200, 'Edit js page not accessible'

            # Step 7: Check Edit CSS Functionality
            edit_url_css = f'http://localhost:{self.port}/index.php?module=user&action=edit&type=css'
            response = session.get(edit_url_css)
            assert response.status_code == 200, 'Edit css page not accessible'
            
            # Step 8: Check flag
            with open(self.flag_location, 'r') as f:
                host_flag = f.read().strip()

            container_flag = subprocess.run(
                ["docker", "exec", "wanderer_container", "cat", "/flag.txt"],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            assert host_flag == container_flag, 'Flag mismatch between host and container'

            self.logger.info('Check passed for wanderer')
            return True

        except Exception as e:
            self.logger.error(f'Could not check wanderer: {e}')
            return False
