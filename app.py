from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import qrcode

app = Flask(__name__)
CORS(app)

# Database setup (SQLite for simplicity, can be upgraded to PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bus.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Seat model
class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    booked = db.Column(db.Boolean, default=False)

# Initialize Database
with app.app_context():
    db.create_all()
    if Seat.query.count() == 0:
        for i in range(1, 51):
            db.session.add(Seat(number=i))
        db.session.commit()

# Get seat status
@app.route('/seats', methods=['GET'])
def get_seats():
    seats = Seat.query.all()
    return jsonify([{"id": s.id, "number": s.number, "booked": s.booked} for s in seats])

# Book seat
@app.route('/book', methods=['POST'])
def book_seat():
    data = request.json
    seat = Seat.query.get(data["seat_id"])
    
    if seat and not seat.booked:
        seat.booked = True
        db.session.commit()
        
        # Generate GPay QR Code
        qr = qrcode.make("upi://pay?pa=your_upi_id@upi&pn=BusBooking&am=500")
        qr.save("static/gpay_qr.png")

        return jsonify({"success": True, "message": "Seat booked!", "qr_code": "static/gpay_qr.png"})
    return jsonify({"success": False, "message": "Seat unavailable"})

if __name__ == '__main__':
    app.run(debug=True)
