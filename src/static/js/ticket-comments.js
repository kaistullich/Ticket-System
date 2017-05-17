$(document).ready(function () {
    // Get Name of the user
    var custName = $('#first-name').text();

    // On click of button
    $('form').on('submit', function (event) {
        // Grab `box` ID
        var divBox = document.getElementById("box");
        // Auto scroll when messages exceed the height of the box
        divBox.scrollTop = divBox.scrollHeight;
        // Grab input entered
        var comment = $('#comment').val();

        // Start AJAX
        $.ajax({
            data: {
                comment: comment
            },
            type: 'POST',
            url: '/process_comments'
        // On success of AJAX call
        }).done(function (data) {
            // Clear the textarea after new comment submitted
            $('#comment').val('');
            if (data.error) {
                console.log(data.error);
            } else {
                // Append the message entered TODO: this will need to be the DB messages; static for now
                console.log('SUCCESS');
                $('#comment-append').append('<div class="msg_bubble"><strong>' + custName +': </strong>' + comment + '</div>');
            }
        });
        event.preventDefault();
    });
}); // END $.ready()