document.addEventListener("DOMContentLoaded", function() {
    const reviewForm = document.getElementById('review-form');
    const reviewsContainer = document.getElementById('reviews-container');

    reviewForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const rating = document.getElementById('rating').value;
        const comment = document.getElementById('comment').value;

        const reviewElement = document.createElement('div');
        reviewElement.classList.add('card', 'mb-3');
        reviewElement.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">Rating: ${rating}</h5>
                <p class="card-text">${comment}</p>
                <p class="card-text"><small class="text-muted">Just now</small></p>
            </div>
        `;

        reviewsContainer.prepend(reviewElement);

        reviewForm.reset();
    });
});