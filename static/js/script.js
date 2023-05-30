/* Hide navbar on scroll down
https://bootstrap-menu.com/_bootstrap4/detail-smart-hide.html
*/

// add padding top to show content behind navbar
$('body').css('padding-top', $('.navbar').outerHeight() + 'px')

// detect scroll top or down
if ($('.smart-scroll').length > 0) { // check if element exists
    let last_scroll_top = 0;
    $(window).on('scroll', function() {
        scroll_top = $(this).scrollTop();
        if(scroll_top < last_scroll_top) {
            $('.smart-scroll').removeClass('scrolled-down').addClass('scrolled-up');
            // hide dropdown menu if it is open
        }
        else {
            $('.smart-scroll').removeClass('scrolled-up').addClass('scrolled-down');

        }
        last_scroll_top = scroll_top;
    });
}