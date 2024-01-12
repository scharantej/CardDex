 
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create a Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Define the Card model
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    rarity = db.Column(db.String(80), nullable=False)

# Define the Deck model
class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Define the Trade model
class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    trade_status = db.Column(db.String(80), nullable=False)

# Create the database tables
db.create_all()

# Define the home page route
@app.route('/')
def index():
    return render_template('index.html')

# Define the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and the password is correct
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            # Log the user in
            return redirect(url_for('dashboard'))

        # If the user does not exist or the password is incorrect, display an error message
        return render_template('index.html', error="Invalid username or password")

    return render_template('index.html')

# Define the registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        user = User.query.filter_by(username=username).first()
        if user:
            # Display an error message
            return render_template('index.html', error="Username already taken")

        # Create a new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Log the user in
        return redirect(url_for('dashboard'))

    return render_template('index.html')

# Define the dashboard route
@app.route('/dashboard')
def dashboard():
    # Get the current user
    user = User.query.get(1)

    # Get the user's cards
    cards = Card.query.filter_by(user_id=user.id).all()

    # Get the user's decks
    decks = Deck.query.filter_by(user_id=user.id).all()

    # Get the user's trades
    trades = Trade.query.filter_by(user_id=user.id).all()

    return render_template('dashboard.html', user=user, cards=cards, decks=decks, trades=trades)

# Define the trade route
@app.route('/trade', methods=['GET', 'POST'])
def trade():
    if request.method == 'POST':
        card_id = request.form['card_id']
        trade_status = request.form['trade_status']

        # Get the card
        card = Card.query.get(card_id)

        # Create a new trade
        new_trade = Trade(user_id=1, card_id=card_id, trade_status=trade_status)
        db.session.add(new_trade)
        db.session.commit()

        # Redirect to the dashboard
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html')

# Define the deckbuilder route
@app.route('/deckbuilder')
def deckbuilder():
    # Get the current user
    user = User.query.get(1)

    # Get the user's cards
    cards = Card.query.filter_by(user_id=user.id).all()

    # Get the user's decks
    decks = Deck.query.filter_by(user_id=user.id).all()

    return render_template('deckbuilder.html', user=user, cards=cards, decks=decks)

# Define the game route
@app.route('/game')
def game():
    # Get the current user
    user = User.query.get(1)

    # Get the user's decks
    decks = Deck.query.filter_by(user_id=user.id).all()

    return render_template('game.html', user=user, decks=decks)

# Run the app
if __name__ == '__main__':
    app.run()
