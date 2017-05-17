$(document).ready(function () {

    $('form').on('submit', function (event) {
        var fName = $('#f_name').val();
        var lName = $('#l_name').val();
        var email = $('#email').val();
        var phone_number = $('#phone_number').val();
        var ticket_type = $('#ticket_type').val();
        var severity = $('#severity').val();
        var message = $('textarea').val();

        // Create object with all the data to send with AJAX
        var form_data = {
            'fName': fName,
            'lName': lName,
            'email': email,
            'phone_number': phone_number,
            'ticket_type': ticket_type,
            'severity': severity,
            'message': message
        };

        // AJAX
        $.ajax({
            type: 'POST',
            url: 'https://acae7c65.ngrok.io/process_form',
            data: JSON.stringify(form_data, null, '\t'),
            contentType: 'application/json;charset=UTF-8',
            success: function (response) {
                // Clear the form on success
                $('form').trigger('reset');
                // Scroll to the top
                window.scrollTo(0,0);
                // Flash success message
                $('#successAlert').text('Your ticket was successfully submitted!').show();
            },
            error: function (error) {
                console.log(error);
            }
        });
        event.preventDefault();
    })
});