document.addEventListener('DOMContentLoaded', function () {
    const documentField = document.getElementById('id_document');
    const shortenedQueryField = document.getElementById('id_shortened_query');
    const descriptionField = document.querySelector('textarea[name="description"]');
    const additionalInfoField = document.querySelector('textarea[name="additional_info"]');

    function adjustTextAreaHeight(textarea) {
        textarea.style.height = '15px';
        textarea.style.height = (textarea.scrollHeight + 2) + 'px';
    }

    shortenedQueryField.innerHTML = '<option value="">---------</option>';

    documentField.addEventListener('change', function () {
        const documentId = this.value;

        if (descriptionField) {
            descriptionField.value = '';
            adjustTextAreaHeight(descriptionField);
        }
        if (additionalInfoField) {
            additionalInfoField.value = '';
            adjustTextAreaHeight(additionalInfoField);
        }

        if (documentId) {
            fetch(`/api/get_documents/${documentId}/`)
                .then(response => response.json())
                .then(data => {

                    shortenedQueryField.innerHTML = '<option value="">---------</option>';
                    data.shortened_queries.forEach(function (shortenedQuery) {
                        const option = document.createElement('option');
                        option.value = shortenedQuery.id;
                        option.textContent = shortenedQuery.shortened_query;
                        shortenedQueryField.appendChild(option);
                    });
                });
        } else {

            shortenedQueryField.innerHTML = '<option value="">---------</option>';
        }
    });


    shortenedQueryField.addEventListener('change', function() {
        const shortenedQueryId = this.value;

        if (shortenedQueryId) {
            fetch(`/api/get_shortened_query_details/${shortenedQueryId}/`)
                .then(response => response.json())
                .then(data => {
                    if (descriptionField && additionalInfoField) {

                        descriptionField.value = data.description;
                        additionalInfoField.value = data.additional_info;

                        adjustTextAreaHeight(descriptionField);
                        adjustTextAreaHeight(additionalInfoField);
                    } else {
                        console.error('Form fields not found.');
                    }
                })
                .catch(error => {
                    console.error('Error fetching shortened query details:', error);
                });
        }
    });

    document.querySelectorAll('.auto-expand').forEach(textarea => {
        adjustTextAreaHeight(textarea);


        textarea.addEventListener('input', () => {
            adjustTextAreaHeight(textarea);
        });
    });
});
