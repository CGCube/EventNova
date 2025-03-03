document.addEventListener('DOMContentLoaded', function() {
    const seatCheckboxes = document.querySelectorAll('.btn-check');
    const confirmButton = document.querySelector('#confirmButton');

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
        document.querySelector('#seatForm').submit();
    });

    // Initial check for confirm button state
    updateConfirmButton();
});