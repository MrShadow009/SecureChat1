import pqcrypto

def generate_keys():
    """
    Generate SABER key pair.
    Returns public key and secret key as bytes.
    """
    public_key, secret_key = pqcrypto.kem.saber.keypair()
    return public_key, secret_key

def encapsulate(public_key):
    """
    Encapsulate a shared secret using the public key.
    Returns ciphertext and shared secret.
    """
    ciphertext, shared_secret = pqcrypto.kem.saber.encapsulate(public_key)
    return ciphertext, shared_secret

def decapsulate(secret_key, ciphertext):
    """
    Decapsulate the shared secret using the secret key and ciphertext.
    Returns the shared secret.
    """
    shared_secret = pqcrypto.kem.saber.decapsulate(secret_key, ciphertext)
    return shared_secret
