$(document).ready(function() {
    $('.content-filter-btn').click(function() {
        let triggerBtn = $(this);
        let container = triggerBtn.next(".content-filter-container")
        autoHeightAnimate(container, 300, 
            function() {
                triggerBtn.attr("data-state", "open");
            },
            function() {
                triggerBtn.attr("data-state", "closed");
            }
        );
    });

    $('#checkout-cart-info-btn').click(function() {
        let container = $(this).next("#checkout-cart-info-container")
        let icon = $(this).find("#checkout-cart-info-icon")
        autoHeightAnimate(container, 300, 
            function() {
                icon.css("transform", "rotate(180deg)");
            },
            function() {
                icon.css("transform", "rotate(0deg)");
            }
        );
    });

    $('#sidebar-open-btn, #sidebar-close-btn, #sidebar-overlay').on('click', function() {
        let sidebarOverlay = $('#sidebar-overlay');
        let sidebar = $('#sidebar-container');
        if (sidebar.hasClass('active')) {
            sidebarOverlay.removeClass('active');
            sidebar.removeClass('active');
        }
        else {
            sidebarOverlay.addClass('active');
            sidebar.addClass('active');
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

    // By Josh Parrett https://codepen.io/JTParrett/pen/nJNXxX
    function autoHeightAnimate(element, time, callbackOpen, callbackClose) {
        if (Math.round(element.height()) === 0) {
            let curHeight = element.height(), // Get Default Height
            autoHeight = element.css('height', 'auto').height(); // Get Auto Height

            element.height(curHeight); // Reset to Default Height
            if (callbackOpen) callbackOpen();
            element.filter(':not(:animated)').animate({ height: autoHeight }, parseInt(time)); // Animate to Auto Height
        }
        else {
            if (callbackClose) callbackClose();
            element.filter(':not(:animated)').animate({ height: '0' }, parseInt(time)); // Animate to 0 Height
        }
    }

    $("#sorter").change(function() {
        let url = new URL(window.location.href);
        url.searchParams.set("order", $(this).val());
        window.location.href = url.href;
    });

    $("#user-popup-btn").click(function() {
        let popupContainer = $(this).next();
        let display = popupContainer.css("display")
        if (display !== "flex") {
            popupContainer.css({ display: "flex" });
        } else {
            popupContainer.css({ display: "none" });
        }
    });

    $("#cart-btn").click(function() {
        $("#cart-modal").toggle();
    });

    $(document).on("click", ".modal-container__close-btn", function() {
        $(this).closest('.modal-container').toggle();
    });
});