// carrito.js

document.addEventListener('DOMContentLoaded', function() {
  const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

  addToCartButtons.forEach(button => {
      button.addEventListener('click', () => {
          const productId = button.getAttribute('data-product-id');

          fetch(`/agregar-al-carrito/${productId}/`, {
              method: 'POST',
              headers: {
                  'X-CSRFToken': getCookie('csrftoken'),
                  'Content-Type': 'application/json'
              }
          })
          .then(response => {
              if (response.ok) {
                  return response.json();
              } else {
                  throw new Error('Error al agregar producto al carrito');
              }
          })
          .then(data => {
              alert(`Producto ${data.producto_nombre} agregado al carrito.`);
          })
          .catch(error => {
              console.error('Error:', error);
              alert('Hubo un problema al agregar el producto al carrito. Inténtalo de nuevo más tarde.');
          });
      });
  });

  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
});
