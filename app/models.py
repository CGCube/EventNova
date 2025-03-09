from app import db

class Guest(db.Model):
    __tablename__ = 'guests'
    guest_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gname = db.Column(db.String(100), nullable=False)
    gemail = db.Column(db.String(100), nullable=False)
    gpassword = db.Column(db.String(100), nullable=False)
    gphone = db.Column(db.String(10), nullable=True)
    gusername = db.Column(db.String(100), nullable=False)
    glocation = db.Column(db.String(100), nullable=False)  # New field for location

class Organizer(db.Model):
    __tablename__ = 'organizers'
    organizer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oname = db.Column(db.String(100), nullable=False)
    oemail = db.Column(db.String(100), nullable=False)
    opassword = db.Column(db.String(100), nullable=False)
    ophone = db.Column(db.String(15), nullable=False)
    odescription = db.Column(db.Text, nullable=True)
    ousername = db.Column(db.String(100), nullable=False)

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('organizers.organizer_id'), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    event_thumbnail = db.Column(db.String(500), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    event_description = db.Column(db.Text, nullable=False)

class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.guest_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    number_of_tickets = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.guest_id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=False)

class Seat(db.Model):
    __tablename__ = 'seats'
    seat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.guest_id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    seat_number = db.Column(db.String(3), nullable=False)

class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.guest_id'), nullable=False)
    rating = db.Column(db.SmallInteger, nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    review_timestamp = db.Column(db.DateTime, nullable=False)