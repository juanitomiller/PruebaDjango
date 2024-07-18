document.addEventListener("DOMContentLoaded", function() {
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

    const carritoCountElement = document.getElementById('carrito-count');
    const carritoTableBody = document.querySelector('#carrito-table tbody');
    const totalGeneralElement = document.getElementById('total-general');

    function actualizarCarrito(carrito_items, total) {
        carritoTableBody.innerHTML = ''; // Limpiar el contenido del tbody antes de actualizar
        carrito_items.forEach(item => {
            carritoTableBody.innerHTML += `
                <tr data-product-id="${item.id}">
                    <td>${item.name}</td>
                    <td>$${item.price.toFixed(2)}</td>
                    <td>
                        <button class="decrease-quantity-btn" data-product-id="${item.id}">-</button>
                        <span class="quantity">${item.quantity}</span>
                        <button class="increase-quantity-btn" data-product-id="${item.id}">+</button>
                    </td>
                    <td>$${(item.price * item.quantity).toFixed(2)}</td>
                    <td>
                        <button class="eliminar-producto-btn" data-product-id="${item.id}">Eliminar</button>
                    </td>
                </tr>`;
        });
        carritoCountElement.textContent = carrito_items.length;
        totalGeneralElement.textContent = `Total: $${total.toFixed(2)}`;
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

    // Función para aumentar la cantidad de un producto en el carrito
    function aumentarCantidad(producto_id) {
        fetch(`/increase-quantity/${producto_id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const quantityElement = document.querySelector(`tr[data-product-id="${producto_id}"] .quantity`);
                quantityElement.textContent = data.quantity;
                // Actualizar el carrito después de aumentar la cantidad
                fetch('/get-cart/')
                .then(response => response.json())
                .then(data => {
                    actualizarCarrito(data.carrito_items, data.total);
                });
            } else {
                console.error('Error al aumentar la cantidad del producto');
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Función para disminuir la cantidad de un producto en el carrito
    function disminuirCantidad(producto_id) {
        fetch(`/decrease-quantity/${producto_id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const quantityElement = document.querySelector(`tr[data-product-id="${producto_id}"] .quantity`);
                if (data.quantity > 0) {
                    quantityElement.textContent = data.quantity;
                } else {
                    // Eliminar la fila del producto si la cantidad es 0
                    document.querySelector(`tr[data-product-id="${producto_id}"]`).remove();
                }
                // Actualizar el carrito después de disminuir la cantidad
                fetch('/get-cart/')
                .then(response => response.json())
                .then(data => {
                    actualizarCarrito(data.carrito_items, data.total);
                });
            } else {
                console.error('Error al disminuir la cantidad del producto');
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function vaciarCarrito() {
        fetch('/vaciar-carrito/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Actualizar la interfaz del carrito después de vaciarlo
                carritoTableBody.innerHTML = '';
                carritoCountElement.textContent = '0';
                totalGeneralElement.textContent = 'Tu carrito está vacío.';
            } else {
                console.error('Error al vaciar el carrito');
            }
        })
        .catch(error => console.error('Error:', error));
    }


    // Evento para manejar el clic en el botón de eliminar producto del carrito
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('eliminar-producto-btn')) {
            const producto_id = event.target.dataset.productId;
            eliminarProducto(producto_id);
        }

        if (event.target.classList.contains('increase-quantity-btn')) {
            const producto_id = event.target.dataset.productId;
            aumentarCantidad(producto_id);
        }

        if (event.target.classList.contains('decrease-quantity-btn')) {
            const producto_id = event.target.dataset.productId;
            disminuirCantidad(producto_id);
        }

        if (event.target.classList.contains('vaciar-carrito-btn')) {
            vaciarCarrito();
        }
    });
});
