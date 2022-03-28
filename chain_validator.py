import sys

sys.path.append("..")

from block_core import validate_block 

def validate_chain(chain:list = []):
    for block in range(len(chain)):
        if block == 0:
            last_block = None
        else: 
            last_block = chain[block - 1]
        block = chain[block]

        validate_block(block, last_block)