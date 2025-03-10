from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Database Configuration (Update this with your actual database URI)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Use PostgreSQL if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Example Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Initialize Database (Run only once)
with app.app_context():
    db.create_all()

# Sample Route
@app.route('/')
def home():
    return jsonify({'message': 'Shree Samarth Krupa Tours and Travels API is running!'})

# Sample API to add a user
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.json
        new_user = User(name=data['name'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Run the App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Ensure the port is set properly for Render
