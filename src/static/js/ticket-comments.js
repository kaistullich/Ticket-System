$(document).ready(function () {
   // Variable for the comment=append div
    var commentAppend = $('#comment-append');
    // Check if the div is empty
    if (commentAppend.html() === '') {
        // If empty display message
        commentAppend.append('<i><h4 id="com-placeholder">No comments so far...</h4></i>');
    }
    // On click of button
    $('#submit-btn').click(function () {
        // Grab input entered
        var comment = $('#comment').val();
        // Remove the placeholder comment
        $('#com-placeholder').remove();
        // Append the message entered TODO: this will need to be the DB messages; static for now
        commentAppend.append('<div class="msg_bubble">' + comment + '</div>')
    });
});