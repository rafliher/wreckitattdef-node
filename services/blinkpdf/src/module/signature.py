from module.decdsa import DECDSA
import PyPDF2
import io
import os
from dotenv import load_dotenv
load_dotenv()
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

decdsa = DECDSA(privateKey=PRIVATE_KEY)

def sign_pdf(file):
    # Read PDF
    pdf_reader = PyPDF2.PdfReader(file)
    pdf_writer = PyPDF2.PdfWriter()

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    # Get PDF content
    pdf_data = io.BytesIO()
    pdf_writer.write(pdf_data)
    pdf_data.seek(0)
    pdf_content = pdf_data.read()

    # Create a signature
    signature = decdsa.sign(pdf_content)

    # Add signature to metadata
    pdf_writer.add_metadata({'/Signature': signature.hex()})
    signed_pdf = io.BytesIO()
    pdf_writer.write(signed_pdf)
    signed_pdf.seek(0)

    return signed_pdf

def verify_signature(file):
    # Read PDF
    pdf_reader = PyPDF2.PdfReader(file)
    signature_text = pdf_reader.metadata.get('/Signature', '')
    signature = bytes.fromhex(signature_text)

    # Get PDF content
    pdf_data = io.BytesIO()
    pdf_writer = PyPDF2.PdfWriter()

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    pdf_writer.write(pdf_data)
    pdf_data.seek(0)
    pdf_content = pdf_data.read()

    return decdsa.verify(pdf_content,signature)