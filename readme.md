# sign2win

题目给了一个ECDSA的签名与验证的服务，观察最后获取flag的要求，需要提供一个签名，可以使用两个不同的消息来验证它并通过，这里其实是ECDSA的一个特性，可以寻找到一个私钥来满足对不同消息的重复的签名

假设我们需要签名的消息为m1和m2，则它们的摘要分别为h1=H(m1)，h2=H(m2)，然后我们选择一个随机数k来计算签名中的r，因为要生成相同的签名那也就是r和s都相同，首先r相同那就表示签名所选择的随机数k是相同的，这样我们就有

> (x1,y1) = k*G
>
> r = x1 mod n

这样利用r,h1,h2我们就可以计算对h1的签名在h2也能验证通过的私钥了

> pri = -(h1+h2)/(2*r) mod n

下面我们不妨简单验证下，用pk签名我们可以得到s

> s = k^-1(h+pri*r) mod n

验证签名要求下面的等式成立

> r = h\*s^-1\*G+r\*s^-1*pub mod n
>
> r = h\*s^-1\*G+r\*s^-1\*pri\*G mod n
>
> r = s^-1\*G\*(h+r\*pri) mod n

从前面对pri的计算我们可以得到

> r*pri = -(h1+h2)/2 mod n

这样假设我们签名的消息是h1时，前面的等式就如下

> r = s^-1\*G\*(h1-(h1+h2)/2) mod n
>
> r = G\*(h2-h1)/2s mod n

同样的将pri代入s，即有

> s = (h2-h1)/2k mod n

代回前面的等式，就能得到

> r = G*k mod n

等式成立，同理可得签名的消息为h2时等式依然成立

exp如下

```python
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
```

