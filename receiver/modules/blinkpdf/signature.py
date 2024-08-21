from .decdsa import DECDSA
import PyPDF2
import io

def sign_pdf(file, PRIVATE_KEY):
    try:
        decdsa = DECDSA(privateKey=PRIVATE_KEY)
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
            
        pdf_data = io.BytesIO()
        pdf_writer.write(pdf_data)
        pdf_data.seek(0)
        pdf_content = pdf_data.read()
        signature = decdsa.sign(pdf_content)
        pdf_writer.add_metadata({'/Signature': signature.hex()})
        signed_pdf = io.BytesIO()
        pdf_writer.write(signed_pdf)
        signed_pdf.seek(0)
        return signed_pdf
    except:
        return False

def verify_signature(file, PRIVATE_KEY):
    try:
        decdsa = DECDSA(privateKey=PRIVATE_KEY)
        pdf_reader = PyPDF2.PdfReader(file)
        signature_text = pdf_reader.metadata.get('/Signature', '')
        signature = bytes.fromhex(signature_text)
        pdf_data = io.BytesIO()
        pdf_writer = PyPDF2.PdfWriter()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        pdf_writer.write(pdf_data)
        pdf_data.seek(0)
        pdf_content = pdf_data.read()
        return decdsa.verify(pdf_content,signature)
    except Exception as e:
        print(e)
        return False