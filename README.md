# REST API Spasial - Praktikum 7 SIG

Repositori ini berisi implementasi REST API *backend* untuk mengelola dan melayani lalu lintas data spasial fasilitas publik. Proyek ini dibangun menggunakan **FastAPI**, **PostgreSQL/PostGIS**, dan **asyncpg**, sebagai bentuk pemenuhan Latihan dan Tugas Praktikum 7 mata kuliah Sistem Informasi Geografis (SIG) Institut Teknologi Sumatera.

**Oleh:** Anselmus Herpin Hasugian (123140020)

---

## Pemenuhan Kriteria Tugas & Latihan
Proyek ini mengintegrasikan langkah-langkah implementasi (Latihan) sekaligus memenuhi seluruh kriteria evaluasi (Tugas Praktikum):

- [x] **Implementasi Minimal 5 Endpoint:** Operasi CRUD dan ekstraksi data (`GET all`, `GET by ID`, `GET GeoJSON`, `GET Nearby`, `POST`).
- [x] **Validasi Pydantic:** Penggunaan skema *type hinting* ketat untuk memastikan integritas input koordinat dan data teks sebelum masuk ke basis data.
- [x] **Output Standar GeoJSON:** Konversi objek spasial (*FeatureCollection* & *Feature*) secara langsung di level *database* menggunakan `jsonb_build_object` dan `ST_AsGeoJSON`.
- [x] **Query Analisis Spasial:** Implementasi pencarian radius lokasi terdekat (*Buffer/Nearby*) menggunakan fungsi tata ruang PostGIS `ST_DWithin`.
- [x] **Arsitektur Asinkronus:** Menerapkan *Connection Pool* dengan `asyncpg` untuk performa *non-blocking I/O* yang optimal.

---

## Teknologi yang Digunakan
* **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
* **Server ASGI:** Uvicorn
* **Database Driver:** Asyncpg
* **Sistem Basis Data:** PostgreSQL dengan ekstensi spasial PostGIS
* **Validasi Data:** Pydantic

---

## Daftar Endpoint API

| Method | Endpoint | Deskripsi |
| :--- | :--- | :--- |
| `GET` | `/api/fasilitas` | Mengambil seluruh titik koordinat fasilitas publik. |
| `GET` | `/api/fasilitas/{id}` | Mengambil detail satu fasilitas berdasarkan ID spesifik. |
| `GET` | `/api/geojson/fasilitas` | Mengekstrak seluruh data fasilitas dalam format standar **GeoJSON** (siap untuk *frontend mapping*). |
| `GET` | `/api/spasial/nearby` | Melakukan query spasial untuk mencari fasilitas dalam radius tertentu (`lon`, `lat`, `radius`). |
| `POST` | `/api/fasilitas` | Menambahkan data titik fasilitas baru ke dalam PostGIS. |

---

## Persiapan Menjalankan Program (Local Setup)

Ikuti langkah-langkah berikut untuk menjalankan API ini di mesin lokal:

### 1. Kloning Repositori
```bash
git clone <URL_GITHUB_ANDA>
cd praktikum7_api
```
### 2. Inisialisasi Virtual Environment & Dependensi
Sangat disarankan untuk mengisolasi instalasi pustaka menggunakan virtual environment.

```bash
# Membuat environment
python -m venv .venv

# Aktivasi (Windows)
.venv\Scripts\activate

# Instalasi library yang dibutuhkan
pip install -r requirements.txt
```
### 3. Konfigurasi Basis Data
1. Pastikan PostgreSQL dan ekstensi PostGIS telah berjalan di komputer Anda.
2. Buat tabel fasilitas_publik dengan kolom geometri (SRID: 4326).
3. Salin template variabel lingkungan:

```bash
cp .env.example .env
```
Buka file .env dan sesuaikan nilainya (User, Password, Port, DB Name) dengan konfigurasi PostgreSQL lokal Anda.

### 4. Menjalankan Server
Jalankan server aplikasi menggunakan Uvicorn dengan mode live-reload:

```bash
uvicorn main:app --reload
```

Dokumentasi & Pengujian (Swagger UI)

FastAPI secara otomatis menghasilkan antarmuka dokumentasi interaktif. Setelah server berjalan, Anda dapat melakukan pengujian (testing) terhadap seluruh endpoint tanpa memerlukan aplikasi pihak ketiga seperti Postman.

Buka tautan berikut di peramban web Anda:
http://127.0.0.1:8000/docs