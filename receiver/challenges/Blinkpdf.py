from .Challenge import Challenge
from modules.blinkpdf import *

import io
import requests
import subprocess
import re

class BlinkPDF(Challenge):
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
            private_key = re.search(r'PRIVATE_KEY="(.+?)"', container_env).group(1)
            assert len(private_key) > 0, 'Missing PRIVATE_KEY on .env'

            sess = requests.Session()

            # Checking C1: Login as user
            url = f'http://localhost:{self.port}/login'
            data = {"username": "user", "password": "user"}
            r = sess.post(url, data=data, timeout=5)
            assert 'Welcome to the PDF Signature App'.lower() in r.text.lower(), 'Cannot login as user'

            pdfpath = 'files/blinkpdf_hellodocs.pdf'
            pdfbytes = open(pdfpath, 'rb').read()

            # Checking C2: Sign pdf as user
            sign_url = f'http://localhost:{self.port}/sign'
            r = sess.post(sign_url, timeout=5)
            sendata = ('main.pdf', pdfbytes, 'application/pdf')
            filedata = {'file': sendata}
            r = sess.post(sign_url, files=filedata, timeout=5)
            signed_pdf = r.content
            assert r.status_code == 200 and 'application/pdf' in r.headers['Content-Type'], 'Signed PDF not available or incorrect content type'
            signed_pdf_stream = io.BytesIO(signed_pdf)
            assert verify_signature(signed_pdf_stream, private_key), 'Algorithm for signature process is changed'

            # Checking C3: Verify valid pdf as user
            pdf_bytes_stream = io.BytesIO(pdfbytes)
            signed_pdf_stream = sign_pdf(pdf_bytes_stream, private_key)
            verify_url = f'http://localhost:{self.port}/verify'
            sendata = ('main_signed.pdf', signed_pdf_stream, 'application/pdf')
            filedata = {'file': sendata}
            r = sess.post(verify_url, files=filedata, timeout=5)
            assert 'The signature is <strong>valid</strong>.' in r.text, 'Verify function not working or algoritm verify process is changed'
            
            # Checking C3: Verify invalid pdf as user
            verify_url = f'http://localhost:{self.port}/verify'
            sendata = ('main_signed.pdf', pdfbytes, 'application/pdf')
            filedata = {'file': sendata}
            r = sess.post(verify_url, files=filedata, timeout=5)
            assert 'The signature is <strong>invalid' in r.text, 'Verify function not working or algoritm verify process is changed for invalid signature'

            # Checking C4: Checking flag on container
            with open(self.flag_location, 'r') as f:
                host_flag = f.read().strip()

            container_flag = subprocess.run(
                ["docker", "exec", "blinkpdf_container", "cat", "/flag.txt"],
                capture_output=True,
                text=True
            ).stdout.strip()
            assert host_flag == container_flag, 'Flag mismatch between host and container'
            
            # Checking C5: Login as admin and enc_flag checking
            url = f'http://localhost:{self.port}/login'
            data = {'username': "admin", "password": f'{private_key}'}
            r = sess.post(url, data=data, timeout=5)
            assert 'Welcome to the PDF Signature App'.lower() in r.text.lower(), 'Cannot login as admin'
            url = f'http://localhost:{self.port}/admin_panel'
            r = sess.get(url, timeout=5)
            enc_flag = r.text.split('encrypted flag: ')[1].split('</p>')[0]
            cek, dec = decryptMessage(enc_flag, private_key)
            assert dec.decode() == host_flag, 'Change algorithm for encryption flag'
            assert cek == True, 'Change signature algorithm for encryption flag'

            self.logger.info('Check passed for blinkpdf')
            return True

        except Exception as e:
            self.logger.error(f'Could not check blinkpdf: {e}')
            return False