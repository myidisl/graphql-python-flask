import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import UserModel
from db import SessionLocal
from auth import generate_token,get_current_user,generate_refresh_token,decode_refresh_token

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
        current_user =  get_current_user()
        print(current_user)
        if not current_user:
            raise Exception("Unauthorized!")
        db = SessionLocal()
        return db.query(UserModel).filter(UserModel.id == id).first()
        #return next((user for user in mock_users if user["id"] == id), None)

    def resolve_users(root, info):
        current_user = get_current_user()
        print(current_user)
     #   if not current_user:
     #       raise Exception("Unauthorized!")
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

class LoginUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    token = graphene.String()
    refresh_token = graphene.String()

    def mutate(self, info, email):
        db = SessionLocal()
        user =  db.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            raise Exception("User not Found!")
        
        token = generate_token(user)
        refresh_token = generate_refresh_token(user)

        user.refresh_token = refresh_token
        db.commit()

        return LoginUser(token=token, refresh_token=refresh_token)

class RefreshToken(graphene.Mutation):
    class Arguments:
        refresh_token = graphene.String(required=True)
    
    token = graphene.String()

    def mutate(self, info, refresh_token):
        try:
            payload = decode_refresh_token(refresh_token)
            user_id = payload["sub"]
        except:
            raise Exception("Invalid Refresh Token")
    
        db = SessionLocal()
        user =  db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user or user.refresh_token != refresh_token:
            raise Exception("Invalid user or refresh token")
        
        new_token = generate_token(user)
        return RefreshToken(token=new_token)

class LogoutUser(graphene.Mutation):
    ok = graphene.Boolean()

    def mutate(self,info):
        user = get_current_user()
        if not user:
            raise Exception("Unauthorized")
        
        db = SessionLocal()
        user.refresh_token = None
        db.commit()

        return LogoutUser(ok=True)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    refresh_token = RefreshToken.Field()
    logout_user = LogoutUser.Field()

# Schema lengkap
schema = graphene.Schema(query=Query, mutation=Mutation)
