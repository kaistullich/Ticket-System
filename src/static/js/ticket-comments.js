$(document).ready(function () {
    // Get Name of the user
    var custName = $('#first-name').text();

    $('form').on('submit', function (event) {
        var divBox = $("#box");
        divBox.scrollTop = divBox.scrollHeight;
        var comment = $('#comment').val();

        // AJAX request
        $.ajax({
            data: {
                comment: comment
            },
            type: 'POST',
            url: '/process_comments'
        }).done(function (data) {
            $('#comment').val('');
            // If error occurred
            if (data.error) {
                window.scrollTo(0,0);
                $('#errorAlert').text('An unexpected error occurred, please try again!').show();
            // Success
            } else {
                // Append the message entered
                $('#comment-append').append('<div class="msg_bubble"><strong>' + custName +': </strong>' + comment + '</div>');
            }
        }); // END .done()
        // Prevent default form submission event
        event.preventDefault();
    }); // END $('form')
}); // END $.ready()