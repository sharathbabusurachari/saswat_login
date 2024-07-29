document.addEventListener('DOMContentLoaded', function () {
    const documentField = document.getElementById('id_document');
    const shortenedQueryField = document.getElementById('id_shortened_query');

    documentField.addEventListener('change', function () {
        const documentId = this.value;

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
});