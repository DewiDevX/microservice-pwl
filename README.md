# Microservice Testing dengan Pytest

## Deskripsi Proyek
Proyek ini merupakan microservice sederhana yang dibangun dengan **FastAPI** dan menggunakan **SQLAlchemy** sebagai ORM. Microservice ini menyediakan endpoint untuk operasi CRUD pada item, autentikasi (register/login), dan otorisasi berbasis peran (RBAC) dengan dua jenis pengguna: `user` dan `admin`.

## Fitur
- Register dan login pengguna (JWT)
- Operasi CRUD item (hanya untuk pengguna yang login)
- Role-Based Access Control:
  - Admin dapat melihat semua user dan mengelola item siapa pun
  - User biasa hanya dapat mengelola item miliknya sendiri
- Pengujian otomatis menggunakan **pytest** (15 test case)

## Cara Menjalankan Aplikasi
1. Clone repository ini:
   ```bash
   git clone https://github.com/DewiDevX/microservice-pwl.git
   cd microservice-pwl
