$(document).ready(function () {
    $('.add-to-cart').click(function () {
        var productId = $(this).data('id');

        $.ajax({
            url: '/cart/add/' + productId,
            type: 'POST',
            success: function (response) {
                if (response.success) {
                    alert('Product added to cart!');
                } else {
                    alert('Failed to add product to cart.');
                }
            },
            error: function () {
                alert('Error occurred while adding product to cart.');
            }
        });
    });
    $('#pay-button').click(function () {
        $.ajax({
            url: '/pay',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ amount: total }),
            success: function (response) {
                if (response.success) {
                    window.location.href = response.url; // Перенаправление на страницу оплаты
                } else {
                    alert('Payment failed: ' + response.error);
                }
            },
            error: function () {
                alert('Error occurred while processing payment.');
            }
        });
    });
});
