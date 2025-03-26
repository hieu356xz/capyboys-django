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
        autoHeightAnimate(container, 300, $(this));
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

    // By Josh Parrett https://codepen.io/JTParrett/pen/nJNXxX
    function autoHeightAnimate(element, time, triggerBtn) {
        triggerBtn.click(function() {
            if (element.height() === 0) {
                let curHeight = element.height(), // Get Default Height
                autoHeight = element.css('height', 'auto').height(); // Get Auto Height
    
                element.height(curHeight); // Reset to Default Height
                element.stop().animate({ height: autoHeight }, parseInt(time)); // Animate to Auto Height
            }
            else {
                element.stop().animate({ height: '0' }, parseInt(time)); // Animate to 0 Height
            }
        });
    }
});