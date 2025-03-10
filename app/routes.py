from flask import render_template, request, redirect, url_for, flash, jsonify, session, current_app
from app import db
from app.models import Guest, Organizer, Event, Review, Booking, Payment, Seat
import logging
import random
from datetime import datetime
import stripe
from app.config import Config

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

isLoggedIn = False
UserType = ""
currentUser = None
currentUserLocation = None  # Variable to store the location of the user
stripe.api_key = Config.STRIPE_API_KEY

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
        return render_template('home.html', isLoggedIn=isLoggedIn, currentUserLocation=currentUserLocation)

    @app.route('/signup_guest')
    def signup_guest():
        return render_template('signup_guest.html', isLoggedIn=isLoggedIn, currentUserLocation=currentUserLocation)

    @app.route('/signup_select')
    def signup_select():
        return render_template('signup_select.html', isLoggedIn=isLoggedIn, currentUserLocation=currentUserLocation)
    
    @app.route('/signup_organizer')
    def signup_organizer():
        return render_template('signup_organizer.html', isLoggedIn=isLoggedIn, currentUserLocation=currentUserLocation)

    @app.route('/shows')
    def shows():
        location_filter = currentUserLocation if currentUserLocation else ""
        events = Event.query.filter_by(event_type='show', city=location_filter).all() if location_filter else Event.query.filter_by(event_type='show').all()
        return render_template('shows.html', isLoggedIn=isLoggedIn, currentUserLocation=currentUserLocation, events=events)

    @app.route('/movies')
    def movies():
        location_filter = currentUserLocation if currentUserLocation else ""
        events = Event.query.filter_by(event_type='movie', city=location_filter).all() if location_filter else Event.query.filter_by(event_type='movie').all()
        return render_template('movies.html', isLoggedIn=isLoggedIn, currentUserLocation=currentUserLocation, events=events)

    @app.route('/api/movies')
    def api_movies():
        try:
            location_filter = currentUserLocation if currentUserLocation else ""
            events = Event.query.filter_by(event_type='movie', city=location_filter).all() if location_filter else Event.query.filter_by(event_type='movie').all()
            movies = []
            for event in events:
                movies.append({
                    "event_id": event.event_id,
                    "event_name": event.event_name[:20] + "..." if len(event.event_name) > 20 else event.event_name,
                    "event_thumbnail": event.event_thumbnail,
                    "event_description": event.event_description[:40] + "..." if len(event.event_description) > 40 else event.event_description
                })
            return jsonify({"movies": movies})
        except Exception as e:
            logging.error(f"Error fetching movies: {e}")
            return jsonify({"error": "An error occurred while fetching movies."}), 500

    @app.route('/api/shows')
    def api_shows():
        try:
            location_filter = currentUserLocation if currentUserLocation else ""
            events = Event.query.filter_by(event_type='show', city=location_filter).all() if location_filter else Event.query.filter_by(event_type='show').all()
            shows = []
            for event in events:
                shows.append({
                    "event_id": event.event_id,
                    "event_name": event.event_name[:20] + "..." if len(event.event_name) > 20 else event.event_name,
                    "event_thumbnail": event.event_thumbnail,
                    "event_description": event.event_description[:40] + "..." if len(event.event_description) > 40 else event.event_description
                })
            return jsonify({"shows": shows})
        except Exception as e:
            logging.error(f"Error fetching shows: {e}")
            return jsonify({"error": "An error occurred while fetching shows."}), 500

    @app.route('/view_description')
    def view_description():
        event_id = request.args.get('event_id')
        event = Event.query.get(event_id)
        reviews = Review.query.filter_by(event_id=event_id).all()
        return render_template('view_description.html', event=event, reviews=reviews, isLoggedIn=isLoggedIn, currentUserLocation=currentUserLocation)

    @app.route('/submit_review', methods=['POST'])
    def submit_review():
        if not isLoggedIn:
            return jsonify({"success": False, "message": "User not logged in"})

        event_id = request.form.get('event_id')
        rating = request.form.get('rating')
        review_text = request.form.get('comment')
        guest = Guest.query.filter_by(gusername=currentUser).first()

        if not guest:
            return jsonify({"success": False, "message": "Guest not found"})

        new_review = Review(
            event_id=event_id,
            guest_id=guest.guest_id,
            rating=rating,
            review_text=review_text,
            review_timestamp=datetime.now()
        )
        db.session.add(new_review)
        db.session.commit()

        return jsonify({"success": True, "message": "Review submitted successfully"})

    @app.route('/select_seats', methods=['GET', 'POST'])
    def select_seats():
        if request.method == 'POST':
            selected_seats = request.form.getlist('seats')
            event_id = request.form.get('event_id')  # Get event_id from form
            return redirect(url_for('booking_confirmation', seats=','.join(selected_seats), event_id=event_id))  # Pass event_id in URL

        seat_labels = generate_seat_labels(10, 20)
        selected_seats = []  # Example selected seats
        guest = Guest.query.filter_by(gusername=currentUser).first()  # Get the current guest user
        guest_id = guest.guest_id if guest else None  # Get the guest ID if available
        return render_template('seat_selection.html', isLoggedIn=True, seat_labels=seat_labels, selected_seats=selected_seats, guest_id=guest_id, currentUserLocation=currentUserLocation)

    if isLoggedIn & (UserType == "organizer"):
        @app.route('/add-event')
        def add_event():
            return render_template('add_event.html', currentUserLocation=currentUserLocation)
        @app.route('/update-event')
        def edit_event():
            return render_template('update_event.html', currentUserLocation=currentUserLocation)
        @app.route('/event-stats')
        def event_stats():
            return render_template('event_stats.html', currentUserLocation=currentUserLocation)

    @app.route('/profile')
    def user_profile():
        if isLoggedIn:
            if UserType == "guest":
                return render_template('profile_guest.html', currentUserLocation=currentUserLocation)
            elif UserType == "organizer":
                return render_template('profile_organizer.html', currentUserLocation=currentUserLocation)
        else:
            return 'NOT LOGGED IN'

    @app.route('/booking_confirmation')
    def booking_confirmation():
        seats = request.args.get('seats', '')  # Get selected seats from query parameters
        seat_list = seats.split(',') if seats else []
        event_id = request.args.get('event_id')  # Get event_id from query parameters
        event = Event.query.get(event_id)  # Fetch event details from database
        price_per_seat = event.price if event else 0  # Get price from event
        total_amount = price_per_seat * len(seat_list)
        return render_template('booking_confirmation.html', isLoggedIn=True, seats=seat_list, price_per_seat=price_per_seat, total_amount=total_amount, currentUserLocation=currentUserLocation)

    @app.route('/submit_signup_guest', methods=['POST'])
    def submit_signup_guest():
        gname = request.form.get('gname')
        gemail = request.form.get('gemail')
        gpassword = request.form.get('gpassword')
        gusername = request.form.get('gusername')
        gphone = request.form.get('gphone')
        glocation = request.form.get('glocation')  # New field for location

        new_guest = Guest(gname=gname, gemail=gemail, gpassword=gpassword, gusername=gusername, gphone=gphone, glocation=glocation)
        db.session.add(new_guest)
        db.session.commit()

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

        new_organizer = Organizer(oname=oname, oemail=oemail, opassword=opassword, ousername=ousername, ophone=ophone, odescription=odescription)
        db.session.add(new_organizer)
        db.session.commit()

        flash('Sign up successful! Please log in.', 'success')
        return redirect(url_for('login'))

    @app.route('/submit_login', methods=['POST'])
    def submit_login():
        global isLoggedIn, UserType, currentUser, currentUserLocation  # Added currentUserLocation

        username = request.form.get('username')
        password = request.form.get('password')
        user_type = request.form.get('user_type')

        logging.debug(f"Login attempt with username: {username}, user_type: {user_type}")

        if user_type == "Guest":
            user = Guest.query.filter_by(gusername=username, gpassword=password).first()
            logging.debug(f"Guest user found: {user}")
            if user:
                UserType = "guest"
                currentUser = user.gusername
                currentUserLocation = user.glocation  # Store the location of the guest user
        elif user_type == "Organizer":
            user = Organizer.query.filter_by(ousername=username, opassword=password).first()
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

    @app.route('/login')
    def login():
        return render_template('login.html')

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
                "guest_id": user.guest_id if UserType == "guest" else None,
                "organizer_id": user.organizer_id if UserType == "organizer" else None,
                "email": user.gemail if UserType == "guest" else user.oemail,
                "phone": user.gphone if UserType == "guest" else user.ophone,
                "description": user.odescription if UserType == "organizer" else None,
                "location": user.glocation if UserType == "guest" else None  # New field for location
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
                user.glocation = data["location"]  # New field for location
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
        global isLoggedIn, UserType, currentUser, currentUserLocation  # Added currentUserLocation
        isLoggedIn = False
        UserType = ""
        currentUser = None
        currentUserLocation = None  # Reset the location
        return jsonify({"success": True})

    @app.route('/get_order_history')
    def get_order_history():
        orders = [
            {"type": "Movie", "name": "Avengers: Endgame", "date": "2023-01-15"},
            {"type": "Event", "name": "Music Concert", "date": "2023-03-10"},
            {"type": "Show", "name": "Comedy Night", "date": "2023-04-05"}
        ]
        return jsonify({"success": True, "orders": orders})

    @app.route('/api/events')
    def api_events():
        location_filter = currentUserLocation if currentUserLocation else ""
        movies = Event.query.filter_by(event_type='movie', city=location_filter).all() if location_filter else Event.query.filter_by(event_type='movie').all()
        shows = Event.query.filter_by(event_type='show', city=location_filter).all() if location_filter else Event.query.filter_by(event_type='show').all()
        
        random.shuffle(movies)
        random.shuffle(shows)
        
        events_list = {
            "movies": [
                {
                    "event_id": event.event_id,
                    "organizer_id": event.organizer_id,
                    "event_name": event.event_name,
                    "event_thumbnail": event.event_thumbnail,
                    "event_type": event.event_type,
                    "genre": event.genre,
                    "date": event.date.strftime('%Y-%m-%d'),
                    "time": event.time.strftime('%H:%M:%S'),
                    "venue": event.venue,
                    "city": event.city,
                    "price": float(event.price),
                    "available_seats": event.available_seats,
                    "event_description": event.event_description
                } for event in movies
            ],
            "shows": [
                {
                    "event_id": event.event_id,
                    "organizer_id": event.organizer_id,
                    "event_name": event.event_name,
                    "event_thumbnail": event.event_thumbnail,
                    "event_type": event.event_type,
                    "genre": event.genre,
                    "date": event.date.strftime('%Y-%m-%d'),
                    "time": event.time.strftime('%H:%M:%S'),
                    "venue": event.venue,
                    "city": event.city,
                    "price": float(event.price),
                    "available_seats": event.available_seats,
                    "event_description": event.event_description
                } for event in shows
            ]
        }
        return jsonify({"success": True, "events": events_list})

    @app.route('/api/event/<int:event_id>')
    def api_event(event_id):
        event = Event.query.get(event_id)
        if event:
            event_data = {
                "event_id": event.event_id,
                "organizer_id": event.organizer_id,
                "event_name": event.event_name,
                "event_thumbnail": event.event_thumbnail,
                "event_type": event.event_type,
                "genre": event.genre,
                "date": event.date.strftime('%Y-%m-%d'),
                "time": event.time.strftime('%H:%M:%S'),
                "venue": event.venue,
                "city": event.city,
                "price": float(event.price),
                "available_seats": event.available_seats,
                "event_description": event.event_description
            }
            return jsonify({"success": True, "event": event_data})
        else:
            return jsonify({"success": False, "status_message": "Event not found"})

    @app.route('/search_events', methods=['POST'])
    def search_events():
        query = request.form.get('query')
        location_filter = currentUserLocation if currentUserLocation else ""
        if query:
            events = Event.query.filter(Event.event_name.ilike(f'%{query}%'), Event.city == location_filter).all() if location_filter else Event.query.filter(Event.event_name.ilike(f'%{query}%')).all()
            event_list = [
                {
                    "event_id": event.event_id,
                    "event_name": event.event_name,
                    "event_description": event.event_description,
                    "event_type": event.event_type,
                    "thumbnail": event.event_thumbnail
                }
                for event in events
            ]
            return jsonify(events=event_list)
        return jsonify(events=[])


    @app.route('/search_results')
    def search_results():
        query = request.args.get('query', '')
        return render_template('search_result.html', query=query, isLoggedIn=isLoggedIn, currentUserLocation=currentUserLocation)
    

    @app.route('/create-payment-intent', methods=['POST'])
    def create_payment_intent():
        data = request.json
        amount = data.get("amount")
        currency = data.get("currency")

        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                payment_method_types=["card"],
            )
            return jsonify({"success": True, "client_secret": intent.client_secret})
        except Exception as e:
            logger.error(f"Error creating payment intent: {str(e)}")
            return jsonify({"success": False, "error": str(e)})

    @app.route('/complete-booking', methods=['POST'])
    def complete_booking():
        data = request.json
        payment_intent_id = data.get("payment_intent_id")
        event_id = data.get("event_id")
        seats = data.get("seats")
        total_amount = data.get("total_amount")

        try:
            # Log the seats array to verify its contents
            logger.debug(f"Seats array before processing: {seats}")

            # Clean the seats array to ensure no extraneous characters
            cleaned_seats = [seat.strip("[]'\" ") for seat in seats]
            logger.debug(f"Seats array after cleaning: {cleaned_seats}")

            # Retrieve the payment intent to get the amount and currency
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            # Assuming user is logged in and we have guest_id
            guest_id = 1  # Replace with actual guest_id from session

            # Create a new booking
            booking = Booking(
                guest_id=guest_id,
                event_id=event_id,
                number_of_tickets=len(cleaned_seats),
                total_price=total_amount
            )
            db.session.add(booking)
            db.session.commit()

            # Create a new payment record
            payment = Payment(
                guest_id=guest_id,
                booking_id=booking.booking_id,
                stripe_payment_id=payment_intent_id,
                amount=intent.amount / 100,  # Convert cents to dollars
                currency=intent.currency,
                status=intent.status
            )
            db.session.add(payment)

            # Update available seats in the event
            event = Event.query.get(event_id)
            event.available_seats -= len(cleaned_seats)
            db.session.add(event)

            # Create seat records for each seat
            for seat in cleaned_seats:
                seat_record = Seat(
                    guest_id=guest_id,
                    booking_id=booking.booking_id,
                    event_id=event_id,
                    seat_number=seat
                )
                db.session.add(seat_record)

            db.session.commit()
            return jsonify({"success": True})
        except Exception as e:
            logger.error(f"Error completing booking: {str(e)}")
            db.session.rollback()
            return jsonify({"success": False, "error": str(e)})

    @app.route('/api/booking_summary', methods=['GET'])
    def booking_summary():
        payment_intent_id = request.args.get('payment_intent')
        if not payment_intent_id:
            logger.error("Missing payment_intent parameter")
            return jsonify({"success": False, "error": "Missing payment_intent parameter"}), 400

        try:
            # Retrieve the payment record
            payment = Payment.query.filter_by(stripe_payment_id=payment_intent_id).first()
            if not payment:
                logger.error("Payment not found")
                return jsonify({"success": False, "error": "Payment not found"}), 404

            # Retrieve the booking record
            booking = Booking.query.get(payment.booking_id)
            if not booking:
                logger.error("Booking not found")
                return jsonify({"success": False, "error": "Booking not found"}), 404

            # Retrieve the event record
            event = Event.query.get(booking.event_id)
            if not event:
                logger.error("Event not found")
                return jsonify({"success": False, "error": "Event not found"}), 404

            # Retrieve the seat records
            seats = Seat.query.filter_by(booking_id=booking.booking_id).all()
            seat_numbers = [seat.seat_number for seat in seats]

            # Prepare the response data
            response_data = {
                "success": True,
                "event_name": event.event_name,
                "location": event.city,
                "date": event.date.strftime("%Y-%m-%d"),
                "time": event.time.strftime("%H:%M:%S"),
                "seats": seat_numbers,
                "txn_id": payment.stripe_payment_id,
                "booking_date": booking.date_created.strftime("%Y-%m-%d"),
                "booking_time": booking.date_created.strftime("%H:%M:%S")
            }
            return jsonify(response_data)
        except Exception as e:
            logger.error(f"Error fetching booking summary: {str(e)}", exc_info=True)
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/booking_summary')
    def booking_summary_page():
        payment_intent = request.args.get('payment_intent')
        payment_success = request.args.get('success', 'false') == 'true'
        
        if payment_intent:
            payment = Payment.query.filter_by(stripe_payment_id=payment_intent).first()
            if payment and payment.status == 'succeeded':
                payment_success = True

        return render_template('booking_summary.html', payment_success=payment_success)
    
    @app.route('/select_seats')
    def seat_selection_page():
        event_id = request.args.get('event_id')
        if not event_id:
            logger.error('Event ID is missing in the URL.')
            return redirect(url_for('home'))  # Redirect to home or an appropriate page if event_id is missing

        # Fetch booked seats for the event
        booked_seat_numbers = db.session.query(Seat.seat_number).filter(Seat.event_id == event_id).all()
        booked_seat_numbers = [seat[0] for seat in booked_seat_numbers]  # Unpack tuples
        logger.info('Fetched Booked Seat Numbers: %s', booked_seat_numbers)  # Debugging line

        guest_id = session.get('guest_id')  # Replace with actual guest_id from session or context
        if guest_id is None:
            logger.error('Guest ID is not available in the session.')
            return redirect(url_for('login'))  # Redirect to login if guest_id is not available

        seat_labels = generate_seat_labels(10, 20)  # Example seat labels, replace with actual logic

        return render_template('seat_selection.html', event_id=event_id, guest_id=guest_id, booked_seat_numbers=booked_seat_numbers, seat_labels=seat_labels)

    @app.route('/api/booked_seats', methods=['GET'])
    def booked_seats():
        event_id = request.args.get('event_id')
        if not event_id:
            return jsonify({"success": False, "error": "Missing event_id parameter"}), 400

        try:
            booked_seat_numbers = db.session.query(Seat.seat_number).filter(Seat.event_id == event_id).all()
            booked_seat_numbers = [seat[0] for seat in booked_seat_numbers]  # Unpack tuples
            logger.info('API Fetched Booked Seat Numbers: %s', booked_seat_numbers)  # Debugging line
            return jsonify({"success": True, "booked_seats": booked_seat_numbers})
        except Exception as e:
            logger.error(f"Error fetching booked seats: {str(e)}", exc_info=True)
            return jsonify({"success": False, "error": str(e)}), 500