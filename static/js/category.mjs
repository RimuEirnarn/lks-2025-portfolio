function init() {
  const csrf = document.querySelector("html").getAttribute('data-csrf')
  document.querySelectorAll("[data-id]").forEach(element => {
    const id = element.getAttribute('data-id')
    element.addEventListener("click", () => {
      $.ajax({
    url: `/category/${id}`,
    type: 'DELETE',
    contentType: 'application/formdata',
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
    })
  })
}