from flask import Flask, request, render_template, send_file, redirect, url_for
import ecdsa
import PyPDF2
import io
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv('ECDSA_SECRET_KEY')

app = Flask(__name__)

def sign_pdf(file):
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

def verify_signature(file):
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('sign'))
        
        file = request.files['file']
        if file.filename == '' or not file.filename.lower().endswith('.pdf'):
            return "Only PDF files are allowed."

        signed_pdf = sign_pdf(file)
        return send_file(signed_pdf, attachment_filename='signed_file.pdf', as_attachment=True)
    
    return render_template('sign.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('verify'))

        file = request.files['file']
        if file.filename == '' or not file.filename.lower().endswith('.pdf'):
            return "Only PDF files are allowed."

        is_valid = verify_signature(file)
        return render_template('verify_result.html', is_valid=is_valid)
    
    return render_template('verify.html')

if __name__ == '__main__':
    app.run(debug=True)