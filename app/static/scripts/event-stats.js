document.addEventListener("DOMContentLoaded", function() {
    const eventNameElement = document.getElementById('event-name');
    const ticketsBookedElement = document.getElementById('tickets-booked');
    const reviewsContainer = document.getElementById('reviews-container');
    const bookedTicketsTableBody = document.querySelector('#booked-tickets-table tbody');
    
    // Placeholder for event statistics data
    const eventStats = {
        name: "Sample Event",
        ticketsBooked: 300,
        reviews: [
            "Great event!",
            "Had a wonderful time.",
            "Would attend again."
        ],
        bookings: [
            { guestName: "John Doe", tickets: 2 },
            { guestName: "Jane Smith", tickets: 4 },
            { guestName: "Alice Johnson", tickets: 1 }
        ]
    };
    
    // Function to render event statistics
    function renderStats(stats) {
        eventNameElement.textContent = `Event Name: ${stats.name}`;
        ticketsBookedElement.textContent = `Number of Tickets Booked: ${stats.ticketsBooked}`;
        
        // Render reviews
        stats.reviews.forEach(review => {
            const reviewElement = document.createElement('p');
            reviewElement.textContent = review;
            reviewsContainer.appendChild(reviewElement);
        });
        
        // Render booked tickets table
        stats.bookings.forEach(booking => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${booking.guestName}</td>
                <td>${booking.tickets}</td>
            `;
            bookedTicketsTableBody.appendChild(row);
        });
    }

    renderStats(eventStats);
});