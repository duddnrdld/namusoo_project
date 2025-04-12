from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, Product, Cart

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
    return "Namusoo Design API Server"

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'description': p.description,
        'image_url': p.image_url
    } for p in products])

@app.route('/cart_items', methods=['GET'])
def get_cart_items():
    user_id = request.args.get('user_id')
    cart = Cart.query.filter_by(user_id=user_id).all()
    result = []
    for item in cart:
        product = Product.query.get(item.product_id)
        result.append({
            'product_name': product.name,
            'price': product.price,
            'quantity': item.quantity
        })
    return jsonify(result)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        return jsonify({"message": "login success", "user_id": user.id})
    else:
        return jsonify({"message": "invalid credentials"}), 401

@app.route('/order', methods=['POST'])
def order():
    data = request.get_json()
    print(f"주문자: {data['user_id']}, 주소: {data['address']} {data['detail']}")
    return jsonify({"message": "order placed"})

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    new_item = Product(
        name=data['name'],
        price=data['price'],
        description=data['description'],
        image_url=data['image_url']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "상품 등록 완료"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)