from datetime import datetime, timedelta


class Bahan:
    """Bahan habis pakai yang disimpan di persediaan cabang."""

    def __init__(self, kode, nama, satuan, stok, stok_minimum, harga_satuan):
        self.__kode = kode
        self.__nama = nama
        self.__satuan = satuan
        self.__stok = float(stok)
        self.__stok_minimum = float(stok_minimum)
        self.__harga_satuan = float(harga_satuan)

    @property
    def kode(self):
        return self.__kode

    @property
    def nama(self):
        return self.__nama

    @property
    def satuan(self):
        return self.__satuan

    @property
    def stok(self):
        return self.__stok

    @property
    def stok_minimum(self):
        return self.__stok_minimum

    @property
    def harga_satuan(self):
        return self.__harga_satuan

    def kurangi_stok(self, jumlah):
        if jumlah > self.__stok:
            raise ValueError(
                f"Stok {self.__nama} tidak mencukupi (sisa {self.__stok} {self.__satuan})."
            )
        self.__stok -= jumlah

    def tambah_stok(self, jumlah):
        if jumlah <= 0:
            raise ValueError("Jumlah penambahan stok harus lebih dari 0.")
        self.__stok += jumlah

    def perlu_restok(self):
        return self.__stok <= self.__stok_minimum

    def to_dict(self):
        return {
            "kode": self.__kode,
            "nama": self.__nama,
            "satuan": self.__satuan,
            "stok": self.__stok,
            "stok_minimum": self.__stok_minimum,
            "harga_satuan": self.__harga_satuan,
            "perlu_restok": self.perlu_restok(),
        }


class Layanan:
    """Class induk untuk layanan dengan tarif tetap."""

    def __init__(self, nama, durasi_jam, tarif, kebutuhan_bahan):
        self.__nama = nama
        self.__durasi_jam = int(durasi_jam)
        self.__tarif = float(tarif)
        self.__kebutuhan_bahan = kebutuhan_bahan

    @property
    def nama(self):
        return self.__nama

    @property
    def durasi_jam(self):
        return self.__durasi_jam

    @property
    def tarif(self):
        return self.__tarif

    @property
    def kebutuhan_bahan(self):
        return self.__kebutuhan_bahan

    def hitung_harga(self, jumlah_pasang=1, **kwargs):
        return self.__tarif * jumlah_pasang


class LayananRepaint(Layanan):
    """Turunan Layanan: tarif bergantung pada jumlah warna (Polimorfisme)."""

    def __init__(
        self, nama, durasi_jam, tarif_satu_warna, tarif_banyak_warna, kebutuhan_bahan
    ):
        super().__init__(nama, durasi_jam, tarif_satu_warna, kebutuhan_bahan)
        self.__tarif_banyak_warna = float(tarif_banyak_warna)

    @property
    def tarif_banyak_warna(self):
        return self.__tarif_banyak_warna

    def hitung_harga(self, jumlah_pasang=1, jumlah_warna=1, **kwargs):
        if int(jumlah_warna) <= 1:
            return super().hitung_harga(jumlah_pasang)
        return self.__tarif_banyak_warna * jumlah_pasang


class LayananAnak(Layanan):
    """Turunan Layanan: Kids & Woman dibatasi maksimal ukuran 30 untuk anak."""

    UKURAN_ANAK_MAKS = 30

    def validasi_ukuran(self, ukuran, untuk_anak=True):
        if untuk_anak and int(ukuran) > self.UKURAN_ANAK_MAKS:
            raise ValueError(
                "Ukuran sepatu anak pada layanan Kids & Woman maksimal 30."
            )
        return True


class Pelanggan:
    """Data pemilik sepatu yang dilaundry."""

    def __init__(self, id_pelanggan, nama, no_telp):
        self.__id = id_pelanggan
        self.__nama = nama
        self.__no_telp = no_telp

    @property
    def id_pelanggan(self):
        return self.__id

    @property
    def nama(self):
        return self.__nama

    @property
    def no_telp(self):
        return self.__no_telp


