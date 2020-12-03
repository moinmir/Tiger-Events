from ics import Calendar, Event
import os
from flask import current_app

# create ical file for one user
def create_ical(events):
    c = Calendar()
    for event in events:
        e = Event(name=event.title,
                  begin=event.start_date,
                  end=event.end_date,
                  description=event.description,
                  created=event.date_posted,
                  location=event.location)
        c.events.add(e)
    
    return c


def save_ical(user, cal):
    ical_fn =  user.ical_uuid.hex + '.ics'
    ical_path = os.path.join(current_app.config["USER_CAL"], ical_fn)

    with open(ical_path, 'w') as my_file:
        my_file.writelines(cal)
    
    return ical_fn
