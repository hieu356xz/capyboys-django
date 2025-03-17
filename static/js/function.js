$(document).ready(function() {
    $("#add-to-cart-btn-decrease").click(function() {
        let quantity = parseInt($("#add-to-cart-quantity").val());
        if (quantity > 1) {
            $("#add-to-cart-quantity").val(quantity - 1);
        }
    });

    $("#add-to-cart-btn-increase").click(function() {
        let quantity = parseInt($("#add-to-cart-quantity").val());
        if (quantity < 99) {
            $("#add-to-cart-quantity").val(quantity + 1);
        }
    }); 

    $("#add-to-cart-quantity").on("input" ,function() {
        let quantity = parseInt($("#add-to-cart-quantity").val());
        
        if (quantity < 1 || isNaN(quantity)) {
            $("#add-to-cart-quantity").val(1);
        } else if (quantity > 99) {
            $("#add-to-cart-quantity").val(99);
        }
    });

    $('.content-filter-btn').click(function() {
        let container = $(this).next(".content-filter-container")
        let hidden = container.attr("hidden");
        if (hidden) {
            container.removeAttr("hidden");
        } else {
            container.attr("hidden", "");
        }
    });
});