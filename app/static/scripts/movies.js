document.addEventListener("DOMContentLoaded", function() {
    const moviesContainer = document.getElementById('movies-container');
    const loadingElement = document.getElementById('loading');
    let page = 1;
    let isLoading = false;
    let hasMoreMovies = true;

    async function fetchMovies(page) {
        if (isLoading || !hasMoreMovies) return;
        isLoading = true;
        loadingElement.style.display = 'block';

        try {
            // Simulating a fetch with static data for demonstration
            const data = {
                movies: Array.from({ length: 8 }, (_, i) => ({
                    image: `https://picsum.photos/200/300?random=${(page - 1) * 8 + i + 1}`,
                    title: `Movie ${(page - 1) * 8 + i + 1}`,
                    description: `Description for Movie ${(page - 1) * 8 + i + 1}`,
                    link: '#'
                }))
            };

            if (data.movies.length === 0) {
                hasMoreMovies = false;
                loadingElement.textContent = 'No more movies';
            } else {
                data.movies.forEach(movie => {
                    const movieElement = document.createElement('div');
                    movieElement.classList.add('col-md-3');
                    movieElement.innerHTML = `
                        <div class="card mb-4">
                            <img src="${movie.image}" class="card-img-top" alt="${movie.title}">
                            <div class="card-body">
                                <h5 class="card-title">${movie.title}</h5>
                                <p class="card-text">${movie.description}</p>
                                <a href="${movie.link}" class="btn" style="background-color: #212529; color: white;">Book Ticket</a>
                            </div>
                        </div>
                    `;
                    moviesContainer.appendChild(movieElement);
                });
            }
        } catch (error) {
            console.error('Error fetching movies:', error);
        }

        loadingElement.style.display = 'none';
        isLoading = false;
    }

    function handleScroll() {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500) {
            page++;
            fetchMovies(page);
        }
    }

    window.addEventListener('scroll', handleScroll);
    fetchMovies(page);
});