---
title: "Dokumentasi Teknis Sistem Informasi Inventaris Barang"
subtitle: "SIIB — Sistem Informasi Inventaris Barang"
author: "[Nama Mahasiswa] — [NIM]"
date: "29 Oktober 2026"
lang: id
---

# 1. Identitas Dokumen dan Riwayat Perubahan

## 1.1 Identitas Dokumen

| Atribut | Keterangan |
|:--|:----------------------|
| Judul dokumen | Dokumentasi Teknis Sistem Informasi Inventaris Barang (SIIB) |
| Kode dokumen | SIIB-DOK-001 |
| Versi | 1.0 |
| Status | Final untuk dikumpulkan |
| Tanggal | 29 Oktober 2026 |
| Penyusun | [Nama Mahasiswa], NIM [NIM] |
| Mata kuliah | [Nama Mata Kuliah] |
| Dosen pengampu | [Nama Dosen] |
| Repositori | [Isi tautan GitHub jika proyek diunggah; belum ada untuk dokumen ini] |

## 1.2 Riwayat Perubahan

| Versi | Tanggal | Penyusun | Perubahan |
|:--|:--|:--|:----------------|
| 0.1 | 22 Okt 2026 | [Nama] | Kerangka dokumen dan deskripsi sistem |
| 0.2 | 25 Okt 2026 | [Nama] | Penambahan kebutuhan fungsional/nonfungsional dan diagram |
| 0.3 | 27 Okt 2026 | [Nama] | Dokumentasi modul Barang Keluar dan kasus uji |
| 1.0 | 29 Okt 2026 | [Nama] | Petunjuk instalasi, referensi, dan finalisasi |

## 1.3 Daftar Istilah

| Istilah | Arti |
|:--|:----------------------|
| SKU / kode barang | Kode unik pengenal setiap barang |
| Stok minimum | Batas jumlah stok; di bawah atau sama dengan batas ini sistem memberi peringatan |
| Transaksi masuk / keluar | Pencatatan penambahan / pengurangan stok barang |
| RBAC | *Role-Based Access Control*, pembatasan akses berdasarkan peran |

# 2. Deskripsi Sistem dan Ruang Lingkup

## 2.1 Latar Belakang

Pencatatan barang secara manual (buku atau lembar kerja terpisah) rawan salah hitung, sulit ditelusuri, dan lambat saat membuat laporan. SIIB dirancang sebagai aplikasi web untuk mencatat data barang, transaksi masuk dan keluar, serta stok secara terpusat dan akurat.

## 2.2 Tujuan

1. Menyediakan data stok yang akurat dan selalu terbarui.
2. Mencatat seluruh pergerakan barang agar dapat ditelusuri.
3. Memberi peringatan dini ketika stok mencapai batas minimum.
4. Mempercepat pembuatan laporan stok dan transaksi.

## 2.3 Pengguna Sistem

| Peran | Tanggung jawab |
|:--|:----------------------|
| Admin | Mengelola pengguna, barang, kategori, dan pemasok; melihat stok dan laporan |
| Staf Gudang | Mencatat barang masuk dan keluar; melihat stok |
| Pimpinan | Melihat stok dan mencetak laporan |

## 2.4 Ruang Lingkup

**Termasuk dalam lingkup:** autentikasi dan otorisasi berbasis peran; pengelolaan data barang, kategori, dan pemasok; pencatatan barang masuk dan keluar dengan pembaruan stok otomatis; peringatan stok minimum; laporan stok dan transaksi (ekspor PDF).

**Di luar lingkup:** pembelian dan penagihan (*procurement*/akuntansi), pemindaian barcode/RFID, integrasi dengan sistem keuangan, aplikasi seluler asli, dan manajemen banyak gudang.

## 2.5 Asumsi dan Batasan

- Sistem dipakai di satu gudang dengan sekitar 10–50 pengguna.
- Pengguna mengakses melalui peramban modern dalam jaringan lokal atau internet.
- Setiap barang dihitung dalam satu satuan (pcs, box, kg, dan sebagainya).

## 2.6 Arsitektur dan Teknologi

Aplikasi berarsitektur tiga lapis (presentasi, logika bisnis, data) dengan pola MVC.

| Lapisan | Teknologi |
|:--|:----------------------|
| Bahasa / kerangka kerja | PHP 8.2 dan Laravel 11 |
| Basis data | MySQL 8.0 (atau MariaDB 10.6+) |
| Antarmuka | Blade, Bootstrap 5 |
| Server web | Apache 2.4 atau Nginx |
| Pustaka laporan | barryvdh/laravel-dompdf |
| Pengujian | PHPUnit 11 |

