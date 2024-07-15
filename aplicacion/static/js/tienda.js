$(document).ready(function(){
  $('.add-to-cart-btn').click(function(){
      let productId = $(this).data('product-id');
      addToCart(productId);
  });

  function addToCart(productId) {
      fetch(`/add-to-cart/${productId}/`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({
              'product_id': productId
          })
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              // Aquí puedes actualizar el contador del carrito u otra acción
              updateCartCount();
          } else {
              console.error('Error al agregar al carrito');
          }
      })
      .catch(error => console.error('Error:', error));
  }

  function updateCartCount() {
      // Implementa la lógica para actualizar el contador del carrito
      // Por ejemplo, puedes hacer una solicitud a tu backend para obtener el número actual de productos en el carrito
      // y actualizar el contador en el frontend sin mostrar una alerta
      console.log('Producto agregado al carrito sin alerta');
  }

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
