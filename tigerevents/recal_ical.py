# CALENDAR EXPORT
from icalendar import Calendar, Event, vText, vRecur
from datetime import datetime, timedelta
from dateutil import parser as dt_parser
import pytz
import uuid


@require_GET
@never_cache
def ical_feed(request, cal_id):
    """
    iCal feed
    Kept up-to-date
    Parameter: cal_id, which is a guid that is 1:1 with schedules in our database
    """
    cal = Calendar()
    cal.add('prodid', '-//Recal Course Planner//recal.io//')
    cal.add('version', '2.0')

    try:
        sched = Schedule.objects.get(Q(ical_uuid=uuid.UUID(cal_id)))
    except Schedule.DoesNotExist:
        return HttpResponseNotFound("Not Found")
    semester = sched.semester

    cal.add('X-WR-CALNAME', 'ReCal %s (%s)' %
            (unicode(semester), sched.user.netid))
    cal.add('X-WR-CALDESC', sched.title)  # 'ReCal Schedule'
    # https://msdn.microsoft.com/en-us/library/ee178699(v=exchg.80).aspx. 15
    # minute updates.
    cal.add('X-PUBLISHED-TTL', 'PT15M')

    tz = pytz.timezone("US/Eastern")  # pytz.utc
    # recurrence
    ical_days = {
        0: 'MO',
        1: 'TU',
        2: 'WE',
        3: 'TH',
        4: 'FR'
    }
    builtin_days = {
        'M': 0,
        'T': 1,
        'W': 2,
        'Th': 3,
        'F': 4
    }

    #data = [hydrate_course_dict(Course.objects.get(Q(id=course['course_id']))) for course in json.loads(sched.enrollments)]

    # 0-6, monday is 0, sunday is 6. we will have values of 0 (Monday) or 2
    # (Wednesday)
    day_of_week_semester_start = semester.start_date.weekday()

    for course_obj in json.loads(sched.enrollments):
        # course = Course.objects.get(Q(id=course_obj['course_id'])) #
        # course_obj is json object; course is model
        for section_id in course_obj['sections']:
            section = Section.objects.get(Q(pk=section_id))
            for meeting in section.meetings.all():
                event = Event()
                event.add('summary', unicode(section))  # name of the event
                event.add('location', vText(
                    meeting.location + ', Princeton, NJ'))

                # compute first meeting date.
                # days when the class meets. convert them to day difference
                # relative to first date of the semester
                # split by space. format: 0-4. monday is 0, friday is 4.
                # matches python weekday() format.
                daysofweek = [builtin_days[i] for i in meeting.days.split()]
                if len(daysofweek) == 0:
                    # no meetings -- skip
                    continue
                dayofweek_relative_to_semester_start = []
                for dow in daysofweek:
                    diff = dow - day_of_week_semester_start
                    if diff < 0:
                        diff += 7  # add a week
                    dayofweek_relative_to_semester_start.append(diff)
                # all must be positive
                assert all(
                    [d >= 0 for d in dayofweek_relative_to_semester_start])
                # a T,Th class will have first meeting on T if semester starts
                # on M, or on Th if semester starts on Wed.
                first_meeting_dayofweek = min(
                    dayofweek_relative_to_semester_start)

                # get meeting time
                # meeting.start_time, meeting.end_time examples: "03:20 PM",
                # "10:00 AM"
                start_time = dt_parser.parse(meeting.start_time)
                end_time = dt_parser.parse(meeting.end_time)

                # add event time.
                event.add('dtstart', tz.localize(datetime(semester.start_date.year, semester.start_date.month, semester.start_date.day,
                                                          start_time.hour, start_time.minute, 0) + timedelta(days=first_meeting_dayofweek)))  # year,month,day, hour,min,second in ET
                event.add('dtend', tz.localize(datetime(semester.start_date.year, semester.start_date.month,
                                                        semester.start_date.day, end_time.hour, end_time.minute, 0) + timedelta(days=first_meeting_dayofweek)))
                # "property specifies the DATE-TIME that iCalendar object was created". per 3.8.7.2 of RFC 5545, must be in UTC
                event.add('dtstamp', tz.localize(datetime(semester.start_date.year,
                                                          semester.start_date.month, semester.start_date.day, 0, 0, 0)))

                # recurring event config
                # producing e.g.: RRULE:FREQ=WEEKLY;UNTIL=[LAST DAY OF SEMESTER
                # + 1];WKST=SU;BYDAY=TU,TH
                selected_days = [ical_days[i]
                                 for i in sorted(daysofweek)]  # formatted for ical
                end_date = tz.localize(datetime(semester.end_date.year, semester.end_date.month,
                                                semester.end_date.day, 0, 0, 0) + timedelta(days=1))  # [LAST DAY OF SEMESTER + 1]
                event.add('rrule', vRecur(
                    {'FREQ': 'WEEKLY', 'UNTIL': end_date, 'WKST': 'SU', 'BYDAY': selected_days}))
                cal.add_component(event)

    ical = cal.to_ical()

    # filter out blank lines
    #filtered = filter(lambda x: not re.match(r'^\s*$', x), ical)
    # print filtered
    return HttpResponse(ical, 'text/calendar', status=200)


@login_required
def get_ical_url_for_schedule(request, schedule_id):
    return get_ical_url(request, schedule_id, make_new=False)


@login_required
def regenerate_ical_url_for_schedule(request, schedule_id):
    return get_ical_url(request, schedule_id, make_new=True)


def get_ical_url(request, schedule_id, make_new=False):
    """
    Returns ical feed url for a particular schedule
    Parameter: schedule_id
    We look up the UUID that is 1:1 to this schedule. Each schedule has a UUID always (it is auto-created.)
    If make_new, then we create a new UUID for the schedule.
    Then we return the url with it
    """
    try:
        schedule = Schedule.objects.get(Q(pk=schedule_id))
    except Schedule.DoesNotExist:
        return HttpResponseNotFound("Not Found")
    # Confirm ownership
    if schedule.user.netid != request.user.username:
        return HttpResponseForbidden("Forbidden")

    if make_new:
        schedule.ical_uuid = uuid.uuid4()
        schedule.save()
    return HttpResponse(request.build_absolute_uri(reverse('ical-feed', args=(str(schedule.ical_uuid),))))