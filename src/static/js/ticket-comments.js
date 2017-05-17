$(document).ready(function () {
    // Get Name of the user
    var custName = $('#first-name').text();

    // On submit of form
    $('form').on('submit', function (event) {
        // Grab `box` ID
        var divBox = document.getElementById("box");
        // Auto scroll when messages exceed the height of the box
        divBox.scrollTop = divBox.scrollHeight;
        // Grab input entered in textarea
        var comment = $('#comment').val();

        // AJAX request
        $.ajax({
            data: {
                comment: comment
            },
            type: 'POST',
            url: '/process_comments'
        // On success of AJAX request
        }).done(function (data) {
            // Clear the textarea after new comment submitted
            $('#comment').val('');
            // If error occurred
            if (data.error) {
                console.log(data.error);
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