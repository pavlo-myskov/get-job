$(document).ready(function () {
    let windowWidth = window.innerWidth;

    // init dropdown menu
    let dropdown = initDropdown();

    hideShowNavbar(windowWidth, dropdown);
    fixDaysCounterPosition(windowWidth);
    fixCardImagePosition(windowWidth);
    addRemoveCollapseClass(windowWidth);
    ageSlider();

    // restart functions on windows resize
    $(window).resize(function () {
        windowWidth = window.innerWidth;
        hideShowNavbar(windowWidth, dropdown);
        fixDaysCounterPosition(windowWidth);
        fixCardImagePosition(windowWidth);
        addRemoveCollapseClass(windowWidth);
    });

});


/**
 * Init dropdown menu if it exists.
 * Add event listener to dropdown menu that adds 'shown' class to dropdown element
 * when dropdown menu is shown.
 * @returns {bootstrap.Dropdown}
 */
function initDropdown() {
    let dropdown;
    let dropdownEl = document.getElementById('navbar--dropdown');
    let dropdownToggle = document.querySelector('#navbar--dropdown .dropdown-toggle');
    if (dropdownToggle) {
        dropdown = new bootstrap.Dropdown(dropdownToggle);
        dropdownEl.addEventListener('show.bs.dropdown', function () {
            this.classList.add('shown');
        })
    }

    return dropdown;
}

/**
 * - Hide/show navbar on scroll up/down if screen width is less than 768px.
 * - Hide dropdown menu on scroll down.
 *
 * Based on the following example:
 * https://bootstrap-menu.com/_bootstrap4/detail-smart-hide.html
 */
function hideShowNavbar(windowWidth, dropdown) {

    // if width is less than 768px activate smart scroll
    if (windowWidth < 768) {
        // add smart scroll that fixes the navbar
        $('.navbar').addClass('smart-scroll');
        // add padding top to show content behind navbar
        $('body').css('padding-top', $('.navbar').outerHeight() + 'px')
        let last_scroll_top = 0;

        // add scroll event handler that detects scroll up/down
        $(window).on('scroll', function () {
            let scroll_top = $(this).scrollTop();
            if (scroll_top < last_scroll_top) {
                $('.smart-scroll').removeClass('scrolled-down').addClass('scrolled-up');
            }
            else {
                // add scrolled-down class that hides the navbar
                $('.smart-scroll').removeClass('scrolled-up').addClass('scrolled-down');
                // hide dropdown menu if it exists and is open
                if (dropdown && $('#navbar--dropdown').hasClass('shown')) {
                    dropdown.hide();
                    $('#navbar--dropdown').removeClass('shown');
                }
            }
            last_scroll_top = scroll_top;
        });
    } else {
        $('.smart-scroll').removeClass('scrolled-up').removeClass('scrolled-down');
        // remove scroll event handler for screens larger than 768px
        $(window).off('scroll');
        // remove smart scroll that fixes the navbar
        $('.navbar').removeClass('smart-scroll');
        // remove padding top from body
        $('body').css('padding-top', '0');
    }
}

/**
 * Fix absolute position of days counter for mobile devices
 * Days counter is located on every card.
 */
function fixDaysCounterPosition(windowWidth) {
    if (windowWidth > 575) {
        $('.days-counter').removeClass('card-subtitle').addClass('position-absolute top-0 end-0 pt-2 pe-3')
    } else {
        $('.days-counter').removeClass('position-absolute top-0 end-0 pt-2 pe-3').addClass('card-subtitle')
    }
}

/**
 * Fix absolute position of card image for mobile devices
 */
function fixCardImagePosition(windowWidth) {
    if (windowWidth < 576) {
        $('.resume-card--img').css('max-height', '50px').addClass('position-absolute top-0 end-0 pt-2')
    } else {
        $('.resume-card--img').css('max-height', '70px').removeClass('position-absolute top-0 end-0 pt-2')
    }
}


/**
 * Add/remove collapse class to search panel based on screen width.
 */
function addRemoveCollapseClass(windowWidth) {
    if (windowWidth < 992) {
        $('#search-panel').addClass('collapse');
    } else {
        $('#search-panel').removeClass('collapse');
    }
}

/**
 * jQuery age range slider
 */
function ageSlider() {
    $("#slider-range").slider({
        range: true,
        min: 18,
        max: 66,
        values: [$("#min-age").val(), $("#max-age").val()],
        slide: function (event, ui) {
            let minValue = ui.values[0];
            let maxValue = ui.values[1];

            // update input hidden form fields
            $("#min-age").val(minValue);
            $("#max-age").val(maxValue);

            // if min and max values are equal, leave only one value
            if (minValue == maxValue) {
                // update input decorative field
                if (maxValue === 66) {
                    // set decorative value to "65+" if max value is 66
                    maxValue = "65+";
                }

                $("#age-amount").val(maxValue);
            } else {
                // update input decorative field
                if (maxValue === 66) {
                    // set decorative value to "65+" if max value is 66
                    maxValue = "65+";
                }

                $("#age-amount").val(minValue + " - " + maxValue);
            }
        }
    });

    // set initial values
    let minValue = $("#slider-range").slider("values", 0);
    let maxValue = $("#slider-range").slider("values", 1);

    // update input hidden form fields
    $("#min-age").val(minValue);
    $("#max-age").val(maxValue);

    // if min and max values are equal, leave only one value
    if (minValue == maxValue) {
        // update input decorative field
        if (maxValue === 66) {
            // set decorative value to "65+" if max value is 66
            maxValue = "65+";
        }

        $("#age-amount").val(maxValue);
    } else {
        // update input decorative field
        if (maxValue === 66) {
            // set decorative value to "65+" if max value is 66
            maxValue = "65+";
        }

        $("#age-amount").val(minValue + " - " + maxValue);
    }
}