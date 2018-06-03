import time
import datetime
from utility import DATETIME_FORMAT, calculate_sleep_time, init_logger, read_config_file
from scheduler_interface import Interface


if __name__ == '__main__':
    logger = None
    try:
        logger = init_logger()

        while True:
            try:
                # sleep
                time.sleep(calculate_sleep_time())
                #test
                #time.sleep(6)
                #get current datetime
                now = datetime.datetime.now()
                # log this check
                logger.info('This check started at:'+ now.strftime(DATETIME_FORMAT))
                # read config file
                config = read_config_file()
                get_rules_endpoint = config['services']['get_valid_rules']['endpoint']
                get_rules_method = config['services']['get_valid_rules']['http_method']

                send_rules_endpoint = config['services']['send_triggered_rules']['endpoint']
                send_rules_method = config['services']['send_triggered_rules']['http_method']

                send_executable_rules_endpoint = config['services']['send_to_be_executed_rules']['endpoint']
                send_executable_rules_method = config['services']['send_to_be_executed_rules']['http_method']
                # initialize interface
                interface = Interface(get_rules_endpoint, get_rules_method,
                                      send_rules_endpoint, send_rules_method,
                                      send_executable_rules_endpoint,send_executable_rules_method)
                rules = interface.get_valid_rules()

                triggered_rules_schedules = {}

                for rule in rules:
                    triggered_schedules = rule.get_triggered_schedules(now)
                    if len(triggered_schedules) > 0:
                        triggered_rules_schedules[rule.id] = triggered_schedules
                        logger.info("triggered rule:" + str(rule.id))
                        logger("triggered schedules:" + str(triggered_schedules))

                if triggered_rules_schedules:
                    interface.send_triggered_rules(triggered_rules_schedules)

            except Exception as e:
                logger.exception(e)

    except Exception as e:
        logger.exception(e)
