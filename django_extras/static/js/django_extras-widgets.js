(function ($) {

    $(function () {
        $('input.django_extras-colorpicker').colorPicker({
            color: '#fff',
            onSubmit: function(hsb, hex, rgb, el) {
                $(el).val('#'+hex);
                $(el).colorPickerHide();
            },
            onBeforeShow: function () {
                $(this).colorPickerSetColor(this.value);
            }
        });
    });

})(jQuery || django.jQuery);
