import hashlib
import json

#For hashing and converting the sha256 hash from hex to normal string
def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()


# return unique hash for a block
def hash_block(block):
    #converts block to json, encodes to utf8, then hashes with sha256
    return hash_string_256(json.dumps(block, sort_keys=True).encode())