# 3. Kebutuhan Fungsional

| ID | Kebutuhan | Prioritas | Peran |
|:--|:----------------------|:--|:--|
| FR-01 | Sistem memungkinkan pengguna login dan logout dengan email dan kata sandi, serta membatasi menu sesuai peran. | Tinggi | Semua |
| FR-02 | Sistem memungkinkan admin menambah, mengubah, menghapus, dan mencari data barang beserta kategorinya. | Tinggi | Admin |
| FR-03 | Sistem memungkinkan admin mengelola data pemasok. | Sedang | Admin |
| FR-04 | Sistem memungkinkan staf mencatat barang masuk (barang, pemasok, jumlah, tanggal) dan menambah stok otomatis. | Tinggi | Staf |
| FR-05 | Sistem memungkinkan staf mencatat barang keluar (barang, jumlah, tanggal, tujuan), mengurangi stok otomatis, dan menolak transaksi jika jumlah melebihi stok. | Tinggi | Staf |
| FR-06 | Sistem menampilkan daftar stok terkini dan menandai barang yang stoknya sama dengan atau di bawah stok minimum. | Tinggi | Semua |
| FR-07 | Sistem menghasilkan laporan stok dan laporan transaksi per periode dalam format PDF. | Sedang | Pimpinan, Admin |
| FR-08 | Sistem memungkinkan admin mengelola akun pengguna dan perannya. | Sedang | Admin |

# 4. Kebutuhan Nonfungsional

| ID | Kategori | Kebutuhan | Cara verifikasi |
|:--|:--|:----------------------|:------------|
| NFR-01 | Keamanan | Kata sandi disimpan sebagai hash bcrypt; semua formulir dilindungi token CSRF; akses fitur diperiksa di sisi server berdasarkan peran. | Inspeksi basis data; uji akses lintas peran |
| NFR-02 | Kinerja | Halaman daftar barang (hingga 10.000 baris) tampil kurang dari 2 detik pada koneksi lokal, dengan paginasi. | Pengukuran waktu respons |
| NFR-03 | Integritas data | Perubahan stok dan pencatatan transaksi berlangsung dalam satu transaksi basis data (atomik); stok tidak boleh negatif. | Uji kasus TC-06, TC-07 |
| NFR-04 | Kegunaan | Antarmuka responsif (layar 360 px ke atas) dan pesan kesalahan berbahasa Indonesia yang jelas. | Uji coba manual |
| NFR-05 | Ketersediaan | Sistem tersedia minimal 99% pada jam kerja; cadangan basis data harian. | Pemantauan; jadwal *backup* |
| NFR-06 | Keterpeliharaan | Kode mengikuti PSR-12 dan struktur MVC Laravel; cakupan uji otomatis modul inti minimal 70%. | Laporan PHPUnit |

# 5. Diagram

## 5.1 Diagram *Use Case*

![Diagram use case SIIB](diagram/usecase.png){ width=100% }

Tiga aktor berinteraksi dengan sembilan *use case*. Notifikasi stok minimum merupakan perluasan (*extend*) dari fungsi Lihat Stok Barang.

## 5.2 Diagram Relasi Entitas (ERD)

![Diagram relasi entitas SIIB](diagram/erd.png){ width=100% }

Enam tabel saling berelasi satu-ke-banyak. Setiap transaksi mencatat barang, pengguna pencatat, dan (untuk transaksi masuk) pemasok.

## 5.3 *Flowchart* Proses Barang Keluar

![Flowchart proses barang keluar](diagram/flow.png){ height=15cm }

Alur ini menjadi dasar modul yang didokumentasikan pada Bagian 6.

# 6. Dokumentasi Modul Utama: Barang Keluar

## 6.1 Deskripsi

Modul Barang Keluar mencatat pengurangan stok akibat pemakaian, penjualan, atau distribusi. Modul ini memenuhi FR-05 dan NFR-03. Pengguna yang berhak: Staf Gudang.

## 6.2 Komponen

| Komponen | Berkas | Fungsi |
|:--|:----------------|:----------------------|
| Rute | `routes/web.php` | `GET /barang-keluar`, `GET /barang-keluar/create`, `POST /barang-keluar` |
| Kontroler | `app/Http/Controllers/OutgoingController.php` | Menerima permintaan, memvalidasi, memanggil layanan |
| Layanan | `app/Services/StockService.php` | Logika pengurangan stok atomik |
| Model | `app/Models/Item.php`, `OutgoingTransaction.php` | Akses data |
| Tampilan | `resources/views/outgoing/*.blade.php` | Daftar dan formulir |

