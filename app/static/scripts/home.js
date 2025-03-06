function selectLocation(location) {
    // Update the text of the Location dropdown
    document.getElementById('locationDropdown').textContent = location;
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Document loaded. Fetching popular movies...');
    fetch('/api/config') // Fetch configuration from the server
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(config => {
            const apiKey = config.TMDB_API_KEY;
            return fetch(`https://api.themoviedb.org/3/movie/popular?api_key=${apiKey}&region=IN&include_adult=false`);
        })
        .then(response => {
            console.log('API response received');
            return response.json();
        })
        .then(data => {
            if (!data.success) {
                throw new Error(data.status_message);
            }
            console.log('Data received:', data);
            // Genres to exclude
            const excludedGenres = ['Horror', 'Murder', 'Thriller'];

            // Languages to include
            const includedLanguages = ['hi', 'en', 'te', 'mr'];

            // Filter the movie data
            const movies = data.results
                .filter(movie => 
                    !movie.genre_ids.some(genre => excludedGenres.includes(genre)) &&
                    includedLanguages.includes(movie.original_language)
                )
                .sort(() => Math.random() - 0.5);

            const movieCards = document.querySelectorAll('.card');
            movies.forEach((movie, index) => {
                if (index < movieCards.length) {
                    const movieCard = movieCards[index];
                    const imgElement = movieCard.querySelector('.card-img-top');
                    const titleElement = movieCard.querySelector('.card-title');
                    const textElement = movieCard.querySelector('.card-text');
                    const btnElement = movieCard.querySelector('.btn');
                    
                    if (imgElement && titleElement && textElement && btnElement) {
                        imgElement.src = `https://image.tmdb.org/t/p/w200${movie.poster_path}`;
                        imgElement.alt = movie.title;
                        titleElement.textContent = movie.title;
                        textElement.textContent = truncateText(movie.overview, 50); // Truncate to 50 characters
                        btnElement.href = `/movie/${movie.id}`;
                    } else {
                        console.warn('Some elements are missing in the card structure.');
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching movies:', error));
});

function truncateText(text, maxLength) {
    if (text.length > maxLength) {
        return text.substring(0, maxLength) + '...';
    }
    return text;
}