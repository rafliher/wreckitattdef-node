from modules.blinkpdf import *

import io
import requests
import subprocess
import re


def check():
    try:
        # Getting private key
        container_env = '''
SECRET_KEY="a3a591c71b14fa8837dca5eb61ec8b14"
PRIVATE_KEY="ceb4fd7181f056b048412a2bef7402991fdf3b8300f07e6617889cb7064cc529"
        '''.strip()
        private_key = re.search(r'PRIVATE_KEY="(.+?)"', container_env).group(1)

        sess = requests.Session()

        # Checking C1: Login as user
        url = 'http://52.221.251.25:11000/login'
        data = {"username": "user", "password": "user"}
        r = sess.post(url, data=data, timeout=5)
        assert 'Welcome to the PDF Signature App'.lower() in r.text.lower(), 'Cannot login as user'

        pdfpath = 'receiver/files/blinkpdf_hellodocs.pdf'
        pdfbytes = open(pdfpath, 'rb').read()

        # Checking C2: Sign pdf as user
        sign_url = 'http://52.221.251.25:11000/sign'
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
        verify_url = 'http://52.221.251.25:11000/verify'
        sendata = ('main_signed.pdf', signed_pdf_stream, 'application/pdf')
        filedata = {'file': sendata}
        r = sess.post(verify_url, files=filedata, timeout=5)
        assert 'The signature is <strong>valid</strong>.' in r.text, 'Verify function not working or algoritm verify process is changed'
        
        # Checking C3: Verify invalid pdf as user
        verify_url = 'http://52.221.251.25:11000/verify'
        sendata = ('main_signed.pdf', pdfbytes, 'application/pdf')
        filedata = {'file': sendata}
        r = sess.post(verify_url, files=filedata, timeout=5)
        assert 'The signature is <strong>invalid' in r.text, 'Verify function not working or algoritm verify process is changed for invalid signature'

        host_flag = 'WreckIT50{1D3rZiz8CrMuO2b2QGsQVQqvk8dLjDCBnmTHV6dGzQ0zZXOScP69b2LxKV2cj7Ut}'
        
        # Checking C5: Login as admin and enc_flag checking
        url = 'http://52.221.251.25:11000/login'
        data = {'username': "admin", "password": f'{private_key}'}
        r = sess.post(url, data=data, timeout=5)
        assert 'Welcome to the PDF Signature App'.lower() in r.text.lower(), 'Cannot login as admin'
        url = f'http://52.221.251.25:11000/admin_panel'
        r = sess.get(url, timeout=5)
        enc_flag = r.text.split('encrypted flag: ')[1].split('</p>')[0]
        cek, dec = decryptMessage(enc_flag, private_key)
        assert dec.decode() == host_flag, 'Change algorithm for encryption flag'
        assert cek == True, 'Change signature algorithm for encryption flag'

        print('Check passed for blinkpdf')
        return True

    except Exception as e:
        print(e)
        return False
    
check()