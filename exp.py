import ecdsa
import gmpy
from ecdsa import SECP256k1
import hashlib

m1="I want the flag"
m2="I hate the flag"

ks = 70072565845091379839538401416782237438929290760763328213667318793346806056450
r=23372277234339732161528747619365498567249265222314495344099167639942101343337

sk = ecdsa.SigningKey.generate(curve=SECP256k1)

n = sk.curve.order

h1=hashlib.sha256(m1.encode("utf-8"))
hs=h1.digest()
z1 = ecdsa.util.string_to_number(h1.digest())%n
h2=hashlib.sha256(m2.encode("utf-8"))
z2 = ecdsa.util.string_to_number(h2.digest())%n

x=-((z1+z2)* gmpy.invert(2*r, n)) %n

sk1 = sk.from_secret_exponent(x,sk.curve)

vk1=sk1.get_verifying_key()
print('pubkey:',vk1.to_string().hex())

sig=sk1.sign(m1.encode('utf-8'),k=ks,hashfunc=hashlib.sha256)
print('sign:',sig.hex())