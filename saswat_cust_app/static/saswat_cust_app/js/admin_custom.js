document.addEventListener('DOMContentLoaded', function() {
    const shortenedQuerySelect = document.querySelector('select[name="shortened_query"]');
    if (shortenedQuerySelect) {
        shortenedQuerySelect.addEventListener('change', function() {
            const shortenedQueryId = this.value;
            if (shortenedQueryId) {
                fetch(`/api/get_shortened_query_details/${shortenedQueryId}/`)
                    .then(response => response.json())
                    .then(data => {
                        const descriptionField = document.querySelector('input[name="description"]');
                        const additionalInfoField = document.querySelector('input[name="additional_info"]');
                        descriptionField.value = data.description;
                        additionalInfoField.value = data.additional_info;
                    })
                    .catch(error => {
                        console.error('Error fetching shortened query details:', error);
                    });
            }
        });
    }
});
