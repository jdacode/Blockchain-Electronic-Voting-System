#blockchain_6 and upwards

import hashlib as hl
import json

# __all__ = ['hash_string_256', 'hash_block']

def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    '''  hashlib.sha256(value) where value is a string, so we cannot pass the block value directly, because it's a dictionary
         json.dumps converts the dictionary type to string because the sha256 function only works with strings
         .encode converts to utf-8 format which is the string format
         hashlib.sha256(value) generate a bytehash, to convert to a normal string, we use .hexdigest() function for that
    '''

    # the reason of copy is because for not overwrite the previous reference of dictionary of block
    # It's mean we need a new copy of a new dictionary every time we hash a new block
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())