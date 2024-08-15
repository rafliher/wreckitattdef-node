import requests
from io import BytesIO
from signature import *
port = 5111

sess = requests.Session()
# Checking C1: Login as user
url = f'http://localhost:{port}/login'
data = {'username': "user", "password": "user"}
r = sess.post(url, data=data, timeout=5)
assert 'Welcome to PDF Signature App'.lower() in r.text.lower(), 'Cannot login as user'

# print(len(pdfbytes))

PRIVATE_KEY="fc901109936ed47102fb4b6df75b2058421dfde75d8e0357f92713aace97fdf0"

# Checking C2: Sign as user
sign_url = f'http://localhost:{port}/sign'
pdfbytes = open("hello_docs.pdf","rb").read()
sendata = ('main.pdf', pdfbytes, 'application/pdf')
filedata = {'file': sendata}
r = sess.post(sign_url, files=filedata, timeout=5)
print(r.headers['Content-Type'])
signed_pdf = r.content
signed_pdf_stream = BytesIO(signed_pdf)
print(verify_signature(signed_pdf_stream, PRIVATE_KEY))

pdf_bytes_stream = BytesIO(pdfbytes)
signed_pdf_stream = sign_pdf(pdf_bytes_stream, PRIVATE_KEY)
verify_url = f'http://localhost:{port}/verify'
sendata = ('main_signed.pdf', signed_pdf_stream, 'application/pdf')
filedata = {'file': sendata}
r = sess.post(verify_url, files=filedata, timeout=5)
print('The signature is valid' in r.text)

verify_url = f'http://localhost:{port}/verify'
sendata = ('main_signed.pdf', pdfbytes, 'application/pdf')
filedata = {'file': sendata}
r = sess.post(verify_url, files=filedata, timeout=5)
# print(r.text)
print('The signature is invalid' in r.text)
