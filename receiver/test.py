from modules.blinkpdf import *

import io
import requests
import subprocess
import re


def check():
    try:
        # Getting private key
        container_env = '''
        SECRET_KEY="f20f9ede4c89b052711547dee21a85e3"
        PRIVATE_KEY="f1c2862e6a9b50fca9a1db8b7044d3814622063410a5833dd9bfb32aafaad49f"
        '''.strip()
        private_key = re.search(r'PRIVATE_KEY="(.+?)"', container_env).group(1)

        sess = requests.Session()

        # Checking C1: Login as user
        url = 'http://54.255.182.220:11000/login'
        data = {"username": "user", "password": "user"}
        r = sess.post(url, data=data, timeout=5)
        assert 'Welcome to the PDF Signature App'.lower() in r.text.lower(), 'Cannot login as user'

        pdfpath = 'receiver/files/blinkpdf_hellodocs.pdf'
        pdfbytes = open(pdfpath, 'rb').read()

        # Checking C2: Sign pdf as user
        sign_url = f'http://54.255.182.220:11000/sign'
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
        verify_url = f'http://54.255.182.220:11000/verify'
        sendata = ('main_signed.pdf', signed_pdf_stream, 'application/pdf')
        filedata = {'file': sendata}
        r = sess.post(verify_url, files=filedata, timeout=5)
        assert 'The signature is <strong>valid</strong>.' in r.text, 'Verify function not working or algoritm verify process is changed'
        
        # Checking C3: Verify invalid pdf as user
        verify_url = f'http://54.255.182.220:11000/verify'
        sendata = ('main_signed.pdf', pdfbytes, 'application/pdf')
        filedata = {'file': sendata}
        r = sess.post(verify_url, files=filedata, timeout=5)
        assert 'The signature is <strong>invalid' in r.text, 'Verify function not working or algoritm verify process is changed for invalid signature'

        host_flag = 'WreckIT50{VG09vN5bKo0cWHltUxNqegByVQjv7u7znjDRih1bhFn9zMt1V0USxQLyONOcbiLS}'
        
        # Checking C5: Login as admin and enc_flag checking
        url = f'http://54.255.182.220:11000/login'
        data = {'username': "admin", "password": f'{private_key}'}
        r = sess.post(url, data=data, timeout=5)
        assert 'Welcome to the PDF Signature App'.lower() in r.text.lower(), 'Cannot login as admin'
        url = f'http://54.255.182.220:11000/admin_panel'
        r = sess.get(url, timeout=5)
        enc_flag = r.text.split('encrypted flag: ')[1].split('</p>')[0]
        print(decryptMessage(enc_flag, private_key))
        assert decryptMessage(enc_flag, private_key).decode() == host_flag, 'Change algorithm for encryption flag'

        print('Check passed for blinkpdf')
        return True

    except Exception as e:
        print(e)
        return False
    
check()