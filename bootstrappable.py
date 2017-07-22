# Project modules
import asymmetric
from config import *

# Python modules
from decimal import *
import random
import numpy as np

getcontext().prec = Q


def generate_ssp_set(size, subset_size, sumto):
    """
    Generate random set of Decimals such that a subset sums to a given value.
    https://en.wikipedia.org/wiki/Subset_sum_problem
    """

    # Generate set with entries uniformly distributed between 0 and 2*average
    average = sumto / Decimal(size)
    ssp_set = [Decimal(random.random()) * 2 * average for i in range(size)]

    # Choose a random subset
    idxs = np.random.choice(np.arange(size), subset_size, replace=False)

    # Adjust subset values to ensure they sum to 'sumto'
    sumto_initial = sum([ssp_set[i] for i in idxs])
    divdiff = (sumto - sumto_initial)/Decimal(subset_size)
    ssp_set = [v+divdiff for v in ssp_set]

    # Return the choice of subset encoded as a binary array with Hamming weigth of 'subset_size'
    subset = [1 if i in idxs else 0 for i in range(size)]

    return (subset, ssp_set)


def keygen():
    """
    Generate private and public keys for the "greased", bootstrappable encryption scheme.
    
    The main idea here is that we want to minimize computation during decryption because it originally contains
    an expensive modulus operation (c % p) that is too much for our somewhat homomorphic encryption system to handle
    in a single recrypt. We would like to substitute that expensive operation by a small summation. To do that we
    include a set with the public key that contains a hidden subset that sums to 1/p. We call that the SSP set.
    The secret key then becomes the binary vector encoding that subset. The SSP set is provided as part of the public
    key, along with the set of encryptions of zero.
    """

    # Generate a regular key pair
    p, pk_z = asymmetric.keygen()

    # Generate a set of rational numbers such that a hidden subset sums to 1/p
    hint = (Decimal(1)/Decimal(p))
    sk, pk_y = generate_ssp_set(HINT_SIZE, HINT_SUBSET_SIZE, hint)  
    
    return (sk, pk_z, pk_y)


def encrypt(pk_z, pk_y, b):
    """Encrypt a bit b into an array of integers based on the provided public key."""

    # Perform regular asymmetric encryption
    c = asymmetric.encrypt(pk_z, b)

    # Post process the cypher text to generate the appropriate 1/p SPP set
    cy = post_process(c, pk_y)

    return (c, cy)


def post_process(c, pk_y):
    """
    Post-process the cyphertext with pk_y to simplify computation during decryption.
    
    We compute and return the 1/p SSP set for the provided cyphertext before decryption takes place.
    This is one of the key steps in making our homomorphic encryption scheme bootstrappable.
    """
    return [Decimal(c) * Decimal(y) for y in pk_y]


def decrypt(sk, c, cy):
    """Decrypt a bit (c, cz) based on sk."""

    # Decode/compute hidden subset sum given secret key
    x = round(sum([cy[i] if sk[i] > 0 else 0 for i in range(HINT_SIZE)]))
    
    lsb_x = x & 1
    lsb_c = c & 1
    
    # XOR the least significant bits together
    return lsb_c ^ lsb_x


if __name__ == '__main__':

    sk, ssp = generate_ssp_set(5, 2, Decimal(3.14159265))
    assert float(sum([ssp[i] if sk[i] else 0 for i in range(5)])) == 3.14159265

    sk, pk_z, pk_y = keygen()
    assert decrypt(sk, *encrypt(pk_z, pk_y, 0)) == 0
    assert decrypt(sk, *encrypt(pk_z, pk_y, 1)) == 1

    from testing import consistency

    T = 10**5

    def keygenEncryptDecrypt(b):
        """bootstrappable keygen-encrypt-decrypt (bit = {0})"""
        sk, pk_z, pk_y = keygen()
        c, cy = encrypt(pk_z, pk_y, b)
        return decrypt(sk, c, cy)

    consistency(keygenEncryptDecrypt, (0,), 0, T)
    consistency(keygenEncryptDecrypt, (1,), 1, T)

    def keygenEncryptSum(b1, b2):
        """bootstrappable keygen-encrypt-sum ({0}+{1})"""
        sk, pk_z, pk_y = keygen()
        c1, cy1 = encrypt(pk_z, pk_y, b1)
        c2, cy2 = encrypt(pk_z, pk_y, b2)
        s = c1 + c2
        sy = post_process(s, pk_y)
        return decrypt(sk, s, sy)

    consistency(keygenEncryptSum, (0,0), 0, T)
    consistency(keygenEncryptSum, (0,1), 1, T)
    consistency(keygenEncryptSum, (1,1), 0, T)

    def keygenEncryptMult(b1, b2):
        """bootstrappable keygen-encrypt-mult ({0}*{1})"""
        sk, pk_z, pk_y = keygen()
        c1, cy1 = encrypt(pk_z, pk_y, b1)
        c2, cy2 = encrypt(pk_z, pk_y, b2)
        m = c1 * c2
        my = post_process(m, pk_y)
        return decrypt(sk, m, my)

    consistency(keygenEncryptMult, (0,0), 0, T)
    consistency(keygenEncryptMult, (0,1), 0, T)
    consistency(keygenEncryptMult, (1,1), 1, T)
