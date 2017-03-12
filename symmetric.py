# Project modules
from config import *

# Python modules
import random


def keygen():
    """Generate a key (i.e. a random odd integer between 2^N and 2^P)."""
    # return (random.randint(2**N, 2**(P-1) -1) << 1) + 1
    return (random.randint(2**(P-2), 2**(P-1) -1) << 1) + 1
    # NOTE: The lower bound of 2**N makes sure decryption works 100% of the time.
    # If the lower bound were 0 (i.e. the odd integer were truly random in P), it would mean that the secret key
    # could be smaller then the N-bit integer 'm' generated during encryption, in which case decryption would fail.


def encrypt(sk, b, mbits=N):
    """Encrypt a bit into a Q-bit integer based on the provided key."""

    # Random N-bit integer with the same parity as b
    # m = (random.randint(0, 2**(mbits-1) -1) << 1) + b
    m = (random.randint(2**(mbits-2), 2**(mbits-1) -1) << 1) + b
    
    # Random Q-bit integer
    q = random.randint(2**(Q-1), 2**Q) - 1
    # q = random.randint(0, 2**Q) - 1
    
    return (m + sk*q)
    

def decrypt(sk, c):
    """Decrypt a cyphertext based on the provided key."""
    return (c % sk) % 2


if __name__ == '__main__':

    key = keygen()
    assert decrypt(key, encrypt(key, 0)) == 0
    assert decrypt(key, encrypt(key, 1)) == 1

    from testing import consistency

    T = 10**6

    def keygenEncryptDecrypt(b):
        """symmetric keygen-encrypt-decrypt (bit = {0})"""
        key = keygen()
        c = encrypt(key, b)
        return decrypt(key, c)

    consistency(keygenEncryptDecrypt, (0,), 0, T)
    consistency(keygenEncryptDecrypt, (1,), 1, T)

    def keygenEncryptSum(b1, b2):
        """symmetric keygen-encrypt-sum ({0}+{1})"""
        key = keygen()
        c1 = encrypt(key, b1)
        c2 = encrypt(key, b2)
        return decrypt(key, c1 + c2)

    consistency(keygenEncryptSum, (0,0), 0, T)
    consistency(keygenEncryptSum, (0,1), 1, T)
    consistency(keygenEncryptSum, (1,1), 0, T)

    def keygenEncryptMult(b1, b2):
        """symmetric keygen-encrypt-mult ({0}+{1})"""
        key = keygen()
        c1 = encrypt(key, b1)
        c2 = encrypt(key, b2)
        return decrypt(key, c1 * c2)

    consistency(keygenEncryptMult, (0,0), 0, T)
    consistency(keygenEncryptMult, (0,1), 0, T)
    consistency(keygenEncryptMult, (1,1), 1, T)

    # TODO find max multiplicative depth with 100% consistency
    # Need to create testing util