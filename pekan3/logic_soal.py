# 1. Deduplication
# Menghapus elemen duplikat dari list tetapi tetap mempertahankan urutan pertama muncul
def deduplikasi(lst):
  seen = set() # set untuk melacak elemen yang sudah muncul
  result = []

  for item in lst:
    if item not in seen:
      seen.add(item)
      result.append(item)

  return result

# 2. Intersection Dua Array
# Mengembalikan elemen yang muncul di kedua list
def intersection(list1, list2):
  set2 = set(list2)   # ubah list2 menjadi set agar pencarian lebih cepat
  result = []

  for item in list1:
    if item in set2:
      result.append(item)

  return result

# 3. Anagram Check
# Mengecek apakah dua string merupakan anagram
def is_anagram(s1, s2):
  if len(s1) != len(s2):
    return False

  count = {}

  # hitung karakter dari string pertama
  for char in s1:
    count[char] = count.get(char, 0) + 1

  # kurangi hitungan dari string kedua
  for char in s2:
    if char not in count:
      return False
    count[char] -= 1
    if count[char] < 0:
      return False

  return True

# 4. First Recurring Character
# Mencari karakter pertama yang muncul lebih dari sekali
def first_recurring_char(s):
  seen = set()

  for char in s:
    if char in seen:
      return char
    seen.add(char)

  return None

# 5. Simulasi Buku Telepon
# Program sederhana dengan menu
def phone_book():
  contacts = {}

  while True:
    print("\n=== MENU BUKU TELEPON ===")
    print("1. Tambah Kontak")
    print("2. Cari Kontak")
    print("3. Tampilkan Semua")
    print("4. Keluar")

    choice = input("Pilih menu: ")

    if choice == "1":
      name = input("Nama: ")
      number = input("Nomor: ")
      contacts[name] = number
      print("Kontak berhasil ditambahkan.")

    elif choice == "2":
      name = input("Masukkan nama: ")
      if name in contacts:
        print("Nomor:", contacts[name])
      else:
        print("Kontak tidak ditemukan.")

    elif choice == "3":
      print("\nDaftar Kontak:")
      for name, number in contacts.items():
        print(f"{name} -> {number}")

    elif choice == "4":
      print("Keluar dari program.")
      break

    else:
      print("Pilihan tidak valid.")