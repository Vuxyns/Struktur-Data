import random
import time

from logic import *

SEP = "=" * 60

# ============================================================
# SOAL 1
# ============================================================

print(SEP)
print("SOAL 1 — Modified Binary Search")
print(SEP)

arr = [1,2,4,4,4,4,7,9,12]

print(countOccurrences(arr,4))
print(countOccurrences(arr,5))
print(countOccurrences(arr,1))
print(countOccurrences(arr,12))


# ============================================================
# SOAL 2
# ============================================================

print("\n",SEP)
print("SOAL 2 — Bubble Sort")
print(SEP)

data = [5,1,4,2,8]

result = bubbleSort(data)

print("Sorted:",result[0])
print("Comparisons:",result[1])
print("Swaps:",result[2])
print("Pass:",result[3])


# ============================================================
# SOAL 3
# ============================================================

print("\n",SEP)
print("SOAL 3 — Hybrid Sort")
print(SEP)

sizes=[50,100,500]

print("Size | Hybrid | Insertion | Selection")

for n in sizes:

    arr=[random.randint(0,1000) for _ in range(n)]

    _,hc,hs=hybridSort(arr)
    _,ic,is_=insertionSort(arr)
    _,sc,ss=selectionSort(arr)

    print(n,hc+hs,ic+is_,sc+ss)


# ============================================================
# SOAL 4
# ============================================================

print("\n",SEP)
print("SOAL 4 — Merge Three Lists")
print(SEP)

A=[1,5,9]
B=[2,6,10]
C=[3,4,7]

print(mergeThreeSortedLists(A,B,C))


# ============================================================
# SOAL 5
# ============================================================

print("\n",SEP)
print("SOAL 5 — Inversion Counter")
print(SEP)

for size in [1000,5000,10000]:

    arr=[random.randint(0,size) for _ in range(size)]

    start=time.time()
    countInversionsNaive(arr)
    t1=time.time()-start

    start=time.time()
    countInversionsSmart(arr)
    t2=time.time()-start

    print(size,"Naive:",round(t1,4),"Smart:",round(t2,4))