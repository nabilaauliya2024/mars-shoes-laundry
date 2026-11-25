CARA MENJALANKAN PROYEK WEB & 4 PROGRAM MAIN PBO - MARS SHOES LAUNDRY

A. MENJALANKAN 4 PROGRAM MAIN PBO (TERMINAL / CMD):
1. Ekstrak folder 'Mars_Shoes_Laundry_Web_Lengkap' ke Desktop.
2. Buka CMD/Terminal di dalam folder tersebut, lalu jalankan:
   - python main_1_pesanan_validasi.py   (Pencatatan pesanan, polimorfisme Repaint, validasi ukuran anak <= 30)
   - python main_2_persediaan_bahan.py   (Pengelolaan stok bahan habis pakai & peringatan restok cabang)
   - python main_3_estimasi_status.py    (Estimasi jam selesai & urutan status berurutan)
   - python main_4_laporan_backup.py     (Laporan pendapatan, biaya bahan, laba kotor & auto-backup JSON/CSV)

B. MENJALANKAN WEBSITE INTERAKTIF (FLASK):
1. Instal Flask: pip install flask
2. Jalankan: python app.py
3. Buka browser ke: http://127.0.0.1:5000
