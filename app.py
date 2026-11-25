from datetime import datetime
from flask import Flask, jsonify, render_template, request
from mars_library import (
    Bahan, Cabang, DatabaseBackup, Layanan, LayananAnak, LayananRepaint, Pelanggan, Pesanan
)

app = Flask(__name__)
db = DatabaseBackup()

DAFTAR_LAYANAN = {
    "Kids & Woman": LayananAnak("Kids & Woman", 48, 25000, {"Sabun pembersih": 20, "Pewangi": 5}),
    "Fast Clean": Layanan("Fast Clean", 24, 25000, {"Sabun pembersih": 20, "Pewangi": 5}),
    "Deep Clean": Layanan("Deep Clean", 48, 35000, {"Sabun pembersih": 40, "Pewangi": 5}),
    "Rewhitening": Layanan("Rewhitening", 72, 35000, {"Sabun pembersih": 20, "Pewangi": 5, "Cairan pemutih": 30}),
    "Unyellowing": Layanan("Unyellowing", 96, 50000, {"Sabun pembersih": 20, "Pewangi": 5, "Penghilang kuning": 30}),
    "Reglue": Layanan("Reglue", 96, 60000, {"Sabun pembersih": 20, "Lem sepatu": 25}),
    "Repaint": LayananRepaint("Repaint", 168, 100000, 130000, {"Sabun pembersih": 20, "Cat sepatu": 30}),
    "Express": Layanan("Express", 24, 50000, {"Sabun pembersih": 20, "Pewangi": 5}),
}

DAFTAR_CABANG = {
    "Jogokaryan": Cabang("Jogokaryan", "Jl. Jogokaryan, Mantrijeron, Yogyakarta"),
    "Gondokusuman": Cabang("Gondokusuman", "Jl. Gondokusuman, Yogyakarta"),
    "Kotagede": Cabang("Kotagede", "Jl. Kemasan, Kotagede, Yogyakarta"),
}

def isi_stok_awal(cabang):
    cabang.tambah_bahan(Bahan("B01", "Sabun pembersih", "ml", 1000, 200, 100))
    cabang.tambah_bahan(Bahan("B02", "Pewangi", "ml", 300, 50, 150))
    cabang.tambah_bahan(Bahan("B03", "Cairan pemutih", "ml", 400, 80, 120))
    cabang.tambah_bahan(Bahan("B04", "Penghilang kuning", "ml", 400, 80, 130))
    cabang.tambah_bahan(Bahan("B05", "Lem sepatu", "ml", 350, 75, 200))
    cabang.tambah_bahan(Bahan("B06", "Cat sepatu", "ml", 400, 100, 300))

for c in DAFTAR_CABANG.values():
    isi_stok_awal(c)

t0 = datetime(2026, 10, 19, 9, 0)
budi = Pelanggan("P01", "Budi", "081234567890")
sari = Pelanggan("P02", "Sari", "081398765432")

for p_awal in [
    Pesanan("T001", budi, DAFTAR_LAYANAN["Fast Clean"], 2, waktu_masuk=t0,
            kategori_sepatu="Sepatu Lari", nama_sepatu="Sepatu Lari Harian",
            bagian_kotor="Midsole & upper mesh berdebu", metode_antar="Gratis Antar-Jemput",
            alamat_jemput="Jl. Kemasan No. 14, Kotagede"),
    Pesanan("T002", sari, DAFTAR_LAYANAN["Deep Clean"], 1, waktu_masuk=t0,
            kategori_sepatu="Sepatu Dewasa / Sneakers", nama_sepatu="Sneakers Kasual",
            bagian_kotor="Toe-box suede & tali sepatu", metode_antar="Drop-off di Cabang", alamat_jemput="-"),
    Pesanan("T003", budi, DAFTAR_LAYANAN["Repaint"], 1, jumlah_warna=2, waktu_masuk=t0,
            kategori_sepatu="Sepatu Kulit / Suede", nama_sepatu="Sneakers Suede Klasik",
            bagian_kotor="Warna pudar & midsole menguning", metode_antar="Gratis Antar-Jemput",
            alamat_jemput="Jl. Mondorakan, Kotagede"),
    Pesanan("T004", sari, DAFTAR_LAYANAN["Kids & Woman"], 1, waktu_masuk=t0,
            kategori_sepatu="Sepatu Anak", nama_sepatu="Sepatu Sekolah Anak (Size 28)",
            bagian_kotor="Insole & outsole berlumpur", metode_antar="Gratis Antar-Jemput",
            alamat_jemput="Prenggan, Kotagede"),
]:
    DAFTAR_CABANG["Kotagede"].terima_pesanan(p_awal)

