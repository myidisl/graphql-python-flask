import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import UserModel
from db import SessionLocal

# Tipe data User
class User(SQLAlchemyObjectType):
    class Meta():
        model = UserModel

# Simulasi database sederhana
#mock_users = [
#    {"id": "1", "name": "Budi", "email": "budi@mail.com"},
#    {"id": "2", "name": "Ani", "email": "ani@mail.com"},
#]

# Query utama
class Query(graphene.ObjectType):
    users = graphene.List(User)
    user = graphene.Field(User, id=graphene.Int(required=True))

    def resolve_user(root, info, id):
        db = SessionLocal()
        return db.query(UserModel).filter(UserModel.id == id).first()
        #return next((user for user in mock_users if user["id"] == id), None)

    def resolve_users(root, info):
        db = SessionLocal()
        return db.query(UserModel).all()
        #return mock_users

# Mutation untuk menambahkan user
class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(lambda: User)

    def mutate(self, info, name, email):
        db = SessionLocal()
        new_user = UserModel(name=name, email=email)
        db.add(new_user)
        db.commit()
        return CreateUser(user=new_user)
        #new_user = {"id": str(len(mock_users) + 1), "name": name, "email": email}
        #mock_users.append(new_user)
        #return CreateUser(user=new_user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

# Schema lengkap
schema = graphene.Schema(query=Query, mutation=Mutation)
