//Revealing Module Pattern
$("#slider-vertical").slider({
    orientation: "vertical",
    range: "min",
    min: 0,
    max: 100,
    value: 60,
    slide: function(event, ui) {
        console.log("previous value:" + $(this).slider('option', 'value'));
    },
    stop: function(event, ui) {
        console.log("Current value:" + $(this).slider('option', 'value'));
    }
});


var Dropdown = (function($) {

    var $body = $('body'),
        $dropdown = $body.find('.m-button'),
        $trigger = $dropdown.find('button'),
        $list = $dropdown.find('ul'),
        $firstLink = $list.find('li:first a'),
        $lastLink = $list.find('li:last a');

    var init = function() {
        ariaSetup();
        bindEvents();
    }

    var ariaSetup = function() {
        var listId = $list.attr('id');

        $trigger.attr({
            'aria-expanded': 'false',
            'aria-controls': listId
        });

        $list.attr({
            'aria-hidden': true
        });
    }

    var bindEvents = function() {
        $trigger.on('click', toggleDropdown);

        $firstLink.on('keydown', function() {
            if (event.which === 9 && event.shiftKey === false) {
                return;
            } else if (event.which === 9 && event.shiftKey === true) {
                toggleDropdown();
            }
        });

        $lastLink.on('keydown', function() {
            if (event.shiftKey) return;
            toggleDropdown();
        });
    }

    var toggleDropdown = function() {
        var $this = $(event.target),
            hidden = $list.attr('aria-hidden') === 'true' ? false : true,
            expanded = !hidden;

        $this.attr('aria-expanded', expanded);
        $this.next('ul').attr('aria-hidden', hidden);
    }

    return {
        init: init
    }

})(jQuery);

Dropdown.init();