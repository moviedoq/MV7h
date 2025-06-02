from flask import Flask
from app.routes import register_routes
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
