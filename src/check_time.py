import time
from src.models import TicketDB

now = int(time.strftime('%H%M'))

tickets = TicketDB.query.all()


def ticket_time_check():
    while True:
        print('CHECKING THE DATABASE')
        print('CHECKING THE DATABASE')
        print('CHECKING THE DATABASE')
        print('CHECKING THE DATABASE')
        print('CHECKING THE DATABASE')
        print('CHECKING THE DATABASE')
        print('CHECKING THE DATABASE')

        time.sleep(6)  # 1 hour
        print('******* CHECKING THE DATABASE')
        print('******* CHECKING THE DATABASE')
        print('******* CHECKING THE DATABASE')
        print('******* CHECKING THE DATABASE')
        print('******* CHECKING THE DATABASE')

        total_tix = []
        for tix in tickets:
            if tix.ticket_severity == 1:
                if tix.ticket_status == "Open":
                    if now - tix.ticket_time >= 60:
                        total_tix.append(tix.ticketID)
        return total_tix
