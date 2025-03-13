from app import db
from app.models import Booking, Event

def get_trending(user_id):
    # Placeholder for the recommendation algorithm
    # For now, we will just recommend the top 5 most booked events/movies
    bookings = db.session.query(Booking.event_id, db.func.count(Booking.event_id).label('count')).group_by(Booking.event_id).order_by(db.desc('count')).limit(5).all()
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