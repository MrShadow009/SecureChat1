import pqcrypto

def generate_keys():
    """
    Generate Falcon key pair.
    Returns public key and secret key as bytes.
    """
    public_key, secret_key = pqcrypto.sign.falcon512.keypair()
    return public_key, secret_key

def sign(secret_key, message):
    """
    Sign a message using the secret key.
    Returns the signature.
    """
    signature = pqcrypto.sign.falcon512.sign(secret_key, message)
    return signature

def verify(public_key, message, signature):
    """
    Verify a signature using the public key.
    Returns True if valid, False otherwise.
    """
    return pqcrypto.sign.falcon512.verify(public_key, message, signature)
