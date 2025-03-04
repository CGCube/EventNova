document.querySelectorAll('.dropdown-item').forEach(function(item) {
    item.addEventListener('click', function() {
        var button = document.getElementById('dropdownMenuButton');
        var hiddenInput = document.getElementById('dropdownSelection');
        button.textContent = this.textContent;
        hiddenInput.value = this.getAttribute('data-value');
    });
});

document.getElementById('loginForm').addEventListener('submit', function(event) {
    var hiddenInput = document.getElementById('dropdownSelection');
    if (!hiddenInput.value) {
        alert('Please select an option from the dropdown.');
        event.preventDefault();
    }
});