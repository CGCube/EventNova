document.addEventListener("DOMContentLoaded", function() {
    const editProfileBtn = document.getElementById("editProfileBtn");
    const submitProfileBtn = document.getElementById("submitProfileBtn");
    const cancelEditProfileBtn = document.getElementById("cancelEditProfileBtn");
    const profileForm = document.getElementById("profile-form");

    const changePasswordBtn = document.getElementById("changePasswordBtn");
    const submitPasswordBtn = document.getElementById("submitPasswordBtn");
    const cancelChangePasswordBtn = document.getElementById("cancelChangePasswordBtn");
    const passwordForm = document.getElementById("change-password-form");

    const navLinks = document.querySelectorAll('.sticky-sidebar .nav-link');
    const sections = document.querySelectorAll("div[id$='-section']");

    // Function to handle the mouse move event
    const handleMouseMove = (e) => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionBottom = sectionTop + section.offsetHeight;

            // Check if the cursor is within the section's bounds
            if (e.pageY >= sectionTop && e.pageY <= sectionBottom) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').substring(1) === current) {
                link.classList.add('active');
            }
        });
    };

    // Listen for mousemove events
    document.addEventListener('mousemove', handleMouseMove);

    // Function to toggle profile edit mode
    function toggleProfileEditMode(editable) {
        profileForm.querySelectorAll("input, textarea").forEach(input => {
            input.readOnly = !editable;
        });
        editProfileBtn.style.display = editable ? "none" : "inline-block";
        submitProfileBtn.style.display = editable ? "inline-block" : "none";
        cancelEditProfileBtn.style.display = editable ? "inline-block" : "none";
    }

    // Function to toggle password change mode
    function togglePasswordChangeMode(editable) {
        passwordForm.querySelectorAll("input").forEach(input => {
            input.readOnly = !editable;
        });
        document.getElementById("new-password-fields").style.display = editable ? "block" : "none";
        document.getElementById("confirm-password-fields").style.display = editable ? "block" : "none";
        changePasswordBtn.style.display = editable ? "none" : "inline-block";
        submitPasswordBtn.style.display = editable ? "inline-block" : "none";
        cancelChangePasswordBtn.style.display = editable ? "inline-block" : "none";
    }

    // Event listener for edit profile button
    editProfileBtn.addEventListener("click", function() {
        toggleProfileEditMode(true);
    });

    // Event listener for cancel edit profile button
    cancelEditProfileBtn.addEventListener("click", function() {
        toggleProfileEditMode(false);
    });

    // Event listener for profile form submit
    profileForm.addEventListener("submit", function(event) {
        event.preventDefault();
        // Perform AJAX request to update profile
        fetch("/update_profile", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                organizer_id: profileForm.elements["organizer_id"].value,
                name: profileForm.elements["name"].value,
                email: profileForm.elements["email"].value,
                description: profileForm.elements["description"].value,
                phone: profileForm.elements["phone"].value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                toggleProfileEditMode(false);
                alert("Profile updated successfully.");
            } else {
                alert("Failed to update profile.");
            }
        });
    });

    // Event listener for change password button
    changePasswordBtn.addEventListener("click", function() {
        togglePasswordChangeMode(true);
    });

    // Event listener for cancel change password button
    cancelChangePasswordBtn.addEventListener("click", function() {
        togglePasswordChangeMode(false);
    });

    // Event listener for password form submit
    passwordForm.addEventListener("submit", function(event) {
        event.preventDefault();
        // Perform AJAX request to change password
        fetch("/change_password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                current_password: passwordForm.elements["current_password"].value,
                new_password: passwordForm.elements["new_password"].value,
                confirm_password: passwordForm.elements["confirm_password"].value
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                togglePasswordChangeMode(false);
                alert("Password changed successfully.");
            } else {
                alert(data.message || "Failed to change password.");
            }
        });
    });

    // Fetch profile data and populate form
    fetch("/get_profile")
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                profileForm.elements["organizer_id"].value = data.profile.organizer_id;
                profileForm.elements["name"].value = data.profile.name;
                profileForm.elements["email"].value = data.profile.email;
                profileForm.elements["description"].value = data.profile.description;
                profileForm.elements["phone"].value = data.profile.phone;
                profileForm.elements["username"].value = data.profile.organizer_id; // Assuming organizer_id is used as the username
            } else {
                alert("Failed to fetch profile data.");
            }
        });

    // Fetch order history and populate list
    fetch("/get_order_history")
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const orderHistoryList = document.getElementById("order-history-list");
                orderHistoryList.innerHTML = "";
                data.orders.forEach(order => {
                    const listItem = document.createElement("li");
                    listItem.classList.add("list-group-item");
                    listItem.innerHTML = `<strong>${order.type}:</strong> ${order.name} | <strong>Date:</strong> ${order.date}`;
                    orderHistoryList.appendChild(listItem);
                });
            } else {
                alert("Failed to fetch order history.");
            }
        });

    // Event listener for logout button
    document.getElementById("logoutBtn").addEventListener("click", function(event) {
        event.preventDefault();
        fetch("/logout", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = "/login";
            } else {
                alert("Failed to log out.");
            }
        });
    });
});