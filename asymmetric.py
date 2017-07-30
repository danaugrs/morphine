# Project modules
import symmetric
from config import *

# Python modules
import numpy as np


def keygen(kt=symmetric.KeyType.RANDOM):
    """Generate private and public keys."""

    # Generate regular secret key
    sk = symmetric.keygen(kt)

    # Generate a set of encryptions of zero
    pk = [symmetric.encrypt(sk, 0, PK_M_BIT_LENGTH) for i in range(PK_SIZE)]

    return (sk, pk)


def encrypt(pk, b):
    """Encrypt a bit b into an integer based on a public key."""

    # Choose a random subset of the pk's encrypted zeros
    idxs = np.random.choice(np.arange(PK_SIZE), PK_SUBSET_SIZE, replace=False)
    
    # Sum subset of encrypted zeros along with the bit to be encrypted
    cypher = b + sum([pk[i] for i in idxs])
        
    return cypher


def decrypt(sk, c):
    """Decrypt using the normal symmetric algorithm."""
    return symmetric.decrypt(sk, c)


if __name__ == '__main__':

    sk, pk = keygen()
    assert decrypt(sk, encrypt(pk, 0)) == 0
    assert decrypt(sk, encrypt(pk, 1)) == 1

    from testing import consistency

    T = 10**5

    def keygenEncryptDecrypt(b):
        """asymmetric keygen-encrypt-decrypt (bit = {0})"""
        sk, pk = keygen()
        c = encrypt(pk, b)
        return decrypt(sk, c)

    consistency(keygenEncryptDecrypt, (0,), 0, T)
    consistency(keygenEncryptDecrypt, (1,), 1, T)

    def keygenEncryptSum(b1, b2):
        """asymmetric keygen-encrypt-sum ({0}+{1})"""
        sk, pk = keygen()
        c1 = encrypt(pk, b1)
        c2 = encrypt(pk, b2)
        return decrypt(sk, c1 + c2)

    consistency(keygenEncryptSum, (0,0), 0, T)
    consistency(keygenEncryptSum, (0,1), 1, T)
    consistency(keygenEncryptSum, (1,1), 0, T)

    def keygenEncryptMult(b1, b2):
        """asymmetric keygen-encrypt-mult ({0}*{1})"""
        sk, pk = keygen()
        c1 = encrypt(pk, b1)
        c2 = encrypt(pk, b2)
        return decrypt(sk, c1 * c2)

    consistency(keygenEncryptMult, (0,0), 0, T)
    consistency(keygenEncryptMult, (0,1), 0, T)
    consistency(keygenEncryptMult, (1,1), 1, T)
