document.addEventListener("DOMContentLoaded", function() {
    const showsContainer = document.getElementById('shows-container');
    const loadingElement = document.getElementById('loading');
    let page = 1;
    let isLoading = false;
    let hasMoreShows = true;

    async function fetchShows(page) {
        if (isLoading || !hasMoreShows) return;
        isLoading = true;
        loadingElement.style.display = 'block';

        try {
            // Simulating a fetch with static data for demonstration
            const data = {
                shows: Array.from({ length: 8 }, (_, i) => ({
                    image: `https://picsum.photos/200/300?random=${(page - 1) * 8 + i + 1}`,
                    title: `Show ${(page - 1) * 8 + i + 1}`,
                    description: `Description for Show ${(page - 1) * 8 + i + 1}`,
                    link: '#'
                }))
            };

            if (data.shows.length === 0) {
                hasMoreShows = false;
                loadingElement.textContent = 'No more shows';
            } else {
                data.shows.forEach(show => {
                    const showElement = document.createElement('div');
                    showElement.classList.add('col-md-3');
                    showElement.innerHTML = `
                        <div class="card mb-4">
                            <img src="${show.image}" class="card-img-top" alt="${show.title}">
                            <div class="card-body">
                                <h5 class="card-title">${show.title}</h5>
                                <p class="card-text">${show.description}</p>
                                <a href="${show.link}" class="btn" style="background-color: #212529; color: white;">Book Ticket</a>
                            </div>
                        </div>
                    `;
                    showsContainer.appendChild(showElement);
                });
            }
        } catch (error) {
            console.error('Error fetching shows:', error);
        }

        loadingElement.style.display = 'none';
        isLoading = false;
    }

    function handleScroll() {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500) {
            page++;
            fetchShows(page);
        }
    }

    window.addEventListener('scroll', handleScroll);
    fetchShows(page);
});