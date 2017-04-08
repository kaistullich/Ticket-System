import json
import time

import requests

from src.all_notifications import ticket_call

with open('src/config.json') as f:
    config_f = json.load(f)

r = requests.get('http://127.0.0.1:5000/api/Ticket')
print('Request status: ' + str(r.status_code))
api_objs = r.text
tickets = json.loads(api_objs)
time_now = int(time.strftime('%H%M'))

while True:
    time.sleep(10)
    print('** CHECKING API FOR NEW TICKETS! **')
    ticket_list = []
    for ticket in tickets['objects']:
        status = ticket['ticket_status']
        severity = ticket['ticket_severity']
        tix_time = ticket['ticket_time']
        if severity == 1:
            if status == "Open":
                if time_now - tix_time >= 60:
                    # TODO: Change number to cellphone when testing away from home
                    print('Ticket(s) found', ticket['ticketID'])
                    ticket_list.append(ticket['ticketID'])
                    ticket_call(config_f['dept_num'])  # Home number currently
