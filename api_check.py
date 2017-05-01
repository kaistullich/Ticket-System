import json
import time

import requests

from src.notifications import ticket_reminder_call

with open('src/config_values.json') as f:
    config_f = json.load(f)

r = requests.get(config_f['api_url'])
print('Request status: ' + str(r.status_code))
api_objs = r.text
tickets = json.loads(api_objs)
time_now = int(time.strftime('%H%M'))
date_now = time.strftime('%D')

while True:
    time.sleep(10)
    print('** CHECKING API FOR NEW TICKETS! **')
    open_tix_found = False
    for ticket in tickets['objects']:
        tix_status = ticket['tix_status']
        tix_severity = ticket['tix_severity']
        tix_time = ticket['tix_recv_time']
        tix_date = ticket['tix_recv_date']
        if tix_severity == 1:
            if tix_status == "Open":
                if date_now == tix_date:
                    if time_now - tix_time >= 5:
                        open_tix_found = True
                elif date_now != tix_date:
                    open_tix_found = True

    if open_tix_found:
        print('~~~ FOUND OPEN P1 TICKETS ~~~')
        ticket_reminder_call(config_f['dept_num'])
