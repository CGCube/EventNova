document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('add-event-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Get form values
        const eventName = document.getElementById('event-name').value;
        const eventType = document.getElementById('event-type').value;
        const eventDate = document.getElementById('event-date').value;
        const eventTime = document.getElementById('event-time').value;
        const venue = document.getElementById('venue').value;
        const city = document.getElementById('city').value;
        const pricePerSeat = document.getElementById('price-per-seat').value;
        const tags = document.getElementById('tags').value;
        const genre = document.getElementById('genre').value;
        const thumbnail = document.getElementById('thumbnail').files[0];

        // Create an event object
        const newEvent = {
            name: eventName,
            type: eventType,
            date: eventDate,
            time: eventTime,
            venue: venue,
            city: city,
            pricePerSeat: pricePerSeat,
            tags: tags.split(',').map(tag => tag.trim()),
            genre: genre,
            thumbnail: thumbnail ? thumbnail.name : ''
        };

        // Log the event object to the console (or send to a server)
        console.log('New Event:', newEvent);

        // Optionally, you can reset the form after submission
        form.reset();

        // Display a success message or redirect the user
        alert('Event added successfully!');
    });
});