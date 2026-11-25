"""
MAIN PROGRAM 4: Laporan Keuangan Cabang (Pendapatan, Biaya Bahan, Laba Kotor) & Auto-Backup Basis Data
"""
from datetime import datetime
from mars_library import (
    Bahan, Cabang, DatabaseBackup, Layanan, LayananAnak, LayananRepaint, Pelanggan, Pesanan
)

def main():
    print("=== MAIN 4: LAPORAN KEUANGAN CABANG & AUTO-BACKUP BASIS DATA ===")
    kotagede = Cabang("Kotagede", "Jl. Kemasan, Kotagede, Yogyakarta")
    kotagede.tambah_bahan(Bahan("B01", "Sabun pembersih", "ml", 1000, 200, 100))
    kotagede.tambah_bahan(Bahan("B02", "Pewangi", "ml", 300, 50, 150))
    kotagede.tambah_bahan(Bahan("B06", "Cat sepatu", "ml", 400, 100, 300))

    fast = Layanan("Fast Clean", 24, 25000, {"Sabun pembersih": 20, "Pewangi": 5})
    deep = Layanan("Deep Clean", 48, 35000, {"Sabun pembersih": 40, "Pewangi": 5})
    repaint = LayananRepaint("Repaint", 168, 100000, 130000, {"Sabun pembersih": 20, "Cat sepatu": 30})
    anak = LayananAnak("Kids & Woman", 48, 25000, {"Sabun pembersih": 20, "Pewangi": 5})

    budi = Pelanggan("P01", "Budi", "081234567890")
    sari = Pelanggan("P02", "Sari", "081398765432")
    t0 = datetime(2026, 10, 19, 9, 0)

    for p in [
        Pesanan("T001", budi, fast, 2, waktu_masuk=t0),
        Pesanan("T002", sari, deep, 1, waktu_masuk=t0),
        Pesanan("T003", budi, repaint, 1, jumlah_warna=2, waktu_masuk=t0),
        Pesanan("T004", sari, anak, 1, waktu_masuk=t0),
    ]:
        kotagede.terima_pesanan(p)

    print(f"Pendapatan Cabang : Rp {kotagede.hitung_pendapatan():,.0f}")
    print(f"Biaya Bahan       : Rp {kotagede.hitung_biaya_bahan():,.0f}")
    print(f"Laba Kotor        : Rp {kotagede.hitung_laba_kotor():,.0f}")

    db = DatabaseBackup()
    json_path, csv_path = db.simpan_backup({"Kotagede": kotagede})
    print("Backup JSON tersimpan di:", json_path)
    print("Backup CSV tersimpan di :", csv_path)

if __name__ == "__main__":
    main()
