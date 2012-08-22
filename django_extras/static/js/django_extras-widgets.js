(function ($) {

    $(function () {
        $('input.django_extras-colorpicker').colorpicker({
            hide: function (e, ui) {
                $(this).val('#'+ui.hex);
                $('.ui-colorpicker').css('display', 'none');
            },
            submit: function (e, ui) {
                $(this).val('#'+ui.hex);
                $('.ui-colorpicker').css('display', 'none');
            }
        });
    });

})(jQuery);
