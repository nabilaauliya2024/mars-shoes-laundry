"""
MAIN PROGRAM 1: Pencatatan Pesanan, Polimorfisme Tarif, dan Validasi Aturan Layanan
"""
from datetime import datetime
from mars_library import Bahan, Cabang, Layanan, LayananAnak, LayananRepaint, Pelanggan, Pesanan

def main():
    print("=== MAIN 1: PENCATATAN PESANAN & VALIDASI ATURAN MARS SHOES LAUNDRY ===")
    kotagede = Cabang("Kotagede", "Jl. Kemasan, Kotagede, Yogyakarta")
    kotagede.tambah_bahan(Bahan("B01", "Sabun pembersih", "ml", 1000, 200, 100))
    kotagede.tambah_bahan(Bahan("B02", "Pewangi", "ml", 300, 50, 150))
    kotagede.tambah_bahan(Bahan("B06", "Cat sepatu", "ml", 400, 100, 300))

    fast = Layanan("Fast Clean", 24, 25000, {"Sabun pembersih": 20, "Pewangi": 5})
    repaint = LayananRepaint("Repaint", 168, 100000, 130000, {"Sabun pembersih": 20, "Cat sepatu": 30})
    anak = LayananAnak("Kids & Woman", 48, 25000, {"Sabun pembersih": 20, "Pewangi": 5})

    budi = Pelanggan("P01", "Budi", "081234567890")
    t0 = datetime(2026, 10, 19, 9, 0)

    # Uji Polimorfisme hitung_harga()
    p1 = Pesanan("T001", budi, fast, 2, waktu_masuk=t0)
    p2 = Pesanan("T002", budi, repaint, 1, jumlah_warna=2, waktu_masuk=t0)
    kotagede.terima_pesanan(p1)
    kotagede.terima_pesanan(p2)

    print(f"Pesanan {p1.no} ({p1.layanan.nama}): Rp {p1.hitung_total():,.0f}")
    print(f"Pesanan {p2.no} ({p2.layanan.nama} 2 warna): Rp {p2.hitung_total():,.0f}")

    # Uji Validasi Ukuran Sepatu Anak (Maksimal 30)
    try:
        anak.validasi_ukuran(32, untuk_anak=True)
    except ValueError as err:
        print("Validasi Kids & Woman Berhasil Menolak:", err)

if __name__ == "__main__":
    main()
