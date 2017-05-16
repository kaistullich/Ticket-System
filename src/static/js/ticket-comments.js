$(document).ready(function () {
    // Get Name of the user
    var custName = $('#first-name').text();
    // Variable for the comment=append div
    var commentAppend = $('#comment-append');
    // Check if the div is empty
    if (commentAppend.html() === '') {
        // If empty display message
        commentAppend.append('<i><h4 id="com-placeholder">No comments so far...</h4></i>');
    }
    // On click of button
    $('form').on('submit', function (event) {
        // Grab `box` ID
        var divBox = document.getElementById("box");
        // Auto scroll when messages exceed the height of the box
        divBox.scrollTop = divBox.scrollHeight;
        // Grab input entered
        var comment = $('#comment').val();
        // Remove the placeholder comment
        $('#com-placeholder').remove();
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
                console.log(data.error)
            } else {
                // Append the message entered TODO: this will need to be the DB messages; static for now
                commentAppend.append('<div class="msg_bubble"><strong>' + custName +': </strong>' + comment + '</div>');
            }
        });
        event.preventDefault();
    });
}); // END $.ready()