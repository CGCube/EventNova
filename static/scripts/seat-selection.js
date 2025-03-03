document.addEventListener('DOMContentLoaded', function() {
    const seatCheckboxes = document.querySelectorAll('.btn-check');
    const confirmButton = document.querySelector('.btn-success');

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
        confirmButton.disabled = selectedSeats.length === 0;
    }

    // Add event listener for confirm button
    confirmButton.addEventListener('click', function(event) {
        event.preventDefault();
        const selectedSeats = document.querySelectorAll('.btn-check:checked');
        const seatNumbers = Array.from(selectedSeats).map(checkbox => checkbox.value);
        alert('You have selected seats: ' + seatNumbers.join(', '));
        // You can add code here to handle the seat selection confirmation (e.g., sending data to the server)
    });
});