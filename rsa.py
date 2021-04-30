# rsa.py
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend


def get_private_key():
    """Generates random private key."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key


def get_public_key(private_key):
    """Generates public key based on private key."""
    return private_key.public_key()


def encrypt(public_key, plaintext):
    """Encrypts provided plaintext with the provided public key."""
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext


def decrypt(private_key, ciphertext):
    """Decrypts provided ciphertext with the provided private key."""
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext


def export_private_key(private_key):
    """Exports private key into a file named 'private_key.pem'"""
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open("private_key.pem", "wb") as file:
        file.write(pem)
        file.close()


def import_key(filename):
    """Imports private key from a specified file name."""
    with open(filename, 'rb') as file:
        content = file.read()
    key = load_pem_private_key(content, None, default_backend())
    return key


# main function for debugging
if __name__ == "__main__":
    message = "data"
    message = bytes(message, 'ascii')
    print(message)

    priv_key1 = import_key("private_key.pem")
    pub_key1 = get_public_key(priv_key1)

    ciphertext = encrypt(pub_key1, message)
    # store_ciphertext(ciphertext)
    print(ciphertext)

    plaintext = decrypt(priv_key1, ciphertext)
    plaintext = plaintext.decode('ascii')
    print(plaintext)

