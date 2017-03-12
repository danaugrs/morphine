# Python modules
from math import log2, floor


SECURITY_PARAMETER = 4

N = SECURITY_PARAMETER
P = SECURITY_PARAMETER**2
Q = SECURITY_PARAMETER**5


HINT_SUBSET_SIZE = floor(SECURITY_PARAMETER/log2(SECURITY_PARAMETER)) # ALPHA
HINT_SIZE = 2 * HINT_SUBSET_SIZE

PK_SIZE = 15 # This is the number of encryptions of zero in the public key

# need to tweak the following 2 parameters such that the maximum noise of an asymmetric cyphertext is <= than that of a symmetric one
PK_M_BIT_LENGTH = 3
PK_SUBSET_SIZE = 4 #5 works almost with 2 mults
# Todo: work through math (instead of finding values empirically)
# When computing asymmetric encryption we perform (PK_SUBSET_SIZE + 1) sums of elements
# whose noise is at most PK_M_BIT_LENGTH bits long.
# The upperbound on the bitlength of the noise of the sum is then (PK_M_BIT_LENGTH + PK_SUBSET_SIZE + 1)
# testUpperBound = (PK_M_BIT_LENGTH + PK_SUBSET_SIZE -2)#PK_M_BIT_LENGTH + PK_SUBSET_SIZE + 1
# print('asymmetric upperbound for noise (test)', testUpperBound) # this last value shoulb be <= to N
# print(2**N, 2**testUpperBound)

if __name__ == '__main__':
	print('N, P, Q:', N, P, Q)
	print('HINT_SUBSET_SIZE:', HINT_SUBSET_SIZE)
	print('HINT_SIZE:', HINT_SIZE)