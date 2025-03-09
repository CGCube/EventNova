document.addEventListener('DOMContentLoaded', function() {
    const seatCheckboxes = document.querySelectorAll('.btn-check');
    const confirmButton = document.querySelector('#confirmButton');

    // Retrieve event_id and guest_id from the form
    const eventId = document.getElementById('event_id').value;
    const guestId = document.getElementById('guest_id').value;
    console.log('Event ID:', eventId); // Debugging line
    console.log('Guest ID:', guestId); // Debugging line

    // Add event listener for seat selection
    seatCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const label = document.querySelector(`label[for="${checkbox.id}"]`);
            if (checkbox.checked) {
                label.classList.add('btn-success', 'text-white', 'border-success');
            } else {
                label.classList.remove('btn-success', 'text-white', 'border-success');
            }
            updateConfirmButton();
        });

        // Initial check for already selected seats
        if (checkbox.checked) {
            const label = document.querySelector(`label[for="${checkbox.id}"]`);
            label.classList.add('btn-success', 'text-white', 'border-success');
        }
    });

    function updateConfirmButton() {
        const selectedSeats = document.querySelectorAll('.btn-check:checked');
        console.log("Selected seats: ", selectedSeats.length); // Debugging line
    }

    // Add event listener for confirm button
    confirmButton.addEventListener('click', function(event) {
        event.preventDefault();

        const selectedSeats = Array.from(document.querySelectorAll('.btn-check:checked'))
            .map(seat => seat.value);

        if (selectedSeats.length === 0) {
            alert('Please select at least one seat.');
            return;
        }

        const noOfSeats = selectedSeats.length;

        // Store the values in appropriate variables
        const bookingDetails = {
            guest_id: guestId,
            event_id: eventId,
            number_of_seats: noOfSeats,
            seat_numbers: selectedSeats
        };

        console.log('Booking Details:', bookingDetails);

        // Display an alert with the variables and their values
        alert(`Guest ID: ${guestId}\nEvent ID: ${eventId}\nNumber of Seats: ${noOfSeats}\nSeat Numbers: ${selectedSeats.join(', ')}`);

        // Submit the form or send data to the server as needed
        document.querySelector('#seatForm').submit();
    });

    // Initial check for confirm button state
    updateConfirmButton();
});