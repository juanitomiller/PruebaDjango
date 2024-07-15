document.addEventListener("DOMContentLoaded", function() {
    const carritoCountElement = document.getElementById('carrito-count');
    const carritoDropdown = document.getElementById('carrito-dropdown');
    const totalGeneralElement = document.getElementById('total-general');

    function actualizarCarrito(carrito_items, total) {
        carritoDropdown.innerHTML = ''; // Limpiar el contenido del dropdown antes de actualizar
        carrito_items.forEach(item => {
            carritoDropdown.innerHTML += `<li>${item.name} - $${item.price} x ${item.quantity}</li>`;
        });
        carritoCountElement.textContent = carrito_items.length;
        totalGeneralElement.textContent = `Total: $${total}`;
    }

    // Obtener el contenido inicial del carrito desde el servidor al cargar la página
    fetch('/get-cart/')
    .then(response => response.json())
    .then(data => {
        if (data.carrito_items.length > 0) {
            actualizarCarrito(data.carrito_items, data.total);
        } else {
            carritoCountElement.textContent = '0';
            totalGeneralElement.textContent = 'Tu carrito está vacío.';
        }
    })
    .catch(error => console.error('Error:', error));

    // Función para eliminar un producto del carrito
    function eliminarProducto(producto_id) {
        fetch(`/remove-from-cart/${producto_id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                actualizarCarrito(data.carrito_items, data.total);
            } else {
                console.error('Error al eliminar producto del carrito');
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Evento para manejar el clic en el botón de eliminar producto del carrito
    carritoDropdown.addEventListener('click', function(event) {
        if (event.target.tagName === 'LI') {
            const producto_id = event.target.dataset.productId;
            eliminarProducto(producto_id);
        }
    });

    // Función auxiliar para obtener el valor de una cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
