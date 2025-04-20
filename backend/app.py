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
    return jsonify({"message": f"order placed for user {data['user_id']}"})

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

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    new = User(email=data['email'], password=data['password'], login_type='email')
    db.session.add(new); db.session.commit()
    return jsonify({"message":"created"}), 201

from flask import Flask, request, jsonify
# … 이미 선언된 app, db, User 모델 임포트 …

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    pw    = data.get('password')
    # 1) 중복 체크
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "이미 가입된 이메일입니다"}), 400
    # 2) 새 유저 생성
    new_user = User(email=email, password=pw, login_type='email')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "회원가입 성공"}), 201

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    pw    = data.get('password')
    # 중복 체크
    if User.query.filter_by(email=email).first():
        return jsonify({"message":"이미 가입된 이메일"}), 400
    # 신규 생성
    new = User(email=email, password=pw, login_type='email')
    db.session.add(new)
    db.session.commit()
    return jsonify({"message":"회원가입 성공"}), 201



 if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Render가 할당한 포트 사용
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
