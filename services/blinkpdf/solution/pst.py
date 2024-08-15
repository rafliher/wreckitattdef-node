import requests
port = 5111

sess = requests.Session()
# Checking C1: Login as user
url = f'http://localhost:{port}/login'
data = {'username': "user", "password": "user"}
r = sess.post(url, data=data, timeout=5)
assert 'Welcome to PDF Signature App'.lower() in r.text.lower(), 'Cannot login as user'

pdfbytes = open("hello_docs.pdf","rb").read()
print(len(pdfbytes))

# Checking C2: Sign as user
sign_url = f'http://localhost:{port}/sign'
bytesData = pdfbytes
sendata = ('main.pdf', bytesData, 'application/pdf')
filedata = {'file': sendata}
r = sess.post(sign_url, files=filedata, timeout=5)
# print(r.content)