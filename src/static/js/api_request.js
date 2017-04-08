$.ajax({
    type: "GET",
    datatype: 'json',
    url: "http://127.0.0.1:5000/api/Ticket",
    success: function(data){
        parseTickets(data)
    },
    error: function(error){
        console.log(error.responseText)
    }
});

function parseTickets(data){
    var all_tickets = data.objects;
    for (var i = 0; i < all_tickets.length; i++){
        var ticket = all_tickets[i];
        console.log('Ticket Severity for Ticket number: '+ ticket['ticketID'] + ' = ' + ticket['ticket_severity']);
    }
}