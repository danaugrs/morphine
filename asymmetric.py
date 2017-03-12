# Project modules
import symmetric
from config import *

# Python modules
import numpy as np


def keygen():
    """Generate private and public keys."""

    # Generate regular secret key
    sk = symmetric.keygen()

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


if __name__ == '__main__':

    sk, pk = keygen()
    assert symmetric.decrypt(sk, encrypt(pk, 0)) == 0
    assert symmetric.decrypt(sk, encrypt(pk, 1)) == 1

    from testing import consistency

    def keygenEncryptDecrypt(b):
        """asymmetric keygen-encrypt-decrypt (bit = {0})"""
        sk, pk = keygen()
        c = encrypt(pk, b)
        return symmetric.decrypt(sk, c)

    consistency(keygenEncryptDecrypt, (0,), 0, 10**5)
    consistency(keygenEncryptDecrypt, (1,), 1, 10**5)