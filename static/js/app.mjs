function set_nav_current_page() {
  const data = document.querySelectorAll('[data-active-state]>li>a')
  const current_page = window.location.pathname
  data.forEach((item) => {
    if (item.getAttribute('href') === current_page) {
      item.classList.add('active')
    }
  })
}

function main() {
  set_nav_current_page()
}

$('#contact-form').submit(function (event) {
  event.preventDefault(); // Prevent default form submission

  // Collect form data
  let formData = {
    firstname: $('#firstname').val().trim(),
    lastname: $('#lastname').val().trim(),
    email: $('#email').val().trim(),
    phonenumber: $('#phonenumber').val().trim(),
    message: $('#message').val().trim()
  };

  // Send AJAX request
  $.ajax({
    url: '/api/v1/contact',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(formData),
    success: function (response) {
      alert('Message sent successfully!');
      $('#contact-form')[0].reset(); // Clear the form
    },
    error: function (xhr, status, error) {
      alert('Error sending message. Please try again.');
      console.error('Error:', error);
    }
  });
});

document.addEventListener('DOMContentLoaded', main)