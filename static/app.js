$(document).ready(function() {
    $('#sort-button').click(function() {
        var selectedOptions = $('.sort-option:checked').map(function() {
            return $(this).val();
        }).get();

        var descriptionValue = $('.description-input').val();
        var genreValue = $('.genre-input').val();

        $.ajax({
            url: '/sort',
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({ 
                sortTypes: selectedOptions, 
                descriptionValue: descriptionValue, 
                genreValue: genreValue 
            }), 
            success: function(response) {
                var sortedData = response;

                // Display the sorted data vertically
                var output = '';
                for (var i = 0; i < sortedData.length; i++) {
                    output += (i + 1) + '. ' + sortedData[i] + '<br>';
                }

                $('#sorted-data').html('<h2>Sorted Releases:</h2><p>' + output + '</p>');
            }
        });
    });
});
