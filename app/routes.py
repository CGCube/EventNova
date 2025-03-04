from flask import render_template, request, redirect, url_for, flash, jsonify, session
from app import db
from app.models import Guest, Organizer  # Assuming you have a Guest and Organizer model
import logging

# Setting up logging
logging.basicConfig(level=logging.DEBUG)

shows = [
    {"id": 1, "title": "Show 1", "description": "Description for Show 1", "image": "https://picsum.photos/200/300", "booking_link": "#"},
    {"id": 2, "title": "Show 2", "description": "Description for Show 2", "image": "https://picsum.photos/200/300", "booking_link": "#"},
    # Add more shows as needed
]

isLoggedIn = False
UserType = ""
currentUser = None

def generate_seat_labels(rows, cols):
    labels = []
    for i in range(rows):
        row_labels = []
        for j in range(1, cols + 1):
            row_labels.append(f"{chr(65 + i)}{j}")
        labels.append(row_labels)
    return labels

def init_routes(app):

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

    @app.route('/submit_signup_guest', methods=['POST'])
    def submit_signup_guest():
        gname = request.form.get('gname')
        gemail = request.form.get('gemail')
        gpassword = request.form.get('gpassword')
        gusername = request.form.get('gusername')
        gphone = request.form.get('gphone')

        # Perform server-side validation if necessary

        # Create a new guest user and save to the database
        new_guest = Guest(gname=gname, gemail=gemail, gpassword=gpassword, gusername=gusername, gphone=gphone)
        db.session.add(new_guest)
        db.session.commit()

        # Flash a success message and redirect to login page
        flash('Sign up successful! Please log in.', 'success')
        return redirect(url_for('login'))

    @app.route('/submit_signup_organizer', methods=['POST'])
    def submit_signup_organizer():
        oname = request.form.get('oname')
        oemail = request.form.get('oemail')
        opassword = request.form.get('opassword')
        ousername = request.form.get('ousername')
        ophone = request.form.get('ophone')
        odescription = request.form.get('odescription')

        # Perform server-side validation if necessary

        # Create a new organizer user and save to the database
        new_organizer = Organizer(oname=oname, oemail=oemail, opassword=opassword, ousername=ousername, ophone=ophone, odescription=odescription)
        db.session.add(new_organizer)
        db.session.commit()

        # Flash a success message and redirect to login page
        flash('Sign up successful! Please log in.', 'success')
        return redirect(url_for('login'))

    @app.route('/submit_login', methods=['POST'])
    def submit_login():
        global isLoggedIn, UserType, currentUser

        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')

        logging.debug(f"Login attempt with email: {email}, user_type: {user_type}")

        if user_type == "Guest":
            user = Guest.query.filter_by(gemail=email, gpassword=password).first()
            logging.debug(f"Guest user found: {user}")
            if user:
                UserType = "guest"
                currentUser = user.gusername
        elif user_type == "Organizer":
            user = Organizer.query.filter_by(oemail=email, opassword=password).first()
            logging.debug(f"Organizer user found: {user}")
            if user:
                UserType = "organizer"
                currentUser = user.ousername
        else:
            return jsonify({"success": False})

        if user:
            isLoggedIn = True
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})

    @app.route('/get_profile')
    def get_profile():
        global currentUser
        if UserType == "guest":
            user = Guest.query.filter_by(gusername=currentUser).first()
        elif UserType == "organizer":
            user = Organizer.query.filter_by(ousername=currentUser).first()
        else:
            return jsonify({"success": False})

        if user:
            profile = {
                "name": user.gname if UserType == "guest" else user.oname,
                "guest_id": user.gusername if UserType == "guest" else None,
                "organizer_id": user.ousername if UserType == "organizer" else None,
                "email": user.gemail if UserType == "guest" else user.oemail,
                "phone": user.gphone if UserType == "guest" else user.ophone,
                "description": user.odescription if UserType == "organizer" else None
            }
            return jsonify({"success": True, "profile": profile})
        else:
            return jsonify({"success": False})

    @app.route('/update_profile', methods=['POST'])
    def update_profile():
        global currentUser
        data = request.json
        if UserType == "guest":
            user = Guest.query.filter_by(gusername=currentUser).first()
            if user:
                user.gname = data["name"]
                user.gemail = data["email"]
                user.gphone = data["phone"]
        elif UserType == "organizer":
            user = Organizer.query.filter_by(ousername=currentUser).first()
            if user:
                user.oname = data["name"]
                user.oemail = data["email"]
                user.ophone = data["phone"]
                user.odescription = data["description"]
        else:
            return jsonify({"success": False})

        if user:
            db.session.commit()
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})

    @app.route('/change_password', methods=['POST'])
    def change_password():
        global currentUser
        data = request.json
        current_password = data["current_password"]
        new_password = data["new_password"]
        confirm_password = data["confirm_password"]

        if new_password != confirm_password:
            return jsonify({"success": False, "message": "New passwords do not match."})

        if UserType == "guest":
            user = Guest.query.filter_by(gusername=currentUser, gpassword=current_password).first()
            if user:
                user.gpassword = new_password
        elif UserType == "organizer":
            user = Organizer.query.filter_by(ousername=currentUser, opassword=current_password).first()
            if user:
                user.opassword = new_password
        else:
            return jsonify({"success": False})

        if user:
            db.session.commit()
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Current password is incorrect."})

    @app.route('/logout', methods=['POST'])
    def logout():
        global isLoggedIn, UserType, currentUser
        isLoggedIn = False
        UserType = ""
        currentUser = None
        return jsonify({"success": True})

    @app.route('/get_order_history')
    def get_order_history():
        # This is a placeholder implementation. Replace it with your actual order fetching logic.
        orders = [
            {"type": "Movie", "name": "Avengers: Endgame", "date": "2023-01-15"},
            {"type": "Event", "name": "Music Concert", "date": "2023-03-10"},
            {"type": "Show", "name": "Comedy Night", "date": "2023-04-05"}
        ]
        return jsonify({"success": True, "orders": orders})