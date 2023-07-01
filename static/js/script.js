// Bootstrap colors in RGB
const bootstrapColors = {
    primary: 'rgb(13, 110, 253)',
    secondary: 'rgb(108, 117, 125)',
    success: 'rgb(25, 135, 84)',
    danger: 'rgb(220, 53, 69)',
    warning: 'rgb(255, 193, 7)',
    info: 'rgb(13, 202, 240)',
    light: 'rgb(248, 249, 250)',
}

// ___MAIN FUNCTIONALITY___
$(document).ready(function () {
    let windowWidth = window.innerWidth;

    // init dropdown menu
    let dropdown = initDropdown();

    // init and show toast messages if they exist
    let toastElementsList = [].slice.call(document.querySelectorAll('.default-msg-toast'))
    showToasts(toastElementsList);
    // init and show messages Modal if it exists
    $('#messagesModal').modal('show');

    // init tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })


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

    backToTop();

    insertRoleToTitle();
    $("#signup_form input:radio").on('change', function () {
        insertRoleToTitle();
    }
    );

    // event listener for logout link
    $('#logout-link').click(function (e) {
        e.preventDefault();
        $('#logoutModal').modal('show');
    });

    // event listener for resume close button
    $('.resume-close-btn').click(function (e) {
        setResumeActionModal(e, 'close');
    });
    // event listener for resume delete button
    $('.resume-delete-btn').click(function (e) {
        setResumeActionModal(e, 'delete');
    });

    // event listener for submit of save form
    $('.save-job-form').submit(toggleSaveResume);

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

/**
 * Back to top button.
 * Triggered by click event on `.back-to-top` element
 */
function backToTop() {
    // scroll body to 0px on click
    $('.back-to-top').click(function () {
        $('body,html').animate({
            scrollTop: 0
        }, 200);
        return false;
    });
}

/**
 * Insert selected role to the title of the Sign Up form.
 */
function insertRoleToTitle() {
    selected_value = $("input[name='role']:checked").val();
    let jobseeker = `as a
    <span class="text-royalpurple">Jobseeker</span>`;
    let employer = `as an
    <span class="text-cyan-blue">Employer</span>`;
    if (selected_value == "JOBSEEKER") {
        $('#role-title').html(jobseeker);
    } else if (selected_value == "EMPLOYER") {
        $('#role-title').html(employer);
    }
}

/**
 * Initialize and show Bootstrap toasts.
 */
function showToasts(toastElementsList, toastBootstrapColor) {
    var toastList = toastElementsList.map(function (toastEl) {

        return new bootstrap.Toast(toastEl)
    })

    changeToastsColor(toastElementsList, toastBootstrapColor);
    // show toast by default
    toastList.forEach(toast => toast.show())
}

/**
 * Change `toast::after` bg color based on passed toastBootstrapColor or
 * `data-msg-tag` attribute. It takes name of bootstrap color as a string,
 * searches for it in bootstrapColors object and sets rgb color to css variable.
 */
function changeToastsColor(toastElList, toastBootstrapColor) {
    // change `toast::after` bg color based on `data-msg-tag` attribute
    toastElList.forEach(toast => {
        let bootstrapColor;
        if (toastBootstrapColor) {
            bootstrapColor = toastBootstrapColor;
        } else {
            // get data-msg-tag attribute value
            bootstrapColor = toast.getAttribute('data-msg-tag');
        }
        // set default color if bootstrapColor is undefined
        // ?? - Nullish coalescing operator
        let rgbColor = bootstrapColors[bootstrapColor] ?? bootstrapColors['light'];
        // set css variable
        toast.style.setProperty('--toast-bg-color', rgbColor);
    }
    );
}

/**
 * Set resume modal form action url and modal action text by
 * clicking on `Close/Delete` button.
 */
function setResumeActionModal(event, actionText) {
    event.preventDefault();
    let actionUrl = event.target.dataset.resumeActionUrl;
    $('#modal-action').text(actionText);
    $('#resume-modal-form').attr('action', actionUrl);
    $('#resumeModal').modal('show');
}
