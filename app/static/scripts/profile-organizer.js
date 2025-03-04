document.addEventListener('DOMContentLoaded', function () {
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

    // Functionality for the Edit Profile button
    document.getElementById('editProfileBtn').addEventListener('click', function () {
        // Enable editing of profile fields
        document.getElementById('organizer-name').removeAttribute('readonly');
        document.getElementById('email').removeAttribute('readonly');
        document.getElementById('description').removeAttribute('readonly');
        document.getElementById('phone').removeAttribute('readonly');
        
        // Show the Save and Cancel buttons
        document.getElementById('editProfileBtn').style.display = 'none';
        document.getElementById('submitProfileBtn').style.display = 'inline-block';
        document.getElementById('cancelEditProfileBtn').style.display = 'inline-block';
    });

    document.getElementById('cancelEditProfileBtn').addEventListener('click', function () {
        // Disable editing of profile fields
        document.getElementById('organizer-name').setAttribute('readonly', true);
        document.getElementById('email').setAttribute('readonly', true);
        document.getElementById('description').setAttribute('readonly', true);
        document.getElementById('phone').setAttribute('readonly', true);

        // Hide the Save and Cancel buttons
        document.getElementById('editProfileBtn').style.display = 'inline-block';
        document.getElementById('submitProfileBtn').style.display = 'none';
        document.getElementById('cancelEditProfileBtn').style.display = 'none';
    });

    // Functionality for the Change Password button
    document.getElementById('changePasswordBtn').addEventListener('click', function () {
        // Empty the current password field and rename it
        const currentPasswordField = document.getElementById('current-password');
        currentPasswordField.value = '';
        currentPasswordField.setAttribute('placeholder', 'Current Password');

        // Show the new password and confirm password fields
        document.getElementById('new-password-fields').style.display = 'block';
        document.getElementById('confirm-password-fields').style.display = 'block';
        document.getElementById('submitPasswordBtn').style.display = 'inline-block';
        document.getElementById('cancelChangePasswordBtn').style.display = 'inline-block';

        // Hide the Change Password button
        document.getElementById('changePasswordBtn').style.display = 'none';
    });

    document.getElementById('cancelChangePasswordBtn').addEventListener('click', function () {
        // Hide the new password and confirm password fields
        document.getElementById('new-password-fields').style.display = 'none';
        document.getElementById('confirm-password-fields').style.display = 'none';
        document.getElementById('submitPasswordBtn').style.display = 'none';
        document.getElementById('cancelChangePasswordBtn').style.display = 'none';

        // Show the Change Password button
        document.getElementById('changePasswordBtn').style.display = 'inline-block';
    });
});