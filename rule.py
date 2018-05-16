import datetime
from utility import DATETIME_FORMAT

class Rule(object):
    def __init__(self, id, schedules, status, start_time, end_time, last_updated, last_triggered, last_executed):
        self.id = id
        self.schedules = schedules
        self.status = status
        self.start_time = start_time
        self.end_time = end_time
        self.last_updated = last_updated
        self.last_triggered = last_triggered
        self.last_executed = last_executed

    def get_triggered_schedules(self, date_time):
        triggered_schedules = []
        if self.status.lower() == 'active':
            time_start = None
            time_end = None
            if self.start_time != '':
                time_start = datetime.datetime.strptime(self.start_time, DATETIME_FORMAT)
            if self.end_time != '':
                time_end = datetime.datetime.strptime(self.end_time, DATETIME_FORMAT)

            if ((time_start is None and time_end is None)
                or (time_start is None and date_time < time_end)
                or (time_end is None and date_time >= time_start) or (time_start <= date_time < time_end)):
                for schedule in self.schedules:
                    if schedule.is_triggered(date_time, time_start, time_end):
                        triggered_schedules.append(schedule.id)

        return triggered_schedules
