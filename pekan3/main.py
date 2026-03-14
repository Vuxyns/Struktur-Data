from logic_soal import deduplikasi, intersection, is_anagram, first_recurring_char, phone_book

while True:
  print("\n=== MENU PROGRAM ===")
  print("1. Deduplication List")
  print("2. Intersection Dua Array")
  print("3. Cek Anagram")
  print("4. First Recurring Character")
  print("5. Simulasi Buku Telepon")
  print("6. Keluar")

  pilihan = input("Pilih menu: ")

  # 1 Deduplication
  if pilihan == "1":
    data = input("Masukkan angka dipisah spasi: ")
    lst = list(map(int, data.split()))
    print("Hasil:", deduplikasi(lst))

  # 2 Intersection
  elif pilihan == "2":
    data1 = input("Masukkan list pertama (pisah spasi): ")
    data2 = input("Masukkan list kedua (pisah spasi): ")

    list1 = list(map(int, data1.split()))
    list2 = list(map(int, data2.split()))

    print("Intersection:", intersection(list1, list2))

  # 3 Anagram
  elif pilihan == "3":
    s1 = input("String pertama: ")
    s2 = input("String kedua: ")

    if is_anagram(s1, s2):
      print("Termasuk Anagram")
    else:
      print("Bukan Anagram")

  # 4 First Recurring Character
  elif pilihan == "4":
    s = input("Masukkan string: ")
    result = first_recurring_char(s)

    if result:
      print("Karakter pertama yang berulang:", result)
    else:
      print("Tidak ada karakter berulang")

  # 5 Phone Book
  elif pilihan == "5":
    phone_book()

  # Keluar
  elif pilihan == "6":
    print("Program selesai.")
    break

  else:
    print("Pilihan tidak valid.")