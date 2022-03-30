from Crypto.PublicKey import RSA
from collections import OrderedDict
from hashlib import sha256
import json

keypair = RSA.generate(bits=1024)

n = keypair.n
d = keypair.d
e = keypair.e
print("d is :", d)
print("n is :", n)
print("e is :", e)

signable_data = 27111378

signature = pow(signable_data, d, n)
print("signature is :",signature)

unsigned_data = pow(signature, e, n)
print("unsigned data is: ",unsigned_data)

print(signable_data == unsigned_data)

data1 = {
    'hello' : "world"
}
data2 = OrderedDict()
data2['hello'] = "world"

print(sha256(json.dumps(data1).encode()).hexdigest())
print(sha256(json.dumps(data2).encode()).hexdigest())

# def unsign_transaction_signature(signature:str, pubkey_as_keypair: str) -> str:
#     """
#     recieves a transactions hashed signable data and unsign signature
#     including:
#         incoins,
#         outcoins,
#         signature

#     returns a string wich is equal to unsigned data
#     """
#     print("public key as keypair is :", pubkey_as_keypair)
#     e, n = pubkey_as_keypair.split(",")
#     signature = int(signature)
#     n = int(n)
#     e = int(e)
#     unsign = pow(signature, e, n)
#     print("unsigned value is : ",unsign)
#     return unsign

# print(unsign_transaction_signature(str(signature), f"{e},{n}"))