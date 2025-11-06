from Crypto.Hash import CMAC
from Crypto.Cipher import AES
import json
import os
deviceL = [ "DEVICE_TOKEN_1",
            "DEVICE_TOKEN_2",
            "DEVICE_TOKEN_3"]

def myPost(key, mess):
    macObj = CMAC.new(key, ciphermod=AES)
    macTag = macObj.update(mess.encode()).digest()
    message = { "title": "FIGYELEM!",
                "body": mess,
                "mac": macTag.hex()}
    for token in deviceL:
        payload = { 'to': token,
                    'notification': message,
                    'priority':'high'}
        with open(token + '.json', 'wt') as f:
            json.dump(payload, f, indent = 4)

def myNotification(key):
    for token in deviceL:
        with open(token + '.json', 'rt') as f:
            payload = json.load(f)
            notifContent = payload['notification']
            mess = notifContent['body']
            macTag = bytes.fromhex(notifContent['mac'])
            currentMacObj = CMAC.new(key, ciphermod=AES)
            currentMacObj.update(mess.encode())
            try:
                currentMacObj.verify(macTag)
                print(f'token: az üzenet ÉRVÉNYES!')
            except:
                print(f'token: az üzenet ÉRVÉNYTELEN!')

key = os.urandom(32)
print(key.hex())
mess = 'Medve a kozelben! Maradj biztonsagban!'
myPost(key, mess)

# key = bytes.fromhex('...') # ide be kell írni a generált kulcs hexadecimális string értékét
# myNotification(key)