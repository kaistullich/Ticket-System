import json
from twilio.rest import Client

with open('src/config.json') as f:
    config_f = json.load(f)

account_sid = config_f['account_sid']
auth_token = config_f['auth_token']

client = Client(account_sid, auth_token)


def ticket_call(dept_number):
    call = client.api.account.calls.create(to=dept_number,
                                           from_=config_f['from_'],
                                           url="https://4b49a3e0.ngrok.io/words",
                                           )
    print(call.sid)
