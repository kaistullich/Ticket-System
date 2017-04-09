import json
import time

import requests

from src.all_notifications import ticket_reminder_call

with open('src/config.json') as f:
    config_f = json.load(f)

# TODO: change url to NEW ngrok url
r = requests.get('http://27d3f05a.ngrok.io/api/Ticket')
print('Request status: ' + str(r.status_code))
api_objs = r.text
tickets = json.loads(api_objs)
time_now = int(time.strftime('%H%M'))
date_now = time.strftime('%a, %d %b %Y')

while True:
    time.sleep(10)
    print('** CHECKING API FOR NEW TICKETS! **')
    open_tix_counter = 0
    open_tix_found = False
    for ticket in tickets['objects']:
        tix_status = ticket['tix_status']
        tix_severity = ticket['tix_severity']
        tix_time = ticket['tix_recv_time']
        tix_date = ticket['tix_recv_date']
        if tix_severity == 1:
            if tix_status == "Open":
                if date_now == tix_date:
                    if time_now - tix_time >= 60:
                        print('Ticket(s) found', ticket['ticketID'])
                        open_tix_counter += 1
                        open_tix_found = True
                elif date_now != tix_date:
                    print('Ticket(s) found', ticket['ticketID'])
                    open_tix_counter += 1
                    open_tix_found = True

    if open_tix_found:
        # TODO: Change number to cellphone when testing away from home
        ticket_reminder_call(config_f['dept_num'])  # Home number currently
