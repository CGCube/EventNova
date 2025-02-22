document.addEventListener("DOMContentLoaded", function() {
    const eventsContainer = document.getElementById('events-container');
    const loadingElement = document.getElementById('loading');
    let page = 1;
    let isLoading = false;
    let hasMoreEvents = true;

    async function fetchEvents(page) {
        if (isLoading || !hasMoreEvents) return;
        isLoading = true;
        loadingElement.style.display = 'block';

        try {
            // Simulating a fetch with static data for demonstration
            const data = {
                events: Array.from({ length: 8 }, (_, i) => ({
                    image: `https://picsum.photos/200/300?random=${(page - 1) * 8 + i + 1}`,
                    title: `Event ${(page - 1) * 8 + i + 1}`,
                    description: `Description for Event ${(page - 1) * 8 + i + 1}`,
                    link: '#'
                }))
            };

            if (data.events.length === 0) {
                hasMoreEvents = false;
                loadingElement.textContent = 'No more events';
            } else {
                data.events.forEach(event => {
                    const eventElement = document.createElement('div');
                    eventElement.classList.add('col-md-3');
                    eventElement.innerHTML = `
                        <div class="card mb-4">
                            <img src="${event.image}" class="card-img-top" alt="${event.title}">
                            <div class="card-body">
                                <h5 class="card-title">${event.title}</h5>
                                <p class="card-text">${event.description}</p>
                                <a href="${event.link}" class="btn" style="background-color: #212529; color: white;">Book Ticket</a>
                            </div>
                        </div>
                    `;
                    eventsContainer.appendChild(eventElement);
                });
            }
        } catch (error) {
            console.error('Error fetching events:', error);
        }

        loadingElement.style.display = 'none';
        isLoading = false;
    }

    function handleScroll() {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500) {
            page++;
            fetchEvents(page);
        }
    }

    window.addEventListener('scroll', handleScroll);
    fetchEvents(page);
});