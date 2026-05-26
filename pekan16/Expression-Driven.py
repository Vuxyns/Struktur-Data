from typing import List, Optional
from collections import deque


class ExprHeapSorter:
    def __init__(self, expr_str: str):
        self.expr = expr_str.replace(" ", "")
        self.values = []

    def parse_and_evaluate(self) -> List[int]:
        """
        Membangun pohon ekspresi, mengevaluasi,
        dan mengembalikan list nilai integer.
        """
        tokens = deque(self.expr)

        if not tokens:
            raise ValueError("Ekspresi kosong")

        root = self._build_tree(tokens)
        self.values = self._eval_tree(root)

        return self.values

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        """
        Implementasi rekursif expression tree.

        Format ekspresi:
        (operand operator operand)

        Contoh:
        ((3+5)*(8-2))

        Node disimpan dalam bentuk:
        {
            'val': value/operator,
            'left': left_node,
            'right': right_node
        }
        """

        if not tokens:
            raise ValueError("Token tidak lengkap")

        token = tokens.popleft()

        # Jika token '(' → bangun subtree
        if token == '(':
            left_subtree = self._build_tree(tokens)

            if not tokens:
                raise ValueError("Operator tidak ditemukan")

            operator = tokens.popleft()

            if operator not in ['+', '-', '*', '/']:
                raise ValueError(f"Operator tidak valid: {operator}")

            right_subtree = self._build_tree(tokens)

            if not tokens or tokens.popleft() != ')':
                raise ValueError("Kurung tutup ')' tidak ditemukan")

            return {
                'val': operator,
                'left': left_subtree,
                'right': right_subtree
            }

        # Operand angka
        elif token.isdigit():
            return {
                'val': int(token),
                'left': None,
                'right': None
            }

        else:
            raise ValueError(f"Token tidak valid: {token}")

    def _eval_tree(self, node: Optional[dict]) -> List[int]:
        """
        Evaluasi expression tree secara postorder.

        Mengembalikan list semua hasil subtree.
        """

        results = []

        def postorder(curr: Optional[dict]) -> int:
            if curr is None:
                return 0

            # Leaf / operand
            if curr['left'] is None and curr['right'] is None:
                value = curr['val']
                results.append(value)
                return value

            left_val = postorder(curr['left'])
            right_val = postorder(curr['right'])

            op = curr['val']

            if op == '+':
                value = left_val + right_val

            elif op == '-':
                value = left_val - right_val

            elif op == '*':
                value = left_val * right_val

            elif op == '/':
                if right_val == 0:
                    raise ValueError("Division by zero")

                value = left_val // right_val

            else:
                raise ValueError(f"Operator tidak dikenal: {op}")

            results.append(value)
            return value

        postorder(node)
        return results

    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        """
        Mengurutkan array ascending menggunakan
        in-place heapsort.
        """

        n = len(arr)

        if n <= 1:
            return arr

        # =========================
        # 1. Build Max Heap
        # =========================
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(arr, n, i)

        # =========================
        # 2. Extract Maximum
        # =========================
        for end in range(n - 1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]
            self._sift_down(arr, end, 0)

        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        """
        Menjaga properti max-heap.

        left  = 2*i + 1
        right = 2*i + 2
        """

        while True:
            largest = idx

            left = 2 * idx + 1
            right = 2 * idx + 2

            # Bandingkan child kiri
            if left < heap_size and arr[left] > arr[largest]:
                largest = left

            # Bandingkan child kanan
            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            # Jika sudah sesuai heap
            if largest == idx:
                break

            # Swap
            arr[idx], arr[largest] = arr[largest], arr[idx]

            # Lanjut sift-down
            idx = largest

    def is_complete_tree(self, arr: List[int]) -> bool:
        """
        Memvalidasi apakah representasi array
        memenuhi properti complete binary tree.
        """

        n = len(arr)

        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2

            # Jika anak kanan ada tapi kiri tidak ada
            if right < n and left >= n:
                return False

            # Semua indeks sebelum n harus valid
            if left >= n and right >= n:
                continue

        return True


# =====================================
# Contoh Penggunaan
# =====================================
if __name__ == "__main__":

    # Expression fully-parenthesized
    expr = "((3+5)*((8-2)+(4/2)))"

    sorter = ExprHeapSorter(expr)

    try:
        # Parse & evaluate
        values = sorter.parse_and_evaluate()

        print("Hasil evaluasi postorder:")
        print(values)

        # Heapsort inplace
        sorter.heapsort_inplace(values)

        print("\nArray setelah heapsort ascending:")
        print(values)

        # Validasi complete tree
        print("\nApakah complete binary tree?")
        print(sorter.is_complete_tree(values))

    except ValueError as e:
        print("Error:", e)