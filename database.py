import csv
import json
import os
from datetime import datetime


class DatabaseBackup:
    """Mengelola penyimpanan basis data dan auto-backup CSV/JSON."""

    def __init__(self, folder="data_backup"):
        self.__folder = folder
        os.makedirs(self.__folder, exist_ok=True)
        self.__json_path = os.path.join(self.__folder, "data_mars_laundry.json")
        self.__csv_path = os.path.join(self.__folder, "backup_transaksi.csv")

    def simpan_backup(self, daftar_cabang):
        snapshot = {
            "terakhir_diperbarui": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cabang": {},
        }

        baris_csv = []
        for nama_cabang, cabang in daftar_cabang.items():
            snapshot["cabang"][nama_cabang] = {
                "alamat": cabang.alamat,
                "pendapatan": cabang.hitung_pendapatan(),
                "biaya_bahan": cabang.hitung_biaya_bahan(),
                "laba_kotor": cabang.hitung_laba_kotor(),
                "perlu_restok": cabang.bahan_perlu_restok(),
                "persediaan": {k: v.to_dict() for k, v in cabang.persediaan.items()},
                "pesanan": [p.to_dict() for p in cabang.pesanan],
            }
            for p in cabang.pesanan:
                d = p.to_dict()
                d["cabang"] = nama_cabang
                baris_csv.append(d)

        with open(self.__json_path, "w", encoding="utf-8") as f_json:
            json.dump(snapshot, f_json, indent=2, ensure_ascii=False)

        if baris_csv:
            kolom = [
                "no_pesanan",
                "cabang",
                "pelanggan",
                "no_telp",
                "layanan",
                "kategori_sepatu",
                "nama_sepatu",
                "bagian_kotor",
                "metode_antar",
                "alamat_jemput",
                "jumlah_pasang",
                "jumlah_warna",
                "total_biaya",
                "waktu_masuk",
                "estimasi_selesai",
                "status",
            ]
            with open(self.__csv_path, "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.DictWriter(f_csv, fieldnames=kolom)
                writer.writeheader()
                writer.writerows(baris_csv)

        return self.__json_path, self.__csv_path
