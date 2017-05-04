import json
import time

import requests

from src.notifications import ticket_reminder_call

# JSON config values
with open('src/config_values.json') as f:
    config_f = json.load(f)
# Send off requests to API
r = requests.get(config_f['api_url'])
# Print status code
print('Request status: ' + str(r.status_code))
# All API text
api_objs = r.text
# Load tickets
tickets = json.loads(api_objs)
# Current time
time_now = int(time.strftime('%H%M'))
# Current date
date_now = time.strftime('%D')

# Start loop
while True:
    # Sleep for 10 seconds
    time.sleep(10)
    print('** CHECKING API FOR NEW TICKETS! **')
    # Will change to `True` for a ticket was found
    open_tix_found = False
    # Loop through all tickets in API
    for ticket in tickets['objects']:
        # Ticket status ('Open')
        tix_status = ticket['tix_status']
        # Ticket severity ('P1')
        tix_severity = ticket['tix_severity']
        # Time ticket was created
        tix_time = ticket['tix_recv_time']
        # Date ticket was received
        tix_date = ticket['tix_recv_date']
        if tix_severity == 1:
            if tix_status == "Open":
                if date_now == tix_date:
                    if time_now - tix_time >= 60:
                        # Matching ticket found
                        open_tix_found = True
                elif date_now != tix_date:
                    # Matching ticket found
                    open_tix_found = True

    # `open_tix_found` changed to `True`
    if open_tix_found:
        print('~~~ FOUND OPEN P1 TICKETS ~~~')
        # Start call
        ticket_reminder_call(config_f['dept_num'])