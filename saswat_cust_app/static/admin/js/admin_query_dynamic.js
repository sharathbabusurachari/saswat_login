(function($) {
    $(document).ready(function() {
        $('#id_shortened_query').change(function() {
            var queryId = $(this).val();
            if (queryId) {
                $.ajax({
                    url: 'query-data/' + queryId + '/',
                    method: 'GET',
                    success: function(data) {
                        $('#id_description').val(data.description);
                        $('#id_additional_info').val(data.additional_info);
                    }
                });
            }
        });
    });
})(django.jQuery);