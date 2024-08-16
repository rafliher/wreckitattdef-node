import requests
import sys
import os
import hashlib
from sage.all import matrix, Integer, Zmod, vector
# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from src.module import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import PyPDF2
from src.module.decdsa import *
from ecdsa import NIST256p
curve = NIST256p
order = int(curve.order)

# url = 'http://localhost:5111'
url = 'http://13.250.57.255:11000'

# checking Login
def login(userData):
    sess = requests.Session()
    r = sess.post(url+'/login', data=userData, timeout=5)
    assert 'Welcome to'.lower() in r.text.lower()
    return sess

# sending pdf
def sendPdf(session, pdfbytes):
    sendata = ('main.pdf', pdfbytes, 'application/pdf')
    filedata = {'file': sendata}
    r = session.post(url+'/sign', files=filedata, timeout=5)
    signed_pdf = r.content
    signed_pdf_stream = io.BytesIO(signed_pdf)
    return signed_pdf_stream

def getFlag(session, private):
    r = session.get(url+'/admin_panel', timeout=5)
    enc_flag = r.text.split("encrypted flag: ")[1].split("</p>")[0]
    return decryptMessage(enc_flag, private)

# create pdf
def create_pdf_bytes(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setTitle("Simple PDF")
    c.drawString(100, 750, text)
    c.showPage()
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes

# extract signature and data
def extractPdf(pdfbytes):
    pdf_reader = PyPDF2.PdfReader(pdfbytes)
    signature_text = pdf_reader.metadata.get('/Signature', '')
    signature = bytes.fromhex(signature_text)
    pdf_data = io.BytesIO()
    pdf_writer = PyPDF2.PdfWriter()
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    pdf_writer.write(pdf_data)
    pdf_data.seek(0)
    pdf_content = pdf_data.read()
    return pdf_content,signature

# make an dataset signature
def createDataset(session, inc):
    ecdsa = DECDSA("ababab")
    dataset = []
    for i in range(inc):
        temp = str(random.getrandbits(512))
        pdfbytes = create_pdf_bytes(temp)
        signedData = sendPdf(session, pdfbytes)
        content, sign = extractPdf(signedData)
        r1, r2, s = ecdsa.bytes_to_sign(sign)
        message = content
        m1, m2 = message[:len(message)//2], message[len(message)//2:]
        h1 = hashlib.sha256(m1).digest()
        h2 = hashlib.sha256(m2).digest()
        z1 = int.from_bytes(h1, byteorder='big') % order
        z2 = int.from_bytes(h2, byteorder='big') % order
        dataset.append([temp, z1, z2, r1, r2, s])
    return dataset

# attack 
def biasedNonce(dataset, inc):
    B = 2**201
    p = order
    Zn = Zmod(p)

    m = [[order,0] + [-Integer((pow(dataset[i-1][5], -1, order)*(dataset[i-1][1]+dataset[i-1][2])-pow(dataset[i][5], -1, order)*(dataset[i][1]+dataset[i][2]))%order) for i in range(1, inc)]]
    m += [[0,Integer(B)/order] + [Integer((pow(dataset[i-1][5], -1, order)*(dataset[i-1][3]+dataset[i-1][4])-pow(dataset[i][5], -1, order)*(dataset[i][3]+dataset[i][4]))%order) for i in range(1, inc)]]
    inc -= 1
    m += [[0,0]+[0]*i+[order]+[0]*(inc-i-1) for i in range(inc)]

    Mat = matrix(m)
    # W = Babai_closest_vector(Mat, Y)
    # x = W[1] * (p-1) / 2
    # print(x)
    for line in Mat.LLL():
        if(line[0]==order):
            key = Zn(line[1]*p/B)
            return order-key

def main():
    userData = {'username': "user", "password": "user"}
    session = login(userData)
    inc = 80
    dataset = createDataset(session, inc)
    print("success generate dataset:",len(dataset))
    private = hex(int(biasedNonce(dataset, inc)))[2:]
    adminData = {'username': "admin", "password": private}
    session = login(adminData)
    flag = getFlag(session, private)
    print(flag)

main()

