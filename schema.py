import graphene

# Tipe data User
class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()

# Simulasi database sederhana
mock_users = [
    {"id": "1", "name": "Budi", "email": "budi@mail.com"},
    {"id": "2", "name": "Ani", "email": "ani@mail.com"},
]

# Query utama
class Query(graphene.ObjectType):
    user = graphene.Field(User, id=graphene.ID(required=True))
    users = graphene.List(User)

    def resolve_user(root, info, id):
        return next((user for user in mock_users if user["id"] == id), None)

    def resolve_users(root, info):
        return mock_users

# Mutation untuk menambahkan user
class CreateUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(lambda: User)

    def mutate(self, info, name, email):
        new_user = {"id": str(len(mock_users) + 1), "name": name, "email": email}
        mock_users.append(new_user)
        return CreateUser(user=new_user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

# Schema lengkap
schema = graphene.Schema(query=Query, mutation=Mutation)
