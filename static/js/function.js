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

    if (typeof Fancybox !== "undefined") {
        Fancybox.bind("[data-fancybox]", {
            //
        });
    }

    $('#main-carousel').owlCarousel({
        items: 1,
        nav: true,
        navText: ["<i class='ph ph-caret-left'></i>", "<i class='ph ph-caret-right'></i>"],
        dots: true,
        loop: true,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: true
    });

    $('.owl-carousel').owlCarousel({
        nav: true,
        navText: ["<i class='ph ph-caret-left'></i>", "<i class='ph ph-caret-right'></i>"],
        dots: false,
        margin: 10,
        responsive: {
            0: {
                items: 2
            },
            480: {
                items: 3
            },
            768: {
                items: 4
            },
            960: {
                items: 5
            },
        }
    });
});