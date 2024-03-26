#!/usr/bin/env python3

### Required modules
from locale import CODESET
import string
import sys
from operator import itemgetter

##################################################################################
### Function definitions
##################################################################################

# Evaluates the likelihood of a byte string being readable English text by comparing
# against the frequency of English letters and spaces.
# Parameters: byte_str - The byte string to evaluate
# Returns: A numerical score indicating the likelihood of the string being English
def evaluate_english_likelihood(byte_str):

	english_char_frequencies = {
		'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06749, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
	}

	return sum([english_char_frequencies.get(chr(b), 0) for b in byte_str.lower()])

# Attempts to decrypt a hex-encoded string by XORing it with potential single-byte keys.
# Parameters: hex_str - The hex-encoded string to decrypt
# Returns: A list of tuples containing decrypted strings and their scores
def decrypt_hex(hex_str):

	test_keys = ["AA","BB","CC"]

	scores = []
	for key in test_keys:
		decrypted_bytes = b''

		for b in hex_str:
			decrypted_bytes += bytes([int(b)^ord(key)])
			
		score = evaluate_english_likelihood(decrypted_bytes)
		scores.append((decrypted_bytes, score))

	sorted_scores = sorted(scores, key=itemgetter(1), reverse=True)
	return sorted_scores

# Displays decrypted strings with the highest likelihood of being English, in descending order.
# Parameters: decrypted_list - A list of decrypted strings and their scores
def display_decrypted_strings(decrypted_list):

	for decrypted, _ in decrypted_list[:5]:
		print(decrypted.decode("latin1"))



##################################
###    EXAMPLE CODE  ############################
######################
from os import urandom

def generate_key(length):
    """Generates a random key."""
    return urandom(2)

def xor_bytes(s, t):
    """Performs XOR operation on two byte strings."""
    if isinstance(s, str):
        return b"".join(chr(ord(a) ^ ord(b)) for a, b in zip(s, t))
    else:
        return bytes(a ^ b for a, b in zip(s, t))

secret_message = 'This is a secret message'
print('Message:', secret_message)

encryption_key = generate_key(len(secret_message))
print('Key:', encryption_key)

encrypted_message = xor_bytes(secret_message.encode('utf8'), encryption_key)
print('Encrypted:', encrypted_message)
print('Decrypted:', xor_bytes(encrypted_message, encryption_key).decode('utf8'))

# Verification
if xor_bytes(encrypted_message, encryption_key).decode('utf8') == secret_message:
    print('Unit test passed')
else:
    print('Unit test failed')

##################################################################################
### Main function
##################################################################################

# Main function for decrypting a hex-encoded string via brute-force.
# Usage: ./xorBruteForce.py <hex-encoded string>
def main():

	input_hex = str(sys.argv[1])
	hex_bytes = bytes.fromhex(input_hex)

	decrypted_data = decrypt_hex(hex_bytes)
	display_decrypted_strings(decrypted_data)

if __name__ == '__main__':
	main()