## 6.3 Aturan Validasi

| Kolom | Aturan |
|:--|:----------------------|
| `item_id` | Wajib, harus ada di tabel `items` |
| `jumlah` | Wajib, bilangan bulat, minimal 1, tidak melebihi stok saat ini |
| `tanggal` | Wajib, format tanggal, tidak melewati hari ini |
| `tujuan` | Wajib, maksimal 150 karakter |

## 6.4 Kode Inti

```php
// app/Services/StockService.php
public function keluar(int $itemId, int $jumlah, string $tanggal,
                       string $tujuan, int $userId): OutgoingTransaction
{
    return DB::transaction(function () use ($itemId, $jumlah, $tanggal, $tujuan, $userId) {
        $item = Item::lockForUpdate()->findOrFail($itemId); // cegah balapan data

        if ($jumlah > $item->stok) {
            throw new InsufficientStockException(
                "Stok {$item->nama_barang} tidak cukup (tersedia {$item->stok})."
            );
        }

        $trx = OutgoingTransaction::create([
            'item_id' => $itemId, 'user_id' => $userId,
            'jumlah'  => $jumlah, 'tanggal' => $tanggal, 'tujuan' => $tujuan,
        ]);

        $item->decrement('stok', $jumlah);
        return $trx;
    });
}
```

## 6.5 Spesifikasi Antarmuka

| Item | Nilai |
|:--|:----------------------|
| Endpoint | `POST /barang-keluar` |
| Masukan | `item_id`, `jumlah`, `tanggal`, `tujuan`, `_token` |
| Keluaran sukses | Redirect ke daftar dengan pesan "Transaksi berhasil dicatat"; bila stok ≤ stok minimum, tampil peringatan stok menipis |
| Keluaran gagal | Kembali ke formulir dengan pesan kesalahan validasi atau "Stok tidak cukup" |
| Hak akses | Peran `staf` |

# 7. Kasus Pengujian

| ID | Skenario | Data masukan | Hasil yang diharapkan | Kebutuhan |
|:--|:------------|:----------------|:----------------|:--|
| TC-01 | Login valid | Email dan sandi benar (staf) | Masuk ke dasbor sesuai peran | FR-01 |
| TC-02 | Login gagal | Sandi salah | Ditolak, pesan "Email atau kata sandi salah" | FR-01 |
| TC-03 | Tambah barang | Kode `BRG-001`, nama, kategori, stok awal 0 | Data tersimpan dan tampil di daftar | FR-02 |
| TC-04 | Kode barang ganda | Kode `BRG-001` yang sudah ada | Ditolak, pesan "Kode barang sudah digunakan" | FR-02 |
| TC-05 | Barang masuk | Item stok 10, jumlah masuk 5 | Stok menjadi 15; transaksi tercatat | FR-04 |
| TC-06 | Barang keluar valid | Item stok 15, jumlah keluar 5 | Stok menjadi 10; transaksi tercatat | FR-05 |
| TC-07 | Barang keluar melebihi stok | Item stok 10, jumlah keluar 20 | Ditolak "Stok tidak cukup"; stok tetap 10 | FR-05, NFR-03 |
| TC-08 | Peringatan stok minimum | Stok minimum 5; keluar hingga stok 5 | Transaksi sukses dan muncul peringatan stok menipis | FR-06 |
| TC-09 | Jumlah tidak valid | Jumlah 0 atau -3 | Ditolak oleh validasi | FR-05 |
| TC-10 | Pembatasan peran | Pimpinan membuka `/barang-keluar/create` | Ditolak (HTTP 403) | FR-01, NFR-01 |
| TC-11 | Laporan stok | Pimpinan memilih laporan stok | Berkas PDF terunduh, berisi seluruh barang | FR-07 |

Contoh pengujian otomatis (PHPUnit) untuk TC-07:

```php
public function test_barang_keluar_melebihi_stok_ditolak(): void
{
    $staf = User::factory()->create(['role' => 'staf']);
    $item = Item::factory()->create(['stok' => 10]);

    $this->actingAs($staf)->post('/barang-keluar', [
        'item_id' => $item->id, 'jumlah' => 20,
        'tanggal' => now()->toDateString(), 'tujuan' => 'Divisi A',
    ])->assertSessionHasErrors();

    $this->assertEquals(10, $item->fresh()->stok);
}
```

