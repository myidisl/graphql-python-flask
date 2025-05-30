from flask import Flask
from flask_graphql import GraphQLView
from schema import schema
from db import init_db

app = Flask(__name__)
init_db() #inisiasi tabel database

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql',schema=schema,graphiql=True)
)

if __name__ == '__main__':
    app.run(debug=True)