db.simpan_backup(DAFTAR_CABANG)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def api_status():
    ringkasan = {}
    for nama, c in DAFTAR_CABANG.items():
        ringkasan[nama] = {
            "pendapatan": c.hitung_pendapatan(),
            "biaya_bahan": c.hitung_biaya_bahan(),
            "laba_kotor": c.hitung_laba_kotor(),
            "perlu_restok": c.bahan_perlu_restok(),
            "persediaan": [b.to_dict() for b in c.persediaan.values()],
            "pesanan": [p.to_dict() for p in c.pesanan],
        }
    return jsonify(ringkasan)

@app.route("/api/pesanan", methods=["POST"])
def api_tambah_pesanan():
    data = request.json
    try:
        cabang = DAFTAR_CABANG[data["cabang"]]
        layanan = DAFTAR_LAYANAN[data["layanan"]]
        jumlah_pasang = int(data.get("jumlah_pasang", 1))
        jumlah_warna = int(data.get("jumlah_warna", 1))

        if isinstance(layanan, LayananAnak):
            ukuran = int(data.get("ukuran_sepatu", 30))
            untuk_anak = bool(data.get("untuk_anak", True))
            layanan.validasi_ukuran(ukuran, untuk_anak)

        nomor_baru = f"T{sum(len(c.pesanan) for c in DAFTAR_CABANG.values()) + 1:03d}"
        pelanggan = Pelanggan(f"P-{nomor_baru}", data["nama"], data["no_telp"])
        pesanan = Pesanan(
            nomor_baru, pelanggan, layanan, jumlah_pasang, jumlah_warna,
            kategori_sepatu=data.get("kategori_sepatu", "Sepatu Dewasa / Sneakers"),
            nama_sepatu=data.get("nama_sepatu", "-"),
            bagian_kotor=data.get("bagian_kotor", "-"),
            metode_antar=data.get("metode_antar", "Gratis Antar-Jemput"),
            alamat_jemput=data.get("alamat_jemput", "-"),
        )
        cabang.terima_pesanan(pesanan)
        db.simpan_backup(DAFTAR_CABANG)
        return jsonify({"sukses": True, "pesanan": pesanan.to_dict()})
    except ValueError as err:
        return jsonify({"sukses": False, "pesan": str(err)}), 400

@app.route("/api/pesanan/status", methods=["POST"])
def api_ubah_status():
    data = request.json
    try:
        cabang = DAFTAR_CABANG[data["cabang"]]
        target = next((p for p in cabang.pesanan if p.no == data["no_pesanan"]), None)
        if not target:
            return jsonify({"sukses": False, "pesan": "Nomor pesanan tidak ditemukan."}), 404
        target.ubah_status(data["status_baru"])
        db.simpan_backup(DAFTAR_CABANG)
        return jsonify({"sukses": True, "status": target.status})
    except ValueError as err:
        return jsonify({"sukses": False, "pesan": str(err)}), 400

@app.route("/api/bahan/restok", methods=["POST"])
def api_restok_bahan():
    data = request.json
    try:
        cabang = DAFTAR_CABANG[data["cabang"]]
        bahan = cabang.persediaan.get(data["nama_bahan"])
        if not bahan:
            return jsonify({"sukses": False, "pesan": "Bahan tidak ditemukan."}), 404
        bahan.tambah_stok(float(data.get("jumlah", 500)))
        db.simpan_backup(DAFTAR_CABANG)
        return jsonify({"sukses": True, "stok_baru": bahan.stok})
    except ValueError as err:
        return jsonify({"sukses": False, "pesan": str(err)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
