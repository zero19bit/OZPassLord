import json
import os
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64




def save_vault(passwords, masterPass, filePath):
    salt = os.urandom(16)
    key = derive_key(masterPass, salt)
    enc_contact = encrypt_data(passwords, key)
    final = {
        "salt" : base64.b64encode(salt).decode('utf-8'),
        "vault" : enc_contact
    }
    with open(filePath, 'w') as file:
        json.dump(final, file)


def derive_key(masterPass, salt):
    KDF = Argon2id(
        salt=salt,
        length=32,
        iterations=3,
        lanes=4,
        memory_cost=65536
    )
    return KDF.derive(masterPass.encode("utf-8"))


def encrypt_data(data, key):
    aesgcm = AESGCM(key=key)
    nonce = os.urandom(12)
    plainText = json.dumps(data).encode("utf-8")
    cipherText = aesgcm.encrypt(nonce, plainText, None)
    return{
        "nonce" : base64.b64encode(nonce).decode('utf-8'),
        "cipherText" : base64.b64encode(cipherText).decode('utf-8')
    }


def load_vault(masterPass , filePath):
    with open(filePath, 'r') as file:
        raw = json.load(file)
    salt = base64.b64decode(raw["salt"].encode('utf-8'))
    key = derive_key(masterPass, salt)
    return decrypt_data(raw["vault"], key)

def decrypt_data(enc_contact, kay):
    aesgcm = AESGCM(kay)
    nonce = base64.b64decode(enc_contact["nonce"].encode("utf-8"))
    cipherText = base64.b64decode(enc_contact["cipherText"].encode('utf-8'))
    plainText = aesgcm.decrypt(nonce, cipherText, None)
    return json.loads(plainText.decode('utf-8'))
