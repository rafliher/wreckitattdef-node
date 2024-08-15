import hashlib
import base64

pathDB = 'db.db'

def handleLogin(username, password):
    with open(pathDB, 'rb') as f:
        listData = f.readlines()
        for line in listData:
            data = line.strip().split(b";")
            if(base64.b64encode(username.encode())==data[0]):
                if(hashlib.sha256(password.encode()).hexdigest().encode()==data[1]):
                    return {'status': True, 'message': 'Successfully Login', 'isAdmin': b'True'==data[2]}
                else: return {'status': False, 'message': 'Wrong Password'}
        return {'status': False, 'message': 'Username not found'}

def register(username, password, isAdmin):
    with open(pathDB, 'ab') as f:
        hashPassword = hashlib.sha256(password.encode()).hexdigest().encode()
        baseUsername = base64.b64encode(username.encode())
        appendData = b''
        if(isAdmin): appendData += baseUsername+b';'+hashPassword+b';True\n'
        else: appendData += baseUsername+b';'+hashPassword+b';False\n'
        f.write(appendData)
        print("Successfully append for username:",username)

def reset():
    with open(pathDB, 'wb') as f:
        pass