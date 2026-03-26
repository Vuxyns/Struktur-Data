'''
SOAL 1:
(a) BigInteger Linked List
(b) BigInteger Python List
'''

# (a) linked list version
class Node:
    def __init__(self, digit):
        self.digit = digit
        self.next = None

class BigIntegerLL:
    def __init__(self, value="0"):
        self.head = None
        self._build(value)

    def _build(self, value):
        #Bangun linked list (LSB di depan)
        value = value.strip().lstrip('0') or '0'

        for ch in value:
            new_node = Node(int(ch))
            new_node.next = self.head
            self.head = new_node

    def toString(self):
        #Konversi ke string
        cur = self.head
        res = []

        while cur:
            res.append(str(cur.digit))
            cur = cur.next

        return ''.join(reversed(res))

    def _to_int(self):
        return int(self.toString())

    def arithmetic(self, other, op):
        #Operasi aritmatika
        a, b = self._to_int(), other._to_int()

        if op == '+': return BigIntegerLL(str(a + b))
        if op == '-': return BigIntegerLL(str(a - b))
        if op == '*': return BigIntegerLL(str(a * b))
        if op == '//': return BigIntegerLL(str(a // b))
        if op == '%': return BigIntegerLL(str(a % b))
        if op == '**': return BigIntegerLL(str(a ** b))

        raise ValueError("Operator tidak valid")

    def comparable(self, other, op):
        #Perbandingan
        a, b = self._to_int(), other._to_int()

        if op == '<': return a < b
        if op == '>': return a > b
        if op == '==': return a == b
        if op == '<=': return a <= b
        if op == '>=': return a >= b
        if op == '!=': return a != b

        raise ValueError("Operator tidak valid")


# (b) list version
class BigIntegerList:
    def __init__(self, value="0"):
        self.digits = []
        self._build(value)

    def _build(self, value):
        #Simpan digit dalam list (LSB di index 0)
        value = value.strip().lstrip('0') or '0'
        self.digits = [int(x) for x in value[::-1]]

    def toString(self):
        return ''.join(map(str, self.digits[::-1]))

    def _to_int(self):
        return int(self.toString())

    def arithmetic(self, other, op):
        #Operasi aritmatika
        a, b = self._to_int(), other._to_int()

        ops = {
            '+': a + b,
            '-': a - b,
            '*': a * b,
            '//': a // b,
            '%': a % b,
            '**': a ** b
        }

        if op not in ops:
            raise ValueError("Operator tidak valid")

        return BigIntegerList(str(ops[op]))

    def comparable(self, other, op):
        #Perbandingan
        a, b = self._to_int(), other._to_int()

        if op == '<': return a < b
        if op == '>': return a > b
        if op == '==': return a == b
        if op == '<=': return a <= b
        if op == '>=': return a >= b
        if op == '!=': return a != b

        raise ValueError("Operator tidak valid")


# case
if __name__ == "__main__":
    print("=== SOAL 1 ===")

    a = BigIntegerLL("12345")
    b = BigIntegerLL("5")

    print("LinkedList A:", a.toString())
    print("LinkedList B:", b.toString())
    print("A + B =", a.arithmetic(b, '+').toString())

    x = BigIntegerList("999")
    y = BigIntegerList("1")

    print("\nList X:", x.toString())
    print("List Y:", y.toString())
    print("X + Y =", x.arithmetic(y, '+').toString())