import hashlib
import json

#For hashing and converting the sha256 hash from hex to normal string
def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()


# return unique hash for a block
def hash_block(block):
    #converts block to json, encodes to utf8, then hashes with sha256
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())