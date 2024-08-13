import ecdsa
import PyPDF2
import io
import os

def sign_pdf(file, SECRET_KEY):
    # Load secret key
    private_key = ecdsa.SigningKey.from_string(bytes.fromhex(SECRET_KEY), curve=ecdsa.SECP256k1)

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
    signature = private_key.sign(pdf_content)

    # Add signature to metadata
    pdf_writer.add_metadata({'/Signature': signature.hex()})
    signed_pdf = io.BytesIO()
    pdf_writer.write(signed_pdf)
    signed_pdf.seek(0)

    return signed_pdf

def verify_signature(file, SECRET_KEY):
    # Load secret key
    public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(SECRET_KEY), curve=ecdsa.SECP256k1)

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

    # Verify signature
    try:
        public_key.verify(signature, pdf_content)
        return True
    except ecdsa.BadSignatureError:
        return False
