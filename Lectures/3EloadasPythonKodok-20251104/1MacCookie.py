from Crypto.Hash import CMAC
from Crypto.Cipher import AES
import base64, os
import flask

def calcMacValue(key, mess):
    macTag = CMAC.new(key, mess.encode(), ciphermod=AES).digest()
    macAuth = base64.b64encode(mess.encode() + b'.' + macTag).decode()
    return macAuth

def macValueVerify(key, macAuth):
    try:
        decoded = base64.b64decode(macAuth.encode())
        mess, macTag = decoded.rsplit(b'.', 1)
        currentMacTag = CMAC.new(key, mess, ciphermod=AES).digest()
        print('currentMacTag: ', currentMacTag)
        if currentMacTag == macTag:
            return mess.decode()
    except Exception:
        pass
    return None

app = flask.Flask(__name__)
secretKey = os.urandom(16)

@app.route('/set')
def set_cookie():
    userId = 'crypto.user@gmail.com'
    macAuth = calcMacValue(secretKey, userId)
    resp = flask.make_response('Cookie beállítva.')
    resp.set_cookie('session', macAuth,
                    httponly=True, secure=True)
    return resp


@app.route('/get')
def get_cookie():
    macAuth = flask.request.cookies.get('session')
    user_id = macValueVerify(secretKey, macAuth)
    if user_id:
        return f'a user_id ID hiteles!'
    else:
        return 'Hibás vagy manipulált cookie.'

app.run(debug=True, port=5000)