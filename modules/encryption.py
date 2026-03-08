import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

#symmetric encryption using AES-GCM
def aes_encrypt(message):
    key = secrets.token_bytes(32)  # Generate a random 256-bit key
    nonce = secrets.token_bytes(12)  # Generate a random 96-bit nonce
    aes = AESGCM(key)
    ciphertext = nonce + aes.encrypt(nonce, message ,None)#ncrypt the message and prepend the nonce
    return key.hex(), ciphertext.hex()

def aes_decrypt(ciphertext_hex, key_hex):
    try:
        key = bytes.fromhex(key_hex.strip())
        full_ciphertext = bytes.fromhex(ciphertext_hex.strip())
        nonce = full_ciphertext[:12]
        ciphertext = full_ciphertext[12:]
        aes = AESGCM(key)
        plaintext = aes.decrypt(nonce, ciphertext, None)
        return plaintext.decode()
    except Exception as e:
        return f"Decryption failed: {str(e)}"

#asymmetric encryption using RSA
def rsa_encrypt(message):
    # Generate RSA key pair
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()
    )
    return pem.decode(), ciphertext.hex()

def rsa_decrypt(ciphertext_hex, private_key_pem):
    try:
        private_key = serialization.load_pem_private_key(private_key_pem.encode(), password=None)
        ciphertext = bytes.fromhex(ciphertext_hex)
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        return plaintext.decode()
    except Exception as e:
        return f"Decryption failed: {str(e)}"
