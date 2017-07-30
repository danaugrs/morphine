# Project modules
from config import *

# Python modules
import random


class KeyType:
    SMALLEST = 0
    RANDOM = 1
    LARGEST = 2


def keygen(kt=KeyType.RANDOM):
    """Generate a key (i.e. a random odd integer between 2^(P-1) and 2^P)."""
    lowerBound = 2**(P-2)
    higherBound = 2**(P-1) - 1
    if kt == KeyType.SMALLEST:
        half = lowerBound
    elif kt == KeyType.LARGEST:
        half = higherBound
    elif kt == KeyType.RANDOM:
        half = random.randint(lowerBound, higherBound)
    return (half << 1) + 1
    # NOTE: If the lower bound were 0 (i.e. the odd integer were truly random in P), it would mean that the secret key
    # could be smaller then the N-bit integer 'm' generated during encryption, in which case decryption would fail.


def encrypt(sk, b, mbits=N):
    """Encrypt a bit into a Q-bit integer based on the provided key."""

    # Random N-bit integer with the same parity as b
    m = (random.randint(2**(mbits-2), 2**(mbits-1) -1) << 1) + b
    
    # Random Q-bit integer
    q = random.randint(2**(Q-1), 2**Q) - 1
    
    return (m + sk*q)


def encryptD(sk, b, mbits=N):
    """Same as encrypt except it returns Q as well to allow computation of the noise."""

    # Random N-bit integer with the same parity as b
    m = (random.randint(2**(mbits-2), 2**(mbits-1) -1) << 1) + b
    
    # Random Q-bit integer
    q = random.randint(2**(Q-1), 2**Q) - 1
    
    return ((m + sk*q), q)
    

def decrypt(sk, c):
    """Decrypt a cyphertext based on the provided key."""
    return (c % sk) % 2


def noise(sk, c):
    """Get the noise of a cyphertext based on the provided key."""
    return (c % sk)


def noiseQ(sk, c, q):
    """Get the noise of a cyphertext based on the provided key."""
    return (c - sk*q)


if __name__ == '__main__':

    key = keygen()
    assert decrypt(key, encrypt(key, 0)) == 0
    assert decrypt(key, encrypt(key, 1)) == 1

    # Print smallest and largest key sizes
    sk = keygen(KeyType.SMALLEST)
    print('Smallest Key:', sk)
    print('Largest Key:', keygen(KeyType.LARGEST), '\n')

    # Calculate Max Multiplicative Depth
    print('Calculating max multiplicative depth...')
    c, q = encryptD(sk, 0)
    mmd = -1
    for i in range(10):
        m = decrypt(sk, c)
        cumulative_noise = noiseQ(sk, c, q)
        print("[i = {0}] noise = {1} | b = {2}".format(i, cumulative_noise, m))
        if cumulative_noise > sk:
            break
        mmd += 1
        (c2, q2) = encryptD(sk, 0)
        q = noise(sk, c)*q2 + noise(sk, c2)*q + sk*q*q2
        c *= c2
    print('Max Multiplicative Depth:', mmd, '\n')

    # Calculate Max Additive Depth
    print('Calculating max additive depth...')
    mads = []
    for j in range(30):
        c, q = encryptD(sk, 0)
        mad = -1
        for i in range(10000):
            m = decrypt(sk, c)
            cumulative_noise = noiseQ(sk, c, q)
            if cumulative_noise > sk:
                break
            mad += 1
            (c2, q2) = encryptD(sk, 0)
            q += q2
            c += c2
        mads.append(mad)
    print('Max Additive Depth:', min(mads))

    from testing import consistency
    T = 10**5

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
        """symmetric keygen-encrypt-mult ({0}*{1})"""
        key = keygen()
        c1 = encrypt(key, b1)
        c2 = encrypt(key, b2)
        return decrypt(key, c1 * c2)

    consistency(keygenEncryptMult, (0,0), 0, T)
    consistency(keygenEncryptMult, (0,1), 0, T)
    consistency(keygenEncryptMult, (1,1), 1, T)
