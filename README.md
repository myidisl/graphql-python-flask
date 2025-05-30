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