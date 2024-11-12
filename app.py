from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import csv
from io import StringIO
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mo_atif_secret_key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game_coins.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login page when unauthorized

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    transactions = db.relationship('TransactionHistory', backref='user', lazy=True)
    coins = db.relationship('GameCoin', backref='owner', lazy=True)

# GameCoin model
class GameCoin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# TransactionHistory model
class TransactionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/import', methods=['POST'])
@login_required
def import_coins():
    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        df = pd.read_csv(file)
        for index, row in df.iterrows():
            coin = GameCoin(user_id=current_user.id, name=row['Name'], type=row['Type'], value=row['Value'],
                            quantity=row['Quantity'], description=row['Description'])
            db.session.add(coin)
        db.session.commit()
        flash('Coins imported successfully!', 'success')
    return redirect(url_for('manage_coins'))

@app.route('/export')
@login_required
def export_coins():
    coins = GameCoin.query.filter_by(user_id=current_user.id).all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Name', 'Type', 'Value', 'Quantity', 'Description'])
    for coin in coins:
        cw.writerow([coin.name, coin.type, coin.value, coin.quantity, coin.description])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=coins.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route('/coins', methods=['GET', 'POST'])
@login_required
def manage_coins():
    if request.method == 'POST':
        data = request.get_json()
        coin = GameCoin(
            user_id=current_user.id,
            name=data['name'],
            type=data['type'],
            value=data['value'],
            quantity=data['quantity'],
            description=data['description']
        )
        db.session.add(coin)
        db.session.commit()
        history = TransactionHistory(user_id=current_user.id, action=f"Added coin {coin.name}")
        db.session.add(history)
        db.session.commit()
        return jsonify({'message': 'Coin added successfully!'})

    search_query = request.args.get('search', '')
    coin_type = request.args.get('type', '')
    sort_by = request.args.get('sort', 'name')

    coins = GameCoin.query.filter_by(user_id=current_user.id)
    if search_query:
        coins = coins.filter(GameCoin.name.ilike(f'%{search_query}%'))
    if coin_type:
        coins = coins.filter_by(type=coin_type)
    
    coins = coins.order_by(getattr(GameCoin, sort_by)).all()

    coins_data = [{
        'id': coin.id,
        'name': coin.name,
        'type': coin.type,
        'value': coin.value,
        'quantity': coin.quantity,
        'description': coin.description
    } for coin in coins]

    return render_template('coins.html', coins=coins_data, search=search_query, type=coin_type)



@app.route('/coins/<int:coin_id>', methods=['PUT', 'DELETE'])
@login_required
def modify_coin(coin_id):
    coin = GameCoin.query.filter_by(id=coin_id, user_id=current_user.id).first_or_404()

    if request.method == 'PUT':  # Only handle PUT for edits
        data = request.get_json()
        if data:
            coin.name = data.get('name', coin.name)
            coin.type = data.get('type', coin.type)
            coin.value = float(data.get('value', coin.value))
            coin.quantity = int(data.get('quantity', coin.quantity))
            coin.description = data.get('description', coin.description)
            db.session.commit()

            history = TransactionHistory(user_id=current_user.id, action=f"Updated coin {coin.name}")
            db.session.add(history)
            db.session.commit()

            return jsonify({'message': f'Coin {coin.name} updated successfully!'}), 200

    elif request.method == 'DELETE':
        db.session.delete(coin)
        db.session.commit()
        history = TransactionHistory(user_id=current_user.id, action=f"Deleted coin {coin.name}")
        db.session.add(history)
        db.session.commit()
        return jsonify({'message': f'Coin {coin.name} deleted successfully!'}), 200

    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('home'))

@app.route('/transactions')
@login_required
def transaction_history():
    transactions = TransactionHistory.query.filter_by(user_id=current_user.id).all()
    return render_template('transactions.html', transactions=transactions)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
