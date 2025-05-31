# GraphQL dengan Python (Flask + Graphene)

Proyek sederhana untuk belajar GraphQL menggunakan Python dan Flask.

## 🔧 Setup
```bash
git clone https://github.com/myidisl/graphql-python-flask.git
cd graphql-python-flask
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

## Tahap 2: GraphQL + SQLite

- Menggunakan SQLAlchemy untuk persistensi data.
- Struktur data: file `data.db`
- Menyediakan query dan mutation: createUser, users, user(id)

## 🔐 Auth (JWT)

### Mutation: Login
```graphql
mutation {
  loginUser(email: "rina@mail.com") {
    token
  }
}

## 🔐 Autentikasi: Access Token & Refresh Token

### ✨ Login
```graphql
mutation {
  loginUser(email: "rina@mail.com") {
    token
    refreshToken
  }
}

## 📦 Migrasi Skema Database

Untuk menambahkan kolom `refresh_token`:

1. Buat revisi migrasi:
   ```bash
   alembic revision --autogenerate -m "Tambah kolom refresh_token"

alembic upgrade head

# Tahap 5 – Role-Based Access Control (RBAC)

## Tujuan
Menerapkan RBAC pada GraphQL API dengan role-based decorator.

## Perubahan:
- Tambah kolom `role` di model `User`
- Tambah decorator `require_role`
- Proteksi query `secretData`
- Middleware JWT parsing → inject `user` ke `context`

## Testing:
- Login sebagai admin → akses berhasil
- Login sebagai user biasa → akses ditolak

## Commit history:
- `feat(models): add role column to User model with default value 'user'`
- `chore(migration): add alembic revision for adding role column`
- `feat(auth): implement require_role decorator for RBAC`
- `feat(schema): protect secretData query using RBAC`
- `feat(api): inject authenticated user into context for RBAC`