# 8. Petunjuk Instalasi dan Konfigurasi

## 8.1 Prasyarat

| Perangkat lunak | Versi minimum |
|:--|:--|
| PHP (ekstensi: mbstring, pdo_mysql, openssl, xml, ctype, fileinfo) | 8.2 |
| Composer | 2.x |
| MySQL / MariaDB | 8.0 / 10.6 |
| Node.js dan npm | 18 |
| Git | 2.x |

## 8.2 Langkah Instalasi

```bash
# 1. Unduh kode sumber
git clone <URL-REPOSITORI> siib && cd siib

# 2. Pasang dependensi
composer install
npm install && npm run build

# 3. Buat berkas konfigurasi dan kunci aplikasi
cp .env.example .env
php artisan key:generate
```

## 8.3 Konfigurasi Basis Data

Buat basis data di MySQL:

```sql
CREATE DATABASE siib CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'siib_user'@'localhost' IDENTIFIED BY 'GANTI_KATA_SANDI';
GRANT ALL PRIVILEGES ON siib.* TO 'siib_user'@'localhost';
```

Sesuaikan berkas `.env`:

```ini
APP_NAME=SIIB
APP_ENV=local
APP_URL=http://localhost:8000
APP_LOCALE=id

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=siib
DB_USERNAME=siib_user
DB_PASSWORD=GANTI_KATA_SANDI
```

## 8.4 Migrasi, Data Awal, dan Menjalankan

```bash
php artisan migrate --seed   # membuat tabel dan akun admin awal
php artisan serve            # akses di http://localhost:8000
php artisan test             # menjalankan pengujian
```

Akun awal hasil *seeder*: `admin@siib.test` dengan kata sandi sementara yang ditampilkan di `database/seeders/UserSeeder.php`. **Ganti kata sandi segera setelah login pertama.**

## 8.5 Catatan Produksi

- Atur `APP_ENV=production` dan `APP_DEBUG=false`.
- Arahkan *document root* web server ke folder `public/`.
- Jalankan `php artisan config:cache && php artisan route:cache`.
- Aktifkan HTTPS dan jadwalkan cadangan harian dengan `mysqldump`.

## 8.6 Pemecahan Masalah Umum

| Gejala | Penyebab / solusi |
|:--|:----------------------|
| `SQLSTATE[HY000] [1045] Access denied` | Periksa `DB_USERNAME` dan `DB_PASSWORD` di `.env` |
| Halaman 500 setelah menyalin `.env` | Jalankan `php artisan key:generate` |
| Gaya tampilan tidak muncul | Jalankan `npm run build` |
| Folder `storage` tidak dapat ditulis | `chmod -R 775 storage bootstrap/cache` |

# 9. Daftar Referensi dan Standar Acuan

## 9.1 Standar

1. ISO/IEC/IEEE 29148:2018. *Systems and software engineering — Life cycle processes — Requirements engineering.* (acuan penulisan kebutuhan)
2. ISO/IEC/IEEE 26514:2022. *Systems and software engineering — Design and development of information for users.* (acuan dokumentasi)
3. ISO/IEC 25010:2023. *Systems and software engineering — Product quality model.* (acuan kebutuhan nonfungsional)
4. ISO/IEC/IEEE 29119-3:2021. *Software testing — Test documentation.* (acuan kasus uji)
5. OMG. *Unified Modeling Language (UML) Specification*, versi 2.5.1, 2017. (notasi diagram)
6. PHP-FIG. *PSR-12: Extended Coding Style Guide.* <https://www.php-fig.org/psr/psr-12/>

## 9.2 Referensi Teknis

7. Laravel. *Laravel 11.x Documentation.* <https://laravel.com/docs/11.x>
8. Oracle. *MySQL 8.0 Reference Manual.* <https://dev.mysql.com/doc/refman/8.0/en/>
9. OWASP. *OWASP Top 10 — 2021.* <https://owasp.org/Top10/>
10. Bootstrap. *Bootstrap 5.3 Documentation.* <https://getbootstrap.com/docs/5.3/>

## 9.3 Pustaka Buku

11. Sommerville, I. (2016). *Software Engineering* (10th ed.). Pearson.
12. Pressman, R. S., & Maxim, B. R. (2020). *Software Engineering: A Practitioner's Approach* (9th ed.). McGraw-Hill.
