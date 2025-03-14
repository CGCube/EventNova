from app import db
from app.models import Booking, Event, GuestGenre
import random

def get_trending(user_id):
    print(f"Getting trending events for user: {user_id}")
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
    print(f"Trending events: {trending}")
    return trending

def get_recommendations(user_id):
    print(f"Getting recommendations for user: {user_id}")
    if not user_id:
        return []
    
    guest_genres = db.session.query(GuestGenre.genre).filter_by(guest_username=user_id).distinct().all()
    print(f"Guest genres: {guest_genres}")
    genres = set()
    for genre in guest_genres:
        genres.update(genre[0].split(','))
    print(f"Unique genres: {genres}")

    if not genres:
        return []

    recommended_events = []
    for genre in genres:
        events = db.session.query(Event).filter(Event.genre.ilike(f'%{genre.strip()}%')).all()
        recommended_events.extend(events)
    print(f"Recommended events before deduplication: {recommended_events}")

    recommended_events = list({event.event_id: event for event in recommended_events}.values())
    random.shuffle(recommended_events)
    recommended_events = recommended_events[:4]
    print(f"Final recommended events: {recommended_events}")

    recommendations = []
    for event in recommended_events:
        recommendations.append({
            'event_id': event.event_id,
            'name': event.event_name,
            'thumbnail': event.event_thumbnail,
            'description': event.event_description[:100] + "..." if len(event.event_description) > 100 else event.event_description
        })
    print(f"Recommendations: {recommendations}")
    return recommendations