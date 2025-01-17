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

    // Alert placeholders for buttons
    document.getElementById('editProfileBtn').addEventListener('click', function () {
        alert('Profile editing functionality coming soon!');
    });

    document.getElementById('changePasswordBtn').addEventListener('click', function () {
        alert('Password change functionality coming soon!');
    });
});
