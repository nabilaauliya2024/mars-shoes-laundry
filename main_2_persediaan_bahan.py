"""
MAIN PROGRAM 2: Pengelolaan Persediaan Bahan Habis Pakai Cabang (Enkapsulasi & Peringatan Restok)
"""
from mars_library import Bahan, Cabang, Layanan, Pelanggan, Pesanan

def main():
    print("=== MAIN 2: PENGELOLAAN PERSEDIAAN BAHAN & RESTOK CABANG ===")
    jogokaryan = Cabang("Jogokaryan", "Jl. Jogokaryan, Mantrijeron, Yogyakarta")
    jogokaryan.tambah_bahan(Bahan("B01", "Sabun pembersih", "ml", 120, 100, 100))
    jogokaryan.tambah_bahan(Bahan("B02", "Pewangi", "ml", 60, 50, 150))

    deep = Layanan("Deep Clean", 48, 35000, {"Sabun pembersih": 40, "Pewangi": 5})
    sari = Pelanggan("P02", "Sari", "081398765432")

    p1 = Pesanan("T101", sari, deep, 2)
    jogokaryan.terima_pesanan(p1)
    print("Sisa Sabun:", jogokaryan.persediaan["Sabun pembersih"].stok, "ml")
    print("Daftar Bahan Perlu Restok:", jogokaryan.bahan_perlu_restok())

    # Admin melakukan restok bahan
    jogokaryan.persediaan["Sabun pembersih"].tambah_stok(500)
    print("Setelah Restok +500ml, Sisa Sabun:", jogokaryan.persediaan["Sabun pembersih"].stok, "ml")

if __name__ == "__main__":
    main()
