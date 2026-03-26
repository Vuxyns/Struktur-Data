'''
SOAL 2:
Tambahan assignment operators (+=, -=, dll)
'''

class BigInteger:
    def __init__(self, value="0"):
        self.digits = []
        self._build(value)

    def _build(self, value):
        value = value.strip().lstrip('0') or '0'
        self.digits = [int(x) for x in value[::-1]]

    def toString(self):
        return ''.join(map(str, self.digits[::-1]))

    def _to_int(self):
        return int(self.toString())

    def _update(self, value):
        #Update nilai object
        self._build(str(value))

    # assignment operations
    def apply(self, other, op):
        #Semua operator assignment
        a, b = self._to_int(), other._to_int()

        if op == '+=': a = a + b
        elif op == '-=': a = a - b
        elif op == '*=': a = a * b
        elif op == '//=': a = a // b
        elif op == '%=': a = a % b
        elif op == '**=': a = a ** b
        elif op == '<<=': a = a << b
        elif op == '>>=': a = a >> b
        elif op == '|=': a = a | b
        elif op == '&=': a = a & b
        elif op == '^=': a = a ^ b
        else:
            raise ValueError("Operator tidak valid")

        self._update(a)
        return self

# case
if __name__ == "__main__":
    print("=== SOAL 2 ===")

    x = BigInteger("100")
    y = BigInteger("20")

    print("Awal:", x.toString())

    x.apply(y, '+=')
    print("+= 20 →", x.toString())

    x.apply(BigInteger("2"), '*=')
    print("*= 2 →", x.toString())

    x.apply(BigInteger("10"), '-=')
    print("-= 10 →", x.toString())

    x.apply(BigInteger("2"), '<<=')
    print("<<= 2 →", x.toString())