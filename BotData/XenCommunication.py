import requests
import hashlib
from base64 import b64encode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

def encrypt(str2encrypt):
    password = ""  # Enter key here
    plain_text = str2encrypt
    salt = get_random_bytes(AES.block_size)
    private_key = hashlib.scrypt(
        password.encode(),
        salt=salt,
        n=2 ** 14,
        r=8,
        p=1,
        dklen=32,
        )
    cipher_config = AES.new(private_key, AES.MODE_GCM)
    (cipher_text, tag) = \
        cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))
    encryptedDict = {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8'),
        }
    encryptedString = encryptedDict['cipher_text'] + '*' \
        + encryptedDict['salt'] + '*' + encryptedDict['nonce'] + '*' \
        + encryptedDict['tag']
    return encryptedString

def send_command(data2send, comname):
    data2send = data2send.replace(" ", "%20")
    command = str(comname) + ":" + data2send
    command = encrypt(command)
    payload = {'command': command}
    requests.post("https://xenial.network", data=payload)
    
'''
usage:
check commands.txt
'''
