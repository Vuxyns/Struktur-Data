# soal 1: Modified Binary Search
def countOccurrences(sortedList, target):

    def find_left(arr, val):
        lo, hi, result = 0, len(arr) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == val:
                result = mid
                hi = mid - 1
            elif arr[mid] < val:
                lo = mid + 1
            else:
                hi = mid - 1
        return result

    def find_right(arr, val):
        lo, hi, result = 0, len(arr) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] == val:
                result = mid
                lo = mid + 1
            elif arr[mid] < val:
                lo = mid + 1
            else:
                hi = mid - 1
        return result

    left = find_left(sortedList, target)
    if left == -1:
        return 0

    right = find_right(sortedList, target)
    return right - left + 1

# soal 2: Bubble Sort
def bubbleSort(arr):

    data = arr[:]
    n = len(data)

    comparisons = 0
    swaps = 0
    passes = 0

    for i in range(n - 1):
        swapped = False

        for j in range(n - 1 - i):
            comparisons += 1

            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swaps += 1
                swapped = True

        passes += 1

        if not swapped:
            break

    return data, comparisons, swaps, passes

# soal 3: Hybrid Sort
def insertionSort(arr):

    data = arr[:]
    comparisons = swaps = 0

    for i in range(1, len(data)):
        key = data[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if data[j] > key:
                data[j + 1] = data[j]
                swaps += 1
                j -= 1
            else:
                break

        data[j + 1] = key

    return data, comparisons, swaps


def selectionSort(arr):

    data = arr[:]
    n = len(data)

    comparisons = swaps = 0

    for i in range(n):

        min_idx = i

        for j in range(i + 1, n):
            comparisons += 1

            if data[j] < data[min_idx]:
                min_idx = j

        if min_idx != i:
            data[i], data[min_idx] = data[min_idx], data[i]
            swaps += 1

    return data, comparisons, swaps


def hybridSort(theSeq, threshold=10):

    if len(theSeq) <= threshold:
        return insertionSort(theSeq)

    else:
        return selectionSort(theSeq)

# soal 4: Merge Three Sorted Lists
def mergeThreeSortedLists(A, B, C):

    result = []

    i = j = k = 0
    a, b, c = len(A), len(B), len(C)

    while i < a and j < b and k < c:

        if A[i] <= B[j] and A[i] <= C[k]:
            result.append(A[i])
            i += 1

        elif B[j] <= A[i] and B[j] <= C[k]:
            result.append(B[j])
            j += 1

        else:
            result.append(C[k])
            k += 1

    while i < a and j < b:
        if A[i] <= B[j]:
            result.append(A[i])
            i += 1
        else:
            result.append(B[j])
            j += 1

    while i < a and k < c:
        if A[i] <= C[k]:
            result.append(A[i])
            i += 1
        else:
            result.append(C[k])
            k += 1

    while j < b and k < c:
        if B[j] <= C[k]:
            result.append(B[j])
            j += 1
        else:
            result.append(C[k])
            k += 1

    result.extend(A[i:])
    result.extend(B[j:])
    result.extend(C[k:])

    return result

# soal 5: Inversion Counter
def countInversionsNaive(arr):

    count = 0

    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):

            if arr[i] > arr[j]:
                count += 1

    return count


def countInversionsSmart(arr):

    def merge_count(arr):

        if len(arr) <= 1:
            return arr, 0

        mid = len(arr) // 2

        left, inv_left = merge_count(arr[:mid])
        right, inv_right = merge_count(arr[mid:])

        merged = []
        inversions = inv_left + inv_right

        i = j = 0

        while i < len(left) and j < len(right):

            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                inversions += len(left) - i
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])

        return merged, inversions

    _, total = merge_count(arr)

    return total