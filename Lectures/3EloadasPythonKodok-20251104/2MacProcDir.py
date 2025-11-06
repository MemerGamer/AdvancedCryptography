import sys
import os
import hmac
import hashlib

def calcMacValue(key, fullPath):
    h = hmac.new(key, digestmod=hashlib.sha256)
    with open(fullPath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def processDirectory(key, directory):
    for root, _, files in os.walk(directory):
        for filename in files:
            fullPath = os.path.join(root, filename)
            try:
                code = calcMacValue(key, fullPath)
                print(f'filename mac tag: {code}')
            except Exception as e:
                print(f'Hiba a fájl feldolgozása közben:{fullPath}\n {e}')

secretKey = b'my secret key for directories'
if len(sys.argv) != 2:
    print('Használat: python 2MacProcDir.py <mappa útvonal>')
else:
    processDirectory(secretKey, sys.argv[1])

# PyCharm, Edit Configurations- beállitani az utvonalat
