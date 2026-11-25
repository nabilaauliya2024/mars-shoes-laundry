"""
MAIN PROGRAM 3: Perhitungan Estimasi Waktu Selesai & Alur Status Pesanan Berurutan
"""
from datetime import datetime
from mars_library import Layanan, Pelanggan, Pesanan

def main():
    print("=== MAIN 3: ESTIMASI WAKTU SELESAI & STATUS PESANAN BERURUTAN ===")
    rewhitening = Layanan("Rewhitening", 72, 35000, {"Sabun pembersih": 20})
    pelanggan = Pelanggan("P03", "Nabila", "081299887766")
    waktu_masuk = datetime(2026, 10, 19, 10, 30)

    pesanan = Pesanan("T201", pelanggan, rewhitening, 1, waktu_masuk=waktu_masuk)
    print("Waktu Masuk     :", waktu_masuk.strftime("%d-%m-%Y %H:%M"))
    print("Estimasi Selesai:", pesanan.estimasi_selesai().strftime("%d-%m-%Y %H:%M"))
    print("Status Awal     :", pesanan.status)

    pesanan.ubah_status("Diproses")
    print("Status Berikut  :", pesanan.status)

    try:
        pesanan.ubah_status("Diambil")  # Melompati status Selesai
    except ValueError as err:
        print("Validasi Urutan Status Berhasil Menolak:", err)

if __name__ == "__main__":
    main()
