function selectLocation(location) {
    // Update the text of the Location dropdown
    document.getElementById('locationDropdown').textContent = location;
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Document loaded. Fetching events...');
    fetch('/api/events') // Fetch events from the server
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!data.success) {
                throw new Error(data.status_message);
            }
            console.log('Data received:', data);
            const { movies, shows } = data.events;

            const movieCards = document.querySelectorAll('.movie-card');
            movies.forEach((movie, index) => {
                if (index < movieCards.length) {
                    const movieCard = movieCards[index];
                    const imgElement = movieCard.querySelector('.card-img-top');
                    const titleElement = movieCard.querySelector('.card-title');
                    const textElement = movieCard.querySelector('.card-text');
                    const btnElement = movieCard.querySelector('.btn');
                    
                    if (imgElement && titleElement && textElement && btnElement) {
                        imgElement.src = movie.event_thumbnail;
                        imgElement.alt = movie.event_name;
                        titleElement.textContent = movie.event_name;
                        textElement.textContent = truncateText(movie.event_description, 50); // Truncate to 50 characters
                        btnElement.href = `/view_description/${movie.event_id}`;
                    } else {
                        console.warn('Some elements are missing in the card structure.');
                    }
                }
            });

            const showCards = document.querySelectorAll('.show-card');
            shows.forEach((show, index) => {
                if (index < showCards.length) {
                    const showCard = showCards[index];
                    const imgElement = showCard.querySelector('.card-img-top');
                    const titleElement = showCard.querySelector('.card-title');
                    const textElement = showCard.querySelector('.card-text');
                    const btnElement = showCard.querySelector('.btn');
                    
                    if (imgElement && titleElement && textElement && btnElement) {
                        imgElement.src = show.event_thumbnail;
                        imgElement.alt = show.event_name;
                        titleElement.textContent = show.event_name;
                        textElement.textContent = truncateText(show.event_description, 50); // Truncate to 50 characters
                        btnElement.href = `/view_description/${show.event_id}`;
                    } else {
                        console.warn('Some elements are missing in the card structure.');
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching events:', error));
});

function truncateText(text, maxLength) {
    if (text.length > maxLength) {
        return text.substring(0, maxLength) + '...';
    }
    return text;
}