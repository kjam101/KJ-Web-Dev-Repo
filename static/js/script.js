document.addEventListener('DOMContentLoaded', () => {
    console.log("Website Loaded Successfully!");

    // --- Contact Form Logic ---
    const contactForm = document.getElementById('contactForm');
    const contactFormMessage = document.getElementById('formMessage');

    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const subject = document.getElementById('subject').value.trim();
            const message = document.getElementById('message').value.trim();

            if (!name || !email || !subject || !message) {
                contactFormMessage.style.color = 'red';
                contactFormMessage.textContent = "Please fill in all required fields.";
                return;
            }

            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(email)) {
                contactFormMessage.style.color = 'red';
                contactFormMessage.textContent = "Please enter a valid email address.";
                return;
            }

            fetch('/contact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, subject, message })
            })
            .then(response => {
                if (!response.ok) throw new Error("Failed to send contact info.");
                return response.json();
            })
            .then(data => {
                contactFormMessage.style.color = 'green';
                contactFormMessage.textContent = "Thank you for contacting us!";
                contactForm.reset();
            })
            .catch(err => {
                contactFormMessage.style.color = 'red';
                contactFormMessage.textContent = err.message;
            });
        });
    }

    // --- Feedback Form Logic ---
    const stars = document.querySelectorAll('.star');
    const feedbackForm = document.getElementById('feedback-form');
    const ratingInput = document.getElementById('rating');
    const feedbackText = document.getElementById('comment');

    let selectedRating = 0;

    if (stars.length > 0) {
        stars.forEach(star => {
            star.addEventListener('click', function () {
                selectedRating = this.getAttribute('data-value');
                ratingInput.value = selectedRating; // Store selected rating in hidden input
                stars.forEach(s => s.classList.remove('selected'));
                this.classList.add('selected');
                let prev = this.previousElementSibling;
                while (prev) {
                    prev.classList.add('selected');
                    prev = prev.previousElementSibling;
                }
            });
        });
    }

    if (feedbackForm) {
        feedbackForm.addEventListener('submit', function (event) {
            // Ensure rating is saved
            ratingInput.value = selectedRating;

            if (!selectedRating) {
                event.preventDefault();
                alert("Please select a star rating.");
            }
        });
    }
});