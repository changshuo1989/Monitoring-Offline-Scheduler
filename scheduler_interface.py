import requests
import json
from rule import Rule
from schedule import Schedule

class Interface(object):

    def __init__(self, get_rules_endpoint, get_rules_method, send_rules_endpoint, send_rules_method):
        self.get_rules_endpoint = get_rules_endpoint
        self.get_rules_method = get_rules_method
        self.send_rules_endpoint = send_rules_endpoint
        self.send_rules_method = send_rules_method

    def get_valid_rules(self):
        if self.get_rules_method.lower() == 'get':
            res = requests.get(self.get_rules_endpoint)

            if res.status_code != 200:
                raise ValueError('getting valid rules and schedules failed!')
                return None
            else:
                rules_list = res.json()
                #rules_list = json.loads(rules_json)
                #rules_list = rules_json

                rules = []
                for rule_dictionary in rules_list:
                    rule = self.dictionary_to_rule(rule_dictionary)
                    rules.append(rule)

                return rules
        else:
            return None

    def send_triggered_rules(self, triggered_rules_schedules):
        if self.send_rules_method.lower() == 'post':
            json_data = json.dumps(triggered_rules_schedules)
            headers = {'content-type': 'application/json'}
            res = requests.post(self.send_rules_endpoint, data=json_data, headers=headers)
            if res.status_code != 200:
                raise ValueError('sending triggered rules and schedules failed!')
                return False
            else:
                #send to execution service
                return True

    def dictionary_to_schedule(self, dictionary):
        schedule_id = dictionary.get('id')
        schedule_type = dictionary.get('type')
        schedule_date = dictionary.get('date')
        schedule_hour_of_day = dictionary.get('hour_of_day')
        schedule_repeat_every = dictionary.get('repeat_every')
        schedule_last_updated = dictionary.get('last_updated')
        schedule_last_triggered = dictionary.get('last_triggered')

        return Schedule(schedule_id, schedule_type, schedule_date, schedule_hour_of_day, schedule_repeat_every,
                        schedule_last_updated, schedule_last_triggered)


    def dictionary_to_rule(self, dictionary):
        rule_id = dictionary.get('id')
        rule_status = dictionary.get('status')
        rule_start_time = dictionary.get('start_time')
        rule_end_time = dictionary.get('end_time')
        rule_last_updated = dictionary.get('last_updated')
        rule_last_triggered = dictionary.get('last_triggered')
        rule_last_executed = dictionary.get('last_executed')
        rule_schedules_list = dictionary.get('schedules')
        rule_schedules = []
        for schedule_dictionary in rule_schedules_list:
            schedule = self.dictionary_to_schedule(schedule_dictionary)
            rule_schedules.append(schedule)

        return Rule(rule_id, rule_schedules, rule_status, rule_start_time, rule_end_time, rule_last_updated,
                    rule_last_triggered, rule_last_executed)

'''
if __name__ == '__main__':
    triggered_rules_schedules = {}
    triggered_rules_schedules[1] = [1,2,3]
    triggered_rules_schedules[2] = [4,6]
    triggered_rules_schedules[3] =[101,234]

    interface = Interface('asdf','GET', 'http://localhost:8080/post', 'POST')
    interface.send_triggered_rules(triggered_rules_schedules)
'''