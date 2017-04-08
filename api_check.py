import json
import time

import requests

from src.all_notifications import ticket_call


r = requests.get('http://127.0.0.1:5000/api/Ticket')
print('Request status: ' + str(r.status_code))
api_objs = r.text
tickets = json.loads(api_objs)
now = int(time.strftime('%H%M'))

while True:
    time.sleep(10)
    print('** CHECKING API FOR NEW TICKETS! **')
    for ticket in tickets['objects']:
        status = ticket['ticket_status']
        severity = ticket['ticket_severity']
        time_ = ticket['ticket_time']
        if severity == 1:
            if status == "Open":
                if now - time_ >= 60:
                    # TODO: Change number to cellphone when testing away from home
                    print('Ticket/s found', ticket['tickerID'])
                    ticket_call('4084655095')
                print('No ticket found')
            print('No ticket found')
        print('No ticket found')