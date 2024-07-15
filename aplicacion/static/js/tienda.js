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
                updateCartCount();
            } else {
                console.error('Error al agregar al carrito');
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function updateCartCount() {
        fetch('/get-cart-count/')
        .then(response => response.json())
        .then(data => {
            const cartCountElement = document.getElementById('carrito-count');
            cartCountElement.textContent = data.cart_count;
        })
        .catch(error => console.error('Error:', error));
    }

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
