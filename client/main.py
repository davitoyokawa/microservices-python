from dataclasses import dataclass
from flask import Flask, abort, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import UniqueConstraint
import requests
from producer import publish

app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@db/main"
CORS(app)  

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(128))
    image = db.Column(db.String(128))


@dataclass
class User(db.Model):
    id: int
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(128))
    product_id = db.Column(db.String(128))

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

@app.route("/api/products")  # Retorna todos os produtos
def index():
    products = Product.query.all()
    return jsonify(products)

@app.route("/api/products/<int:id>/like", methods=['POST'])  
def like(id):
    # Verificar se o produto existe
    product = Product.query.get(id)
    if not product:
        abort(404, f"Product with id {id} does not exist.")

    req = requests.get("http://host.docker.internal:8000/api/user", verify=False)
    json = req.json()

    try:
        productUser = User(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id)
    except Exception as e:
        db.session.rollback()
        abort(400, f'You already liked this product. Error: {e}')

    return render_template('like_success.html', product_id=id, user_id=json['id']), 200


@app.route("/api/products/<int:id>/ratings", methods=['GET'])
def get_product_ratings(id):
    try:
        response = requests.get(f"http://host.docker.internal:8000/api/products/{id}/ratings", verify=False)

        # Verificar se a requisição foi bem-sucedida
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            abort(response.status_code, f"Error fetching ratings: {response.text}")
    
    except requests.RequestException as e:
        abort(500, f"An error occurred while connecting to the ratings service: {e}")


@app.route("/api/products/<int:id>/rate", methods=['POST'])
def rate_product(id):
    req = requests.get("http://host.docker.internal:8000/api/user", verify=False)
    json = req.json()

    rating_value = request.json.get('rating')
    if not (1 <= rating_value <= 5):
        abort(400, 'Rating must be between 1 and 5')

    product = Product.query.get_or_404(id)

    try:
        productUser = User(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_rated', {
            "id": id,
            "rating": rating_value
        })
    except Exception as e:
        db.session.rollback()
        abort(400, f"An error occurred: {e}")

    return jsonify({
        'message': 'Rating added successfully',
        'product_id': id,
        'user_id': json['id'],
    })

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, host="0.0.0.0", port=5000)