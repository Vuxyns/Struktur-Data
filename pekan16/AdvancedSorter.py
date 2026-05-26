from typing import List, Optional
import math


class ListNode:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def __repr__(self):
        return str(self.data)


class AdvancedSorter:
    def __init__(self):
        pass

    # =========================================================
    # 1. ARRAY MERGE SORT
    # (Virtual Sublists + Single tmpArray)
    # =========================================================
    def sort_array(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr

        # Hanya SATU temporary array
        tmp_array = [0] * len(arr)

        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)
        return arr

    def _rec_merge_sort(self, arr, first, last, tmp_array):
        if first >= last:
            return

        mid = (first + last) // 2

        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)

        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr, left_start, mid, right_end, tmp_array):
        """
        Menggabungkan dua virtual sublists:
        - kiri  = arr[left_start ... mid]
        - kanan = arr[mid+1 ... right_end]

        Stable merge:
        Jika sama, elemen kiri dipilih lebih dulu.
        """

        left = left_start
        right = mid + 1
        index = left_start

        # Merge ke tmp_array
        while left <= mid and right <= right_end:
            # <= menjaga STABILITAS
            if arr[left] <= arr[right]:
                tmp_array[index] = arr[left]
                left += 1
            else:
                tmp_array[index] = arr[right]
                right += 1

            index += 1

        # Sisa elemen kiri
        while left <= mid:
            tmp_array[index] = arr[left]
            left += 1
            index += 1

        # Sisa elemen kanan
        while right <= right_end:
            tmp_array[index] = arr[right]
            right += 1
            index += 1

        # Copy balik ke array asli
        i = left_start
        while i <= right_end:
            arr[i] = tmp_array[i]
            i += 1

    # =========================================================
    # 2. LINKED LIST MERGE SORT
    # (Fast-Slow + Dummy Merge)
    # =========================================================
    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head

        # Split linked list
        right_head = self._split_linked_list(head)
        left_head = head

        # Recursive sort
        left_sorted = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)

        # Merge hasil sorting
        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head: ListNode) -> Optional[ListNode]:
        """
        Split linked list menjadi dua bagian menggunakan:
        - midPoint bergerak 1 langkah
        - curNode bergerak 2 langkah
        """

        midPoint = head
        curNode = head.next

        while curNode and curNode.next:
            midPoint = midPoint.next
            curNode = curNode.next.next

        # Head bagian kanan
        right_head = midPoint.next

        # Putus link
        midPoint.next = None

        return right_head

    def _merge_linked_lists(
        self,
        listA: Optional[ListNode],
        listB: Optional[ListNode]
    ) -> Optional[ListNode]:
        """
        Merge dua linked list terurut.

        Menggunakan:
        - dummy node
        - tail reference

        STABLE:
        Jika data sama, node dari listA dipilih lebih dulu.
        """

        dummy = ListNode(0)
        tail = dummy

        while listA and listB:
            # <= menjaga stabilitas
            if listA.data <= listB.data:
                tail.next = listA
                listA = listA.next
            else:
                tail.next = listB
                listB = listB.next

            tail = tail.next

        # Sambungkan sisa node
        tail.next = listA if listA else listB

        return dummy.next

    # =========================================================
    # 3. QUICK SORT PARTITION
    # (Median-of-Three Pivot)
    # =========================================================
    def partition_quick(self, arr: List[int], first: int, last: int) -> int:
        """
        Partition Quick Sort dengan:
        - median-of-three pivot selection
        - in-place partition

        Catatan:
        Quick Sort in-place secara alami TIDAK STABLE,
        karena elemen dapat saling bertukar posisi.
        """

        mid = (first + last) // 2

        # Urutkan first, mid, last
        if arr[first] > arr[mid]:
            arr[first], arr[mid] = arr[mid], arr[first]

        if arr[first] > arr[last]:
            arr[first], arr[last] = arr[last], arr[first]

        if arr[mid] > arr[last]:
            arr[mid], arr[last] = arr[last], arr[mid]

        # Median dipindah ke first sebagai pivot
        arr[first], arr[mid] = arr[mid], arr[first]

        pivot = arr[first]

        low = first + 1
        high = last

        while True:
            while low <= high and arr[low] <= pivot:
                low += 1

            while low <= high and arr[high] > pivot:
                high -= 1

            if low > high:
                break

            arr[low], arr[high] = arr[high], arr[low]

        # Letakkan pivot di posisi final
        arr[first], arr[high] = arr[high], arr[first]

        return high

    # =========================================================
    # 4. QUICK SORT DENGAN DEPTH LIMITER
    # =========================================================
    def quick_sort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr

        max_depth = 2 * math.log2(len(arr))

        self._quick_sort_recursive(arr, 0, len(arr) - 1, 0, max_depth)
        return arr

    def _quick_sort_recursive(
        self,
        arr,
        first,
        last,
        depth,
        max_depth
    ):
        if first >= last:
            return

        # Fallback ke Merge Sort jika depth terlalu dalam
        if depth > max_depth:
            tmp_array = [0] * len(arr)
            self._rec_merge_sort(arr, first, last, tmp_array)
            return

        pivot_index = self.partition_quick(arr, first, last)

        self._quick_sort_recursive(
            arr,
            first,
            pivot_index - 1,
            depth + 1,
            max_depth
        )

        self._quick_sort_recursive(
            arr,
            pivot_index + 1,
            last,
            depth + 1,
            max_depth
        )


# =========================================================
# HELPER FUNCTIONS
# =========================================================
def build_linked_list(values):
    if not values:
        return None

    head = ListNode(values[0])
    current = head

    i = 1
    while i < len(values):
        current.next = ListNode(values[i])
        current = current.next
        i += 1

    return head


def print_linked_list(head):
    current = head

    while current:
        print(current.data, end=" -> ")
        current = current.next

    print("None")


# =========================================================
# TESTING
# =========================================================
if __name__ == "__main__":
    sorter = AdvancedSorter()

    # -------------------------------
    # TEST ARRAY MERGE SORT
    # -------------------------------
    arr1 = [38, 27, 43, 3, 9, 82, 10]

    print("Array sebelum Merge Sort:")
    print(arr1)

    sorter.sort_array(arr1)

    print("Array sesudah Merge Sort:")
    print(arr1)

    # -------------------------------
    # TEST QUICK SORT
    # -------------------------------
    arr2 = [50, 20, 60, 10, 40, 30, 70]

    print("\nArray sebelum Quick Sort:")
    print(arr2)

    sorter.quick_sort(arr2)

    print("Array sesudah Quick Sort:")
    print(arr2)

    # -------------------------------
    # TEST LINKED LIST MERGE SORT
    # -------------------------------
    linked_values = [7, 2, 9, 1, 5, 3]

    head = build_linked_list(linked_values)

    print("\nLinked List sebelum sorting:")
    print_linked_list(head)

    sorted_head = sorter.sort_linked_list(head)

    print("Linked List sesudah sorting:")
    print_linked_list(sorted_head)