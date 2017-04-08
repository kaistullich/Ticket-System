import pprint
import json
import requests

r = requests.get('http://127.0.0.1:5000/api/Ticket')
text = r.text
tickets = json.loads(text)

for ticket in tickets['objects']:
    print(ticket['ticketID'])