class Pesanan:
    """Transaksi laundry yang menghubungkan pelanggan, layanan, dan cabang."""

    STATUS_URUTAN = ["Diterima", "Diproses", "Selesai", "Diambil"]

    def __init__(
        self,
        no_pesanan,
        pelanggan,
        layanan,
        jumlah_pasang=1,
        jumlah_warna=1,
        waktu_masuk=None,
        status="Diterima",
        kategori_sepatu="Sepatu Dewasa / Sneakers",
        nama_sepatu="-",
        bagian_kotor="-",
        metode_antar="Gratis Antar-Jemput",
        alamat_jemput="-",
    ):
        self.__no = no_pesanan
        self.__pelanggan = pelanggan
        self.__layanan = layanan
        self.__jumlah = int(jumlah_pasang)
        self.__jumlah_warna = int(jumlah_warna)
        self.__waktu_masuk = waktu_masuk or datetime.now()
        self.__status = status
        self.__kategori_sepatu = kategori_sepatu
        self.__nama_sepatu = nama_sepatu
        self.__bagian_kotor = bagian_kotor
        self.__metode_antar = metode_antar
        self.__alamat_jemput = alamat_jemput

    @property
    def no(self):
        return self.__no

    @property
    def pelanggan(self):
        return self.__pelanggan

    @property
    def layanan(self):
        return self.__layanan

    @property
    def jumlah(self):
        return self.__jumlah

    @property
    def jumlah_warna(self):
        return self.__jumlah_warna

    @property
    def status(self):
        return self.__status

    def hitung_total(self):
        return self.__layanan.hitung_harga(
            self.__jumlah, jumlah_warna=self.__jumlah_warna
        )

    def estimasi_selesai(self):
        return self.__waktu_masuk + timedelta(hours=self.__layanan.durasi_jam)

    def ubah_status(self, status_baru):
        if status_baru not in self.STATUS_URUTAN:
            raise ValueError(f"Status '{status_baru}' tidak dikenali.")
        idx_sekarang = self.STATUS_URUTAN.index(self.__status)
        idx_baru = self.STATUS_URUTAN.index(status_baru)
        if idx_baru != idx_sekarang + 1:
            raise ValueError(
                f"Status harus berurutan dari '{self.__status}' ke '{self.STATUS_URUTAN[idx_sekarang + 1]}'."
            )
        self.__status = status_baru

    def to_dict(self):
        return {
            "no_pesanan": self.__no,
            "pelanggan": self.__pelanggan.nama,
            "no_telp": self.__pelanggan.no_telp,
            "layanan": self.__layanan.nama,
            "kategori_sepatu": self.__kategori_sepatu,
            "nama_sepatu": self.__nama_sepatu,
            "bagian_kotor": self.__bagian_kotor,
            "metode_antar": self.__metode_antar,
            "alamat_jemput": self.__alamat_jemput,
            "jumlah_pasang": self.__jumlah,
            "jumlah_warna": self.__jumlah_warna,
            "total_biaya": self.hitung_total(),
            "waktu_masuk": self.__waktu_masuk.strftime("%d-%m-%Y %H:%M"),
            "estimasi_selesai": self.estimasi_selesai().strftime("%d-%m-%Y %H:%M"),
            "status": self.__status,
        }


class Cabang:
    """Cabang Mars Shoes Laundry (Jogokaryan, Gondokusuman, Kotagede)."""

    def __init__(self, nama, alamat):
        self.__nama = nama
        self.__alamat = alamat
        self.__persediaan = {}
        self.__pesanan = []

    @property
    def nama(self):
        return self.__nama

    @property
    def alamat(self):
        return self.__alamat

    @property
    def persediaan(self):
        return self.__persediaan

    @property
    def pesanan(self):
        return self.__pesanan

    def tambah_bahan(self, bahan):
        self.__persediaan[bahan.nama] = bahan

    def terima_pesanan(self, pesanan):
        kebutuhan = pesanan.layanan.kebutuhan_bahan
        for nama_bahan, per_pasang in kebutuhan.items():
            if nama_bahan not in self.__persediaan:
                raise ValueError(
                    f"Bahan '{nama_bahan}' belum terdaftar di cabang {self.__nama}."
                )
            if self.__persediaan[nama_bahan].stok < per_pasang * pesanan.jumlah:
                raise ValueError(
                    f"Stok {nama_bahan} di cabang {self.__nama} tidak mencukupi!"
                )

        for nama_bahan, per_pasang in kebutuhan.items():
            self.__persediaan[nama_bahan].kurangi_stok(per_pasang * pesanan.jumlah)

        self.__pesanan.append(pesanan)

    def bahan_perlu_restok(self):
        return [b.nama for b in self.__persediaan.values() if b.perlu_restok()]

    def hitung_pendapatan(self):
        return sum(p.hitung_total() for p in self.__pesanan)

    def hitung_biaya_bahan(self):
        total = 0.0
        for p in self.__pesanan:
            for nama_bahan, per_pasang in p.layanan.kebutuhan_bahan.items():
                harga = self.__persediaan[nama_bahan].harga_satuan
                total += per_pasang * p.jumlah * harga
        return total

    def hitung_laba_kotor(self):
        return self.hitung_pendapatan() - self.hitung_biaya_bahan()
