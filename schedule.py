import datetime
from utility import DATETIME_FORMAT, change_datetime_to_floor_tens_minute, \
    change_datetime_to_ceil_tens_minute, get_same_day_next_x_months

class Schedule(object):
    def __init__(self, id, type, date, hour_of_day, repeat_every, last_updated, last_triggered):
        self.id = id
        self.type = type
        self.date = date
        self.hour_of_day = hour_of_day
        self.repeat_every = repeat_every
        self.last_updated = last_updated
        self.last_triggered = last_triggered


    def is_triggered(self, date_time, start_time, end_time):
        #clean current_date_time format
        #current_date_time_str = date_time.strftime(DATETIME_FORMAT)
        #current_date_time= datetime.datetime.strptime(current_date_time_str, DATETIME_FORMAT)
        #minute = current_date_time.minute // 10 * 10
        #current_date_time = current_date_time.replace(minute=minute)
        current_date_time = change_datetime_to_floor_tens_minute(date_time)

        last_updated = None
        last_triggered = None

        if self.last_updated is not None and self.last_updated != '':
            last_updated = datetime.datetime.strptime(self.last_updated, DATETIME_FORMAT)

        if self.last_triggered is not None and self.last_triggered != '':

            last_triggered = change_datetime_to_floor_tens_minute(datetime.datetime.strptime(self.last_triggered, DATETIME_FORMAT))

        # every X type
        if self.type == 1:
            updated_time = last_triggered + datetime.timedelta(minutes=self.repeat_every)
            updated_time = change_datetime_to_floor_tens_minute(updated_time)
            if last_triggered is None and start_time is not None:
                # find most reasonable first triggered time based on start_time
                first_trigger_time = change_datetime_to_ceil_tens_minute(start_time)
                if current_date_time == first_trigger_time:
                    return True
            elif last_triggered is not None:
                if current_date_time > updated_time:
                    while current_date_time >= updated_time:
                        if current_date_time == updated_time:
                            return True
                        else:
                            updated_time = updated_time + datetime.timedelta(minutes=self.repeat_every)
                            updated_time = change_datetime_to_floor_tens_minute(updated_time)
                elif current_date_time == updated_time:
                    return True


        # daily type
        elif self.type == 2:
            if last_triggered is None:
                if current_date_time.hour == self.hour_of_day and current_date_time.minute == 0:
                    return True
            else:
                updated_time = last_triggered + datetime.timedelta(days=self.repeat_every)

                if current_date_time > updated_time:
                    if current_date_time.hour == self.hour_of_day and current_date_time.minute == 0:
                        return True

                elif (current_date_time.year == updated_time.year
                    and current_date_time == updated_time.month
                    and current_date_time.day == updated_time.day
                    and current_date_time.hour == self.hour_of_day
                    and current_date_time.minute == 0):

                    return True




        # weekly type
        elif self.type == 3:
            if last_triggered is None:
                if (current_date_time.weekday() == self.date
                    and current_date_time.hour == self.hour_of_day
                    and current_date_time.minute == 0):
                    return True

            else:
                updated_time = last_triggered + datetime.timedelta(weeks=self.repeat_every)
                if current_date_time > updated_time:
                    if (current_date_time.weekday() == self.date
                        and current_date_time.hour == self.hour_of_day
                        and current_date_time.minute == 0):
                        return True

                elif (current_date_time.year == updated_time.year
                    and current_date_time.month == updated_time.month
                    and current_date_time.day == updated_time.day
                    and current_date_time.hour == self.hour_of_day
                    and current_date_time.minute == 0):

                    return True



        # monthly type
        elif self.type == 4:
            if last_triggered is None:
                if (current_date_time.day == self.date
                    and current_date_time.hour == self.hour_of_day
                    and current_date_time.minute == 0):
                    return True

            else:
                updated_time = get_same_day_next_x_months(last_triggered, self.repeat_every)
                if current_date_time > updated_time:
                    if (current_date_time.day == self.date
                        and current_date_time.hour == self.hour_of_day
                        and current_date_time.minute == 0):
                        return True

                elif (current_date_time.year == updated_time.year
                    and current_date_time.month == updated_time.month
                    and current_date_time.day == updated_time.day
                    and current_date_time.hour == self.hour_of_day
                    and current_date_time.minute == 0):
                    return True


        else:
            return False
        #Test
            #return True












