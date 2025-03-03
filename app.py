from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

shows = [
    {"id": 1, "title": "Show 1", "description": "Description for Show 1", "image": "https://picsum.photos/200/300", "booking_link": "#"},
    {"id": 2, "title": "Show 2", "description": "Description for Show 2", "image": "https://picsum.photos/200/300", "booking_link": "#"},
    # Add more shows as needed
]

isLoggedIn = 0
UserType = "organizer"

def generate_seat_labels(rows, cols):
    labels = []
    for i in range(rows):
        row_labels = []
        for j in range(1, cols + 1):
            row_labels.append(f"{chr(65 + i)}{j}")
        labels.append(row_labels)
    return labels

@app.route('/')
def index():
    return render_template('home.html', isLoggedIn=isLoggedIn)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup_select')
def signup_select():
    return render_template('signup_select.html')

@app.route('/signup_guest')
def signup_guest():
    return render_template('signup_guest.html')

@app.route('/signup_organizer')
def signup_organizer():
    return render_template('signup_organizer.html')

@app.route('/shows')
def shows():
    return render_template('shows.html', isLoggedIn=isLoggedIn)

@app.route('/movies')
def movies():
    return render_template('movies.html', isLoggedIn=isLoggedIn)

@app.route('/view_description')
def view_description():
    return render_template('view_description.html', isLoggedIn=isLoggedIn)

@app.route('/select_seats', methods=['GET', 'POST'])
def select_seats():
    if request.method == 'POST':
        selected_seats = request.form.getlist('seats')
        return redirect(url_for('booking_confirmation', seats=','.join(selected_seats)))
    
    seat_labels = generate_seat_labels(10, 20)
    selected_seats = []  # Example selected seats
    return render_template('seat_selection.html', isLoggedIn=True, seat_labels=seat_labels, selected_seats=selected_seats)

if isLoggedIn & (UserType == "organizer"):
    @app.route('/add-event')
    def add_event():
        return render_template('add_event.html')
    @app.route('/update-event')
    def edit_event():
        return render_template('update_event.html')
    @app.route('/event-stats')
    def event_stats():
        return render_template('event_stats.html')

@app.route('/profile')
def user_profile():
    if isLoggedIn:
        if UserType == "guest":
            return render_template('profile_guest.html')
        elif UserType == "organizer":
            return render_template('profile_organizer.html')
    else:
        return 'NOT LOGGED IN'

@app.route('/booking_summary')
def booking_summary():
    payment_success = True  # Example variable
    event_name = "Sample Event"
    location = "Sample Location"
    date = "2025-03-03"
    time = "18:30"
    seats = "A1, A2, A3"
    txn_id = "1234567890"
    booking_date = "2025-03-03"
    booking_time = "19:07:33"
    return render_template('booking_summary.html', isLoggedIn=True, payment_success=payment_success, event_name=event_name, location=location, date=date, time=time, seats=seats, txn_id=txn_id, booking_date=booking_date, booking_time=booking_time)

@app.route('/booking_confirmation')
def booking_confirmation():
    seats = request.args.get('seats', '')  # Get selected seats from query parameters
    seat_list = seats.split(',') if seats else []
    price_per_seat = 15.0  # Example price per seat
    total_amount = price_per_seat * len(seat_list)
    return render_template('booking_confirmation.html', isLoggedIn=True, seats=seats, price_per_seat=price_per_seat, total_amount=total_amount)

if __name__ == '__main__':
    app.run(debug=True)