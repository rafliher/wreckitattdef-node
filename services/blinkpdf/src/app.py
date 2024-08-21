from flask import Flask, request, render_template, redirect, url_for, session, send_file
import base64
import os
from dotenv import load_dotenv
from module import sign_pdf, verify_signature, handleLogin, encryptMessage

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

def generate_token(username, isAdmin):
    token_string = f"{username}:{SECRET_KEY}:{isAdmin}"
    token = base64.b64encode(token_string.encode()).decode()
    return token

def verify_token(token):
    try:
        decoded_token = base64.b64decode(token).decode()
        username, key, isAdmin = decoded_token.split(':')
        if(key==SECRET_KEY): return {'status': True, 'data': {'username':username, 'isAdmin':isAdmin=='True'}}
        else: return {'status': False}
        
    except (ValueError, TypeError):
        return None

@app.route('/admin_panel')
def admin_panel():
    if 'token' in session:
        verifies = verify_token(session['token'])
        if(verifies['status']):
            decoded_token_data = verifies['data'] 
            if decoded_token_data['isAdmin']:
                FLAG = b''
                try:
                    FLAG = open("/flag.txt","rb").read()
                except:
                    FLAG = b'WRECKIT50{PLACEHOLDER}'
                encrypted_flag = encryptMessage(FLAG, os.getenv('PRIVATE_KEY'))
                return render_template('admin_panel.html', isAdmin=decoded_token_data['isAdmin'], enc_flag=encrypted_flag)
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'token' in session:
        verifies = verify_token(session['token'])
        if(verifies['status']):
            decoded_token_data = verifies['data']
            return render_template('index.html', isAdmin=decoded_token_data['isAdmin'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        wasLogin = handleLogin(username, password)
        if wasLogin['status']:
            token = generate_token(username, wasLogin['isAdmin'])
            session['token'] = token
            return redirect(url_for('index'))
        return redirect(url_for('login', error='Invalid username or password'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('index'))

@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if 'token' in session:
        verifies = verify_token(session['token'])
        if(verifies['status']):
            decoded_token_data = verifies['data']
            if request.method == 'POST':
                if 'file' not in request.files:
                    return redirect(url_for('sign'), error='File not Found!')
                
                file = request.files['file']
                if file.filename == '' or not file.filename.lower().endswith('.pdf'):
                    return redirect(url_for('sign', error='Only PDF files are allowed.'))

                signed_pdf_data = sign_pdf(file, os.getenv('PRIVATE_KEY'))
                return send_file(signed_pdf_data, 
                            mimetype='application/pdf', 
                            as_attachment=True, 
                            download_name=file.filename.split('.pdf')[0]+'_signed.pdf')
            
            return render_template('sign.html', isAdmin=decoded_token_data['isAdmin'])
    return redirect(url_for('login'))

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'token' in session:
        verifies = verify_token(session['token'])
        if(verifies['status']):
            decoded_token_data = verifies['data']
            if request.method == 'POST':
                if 'file' not in request.files:
                    return redirect(url_for('verify'), error='File not Found!')

                file = request.files['file']

                if file.filename == '' or not file.filename.lower().endswith('.pdf'):
                    return redirect(url_for('verify', error='Only PDF files are allowed.'))

                is_valid = verify_signature(file, os.getenv('PRIVATE_KEY'))
                return render_template('verify_result.html', is_valid=is_valid, isAdmin=decoded_token_data['isAdmin'])
            
            return render_template('verify.html', isAdmin=decoded_token_data['isAdmin'])
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True,port="5111",host="0.0.0.0")