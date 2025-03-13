from app import db
from app.models import Booking, Event

def get_trending(user_id):
    # Placeholder for the recommendation algorithm
    # For now, we will just recommend the top 5 events/movies with the most booked seats
    bookings = db.session.query(Booking.event_id, db.func.sum(Booking.number_of_tickets).label('total_seats')).group_by(Booking.event_id).order_by(db.desc('total_seats')).limit(5).all()
    trending = []
    for booking in bookings:
        event = Event.query.get(booking.event_id)
        trending.append({
            'event_id': event.event_id,
            'name': event.event_name,
            'thumbnail': event.event_thumbnail,
            'description': event.event_description[:100] + "..." if len(event.event_description) > 100 else event.event_description
        })
    return trending