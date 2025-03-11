document.addEventListener("DOMContentLoaded", function() {
    const bookTicketBtn = document.querySelector('.book-ticket-btn');
    const urlParams = new URLSearchParams(window.location.search);
    const eventId = urlParams.get('event_id');
    console.log('Event ID from URL:', eventId); // Debug log

    if (eventId) {
        fetch(`/api/event/${eventId}`) // Fetch event details from the server
            .then(response => response.json())
            .then(data => {
                console.log('Fetched event data:', data); // Debug log
                if (data.success) {
                    const event = data.event;
                    // Ensure elements are correctly selected and exist
                    const titleElement = document.querySelector('.event-title');
                    const imgElement = document.querySelector('.event-image');
                    const descriptionElement = document.querySelector('.event-description');
                    const genreElement = document.querySelector('.event-genre');
                    const dateTimeElement = document.querySelector('.event-date-time');
                    const venueElement = document.querySelector('.event-venue');
                    const cityElement = document.querySelector('.event-city');
                    const bookButton = document.querySelector('.book-ticket-btn');

                    if (titleElement && imgElement && descriptionElement && genreElement && dateTimeElement && venueElement && cityElement && bookButton) {
                        titleElement.textContent = event.event_name;
                        imgElement.src = event.event_thumbnail;
                        imgElement.alt = event.event_name;
                        descriptionElement.textContent = event.event_description;
                        genreElement.textContent = event.genre;
                        dateTimeElement.textContent = `${event.date}, ${event.time}`;
                        venueElement.textContent = event.venue;
                        cityElement.textContent = event.city;
                        bookButton.href = `/select_seats?event_id=${event.event_id}`;
                    } else {
                        console.error('One or more elements are missing in the DOM');
                    }
                } else {
                    console.error('Error fetching event details:', data.status_message);
                }
            })
            .catch(error => console.error('Error fetching event details:', error));
    } else {
        console.error('No event_id found in URL');
    }

    const reviewForm = document.getElementById('review-form');
    const reviewsContainer = document.getElementById('reviews-container');

    reviewForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const rating = document.getElementById('rating').value;
        const comment = document.getElementById('comment').value;
        const eventId = urlParams.get('event_id');

        fetch('/submit_review', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                event_id: eventId,
                rating: rating,
                comment: comment
            })
        })
        .then(response => response.text())  // Changed to .text() to handle HTML response
        .then(data => {
            try {
                data = JSON.parse(data);  // Attempt to parse JSON
            } catch (e) {
                console.error('Error parsing JSON:', e);
                throw new Error('Invalid JSON response');
            }

            if (data.success) {
                const reviewElement = document.createElement('div');
                reviewElement.classList.add('card', 'mb-3');
                reviewElement.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">Rating: ${rating}</h5>
                        <p class="card-text">${comment}</p>
                        <p class="card-text"><small class="text-muted">Just now</small></p>
                    </div>
                `;

                reviewsContainer.prepend(reviewElement);
                reviewForm.reset();
            } else {
                console.error('Error submitting review:', data.message);
            }
        })
        .catch(error => console.error('Error submitting review:', error));
        
            bookTicketBtn.addEventListener('click', function () {
                const eventId = this.getAttribute('data-event-id'); // Assuming data-event-id attribute is set
                window.location.href = `/select_seats?event_id=${eventId}`;
            });
    });
});