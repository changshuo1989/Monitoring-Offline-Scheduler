import datetime
import yaml
import logging


CONFIG_FILE = 'config.yml'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def read_config_file():
    config = None
    with open(CONFIG_FILE, 'r') as config_file:
        config = yaml.load(config_file)
    return config


def init_logger():
    logger = logging.getLogger('offline-schedule-logger')
    hdlr = logging.FileHandler('output.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger


def calculate_sleep_time():
    now = datetime.datetime.now()
    pre_min = now.minute // 10 * 10
    pre_time = datetime.datetime(now.year, now.month, now.day, now.hour, pre_min)
    aim_time = pre_time+datetime.timedelta(minutes=10)
    delta = aim_time 
    return delta.total_seconds()


def change_datetime_to_floor_tens_minute(date_time):
    new_date_time_str = date_time.strftime(DATETIME_FORMAT)
    new_date_time = datetime.datetime.strptime(new_date_time_str, DATETIME_FORMAT)
    minute = new_date_time.minute // 10 * 10
    return new_date_time.replace(minute=minute).replace(second=0)


def change_datetime_to_ceil_tens_minute(date_time):
    new_date_time_str = date_time.strftime(DATETIME_FORMAT)
    new_date_time = datetime.datetime.strptime(new_date_time_str, DATETIME_FORMAT)
    if new_date_time.minute % 10 != 0:
        minute = new_date_time.minute // 10 * 10
        new_date_time = new_date_time.replace(minute=minute).replace(second=0)
        new_date_time = new_date_time + datetime.timedelta(minutes=10)
    return new_date_time


def get_same_day_next_x_months(current_date_time, number_of_months):
    current_year = current_date_time.year
    current_month = current_date_time.month
    years_added = (current_month+number_of_months)//12

    new_month = (current_month+number_of_months)%12
    if new_month == 0:
        new_month = 12
    return current_date_time.replace(year=current_date_time.year+years_added, month=new_month)


#test = datetime.datetime.strptime('2017-12-27 19:46:04', DATETIME_FORMAT)
#print(test)