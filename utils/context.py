from home import graphs, actions


import json 

f = open('config/api_config.json','r')
API_CONFIG = json.load(f)

INTENT_ENDPONINT = API_CONFIG['intent-api'][0]['endpoint']
INTENT_METHOD = API_CONFIG['intent-api'][0]['method']

ACTION_GREETING = 'action_ask_symptom_1'


def get_message_response(message, records, true_intent, true_action):
    message = None
    properties = get_properties(true_intent, records)
    print(f"properties: {properties}")
    message = get_message_text(true_action,true_intent, properties, records)
    print(f"message: {message}")

    return message

def get_true_intent(message, records):
    true_intent = None
    pre_action = records['pre_action']
    pre_intent = records['pre_intent']
    true_intent = get_predict_intent(message, pre_action)
    if pre_action == 'action_start':
        true_intent = "intent_start"
    return true_intent

def get_predict_intent(message, pre_action):
    # request to classification - API
    if pre_action == 'action_ask_symptom_1':
        return "describe_symptom"
    if pre_action == 'action_ask_department_2':
        return "choose_another_department"
    # if pre_action == 'action_ask_symptom_1':
    #     return "describe_symptom"
    # if pre_action == 'action_ask_symptom_1':
    #     return "describe_symptom"
    # if pre_action == 'action_ask_symptom_1':
    #     return "describe_symptom"
    # if pre_action == 'action_ask_symptom_1':
    #     return "describe_symptom"
    
    
def get_properties(true_intent, records):
    properties = None
    pre_intent = records['pre_intent']
    if true_intent == pre_intent:        
        properties = "repeat"
    else:
        properties = "first_time"
    return properties

def get_message_text(true_action, true_intent, properties, records):
    message = None
    reponses = actions[true_action]
    for response in reponses:
        if response['properties'] == properties:
            message = response['text']
            break
    message = message.replace("{get_hospital_name}", get_hospital_name(records))
    message = message.replace("{get_free_date}", get_free_date(records))
    message = message.replace("{get_customer_info}", get_customer_info(records))
    return message

def get_true_action(true_intent, records):
    cur_action = None
    pre_action = records['pre_action']
    if true_intent == "intent_start":
        cur_action = ACTION_GREETING
        return cur_action
    
    cur_action = graphs[pre_action][true_intent]
    return cur_action
    
def update_records(records, true_intent, true_action):
    records['pre_action'] = true_action
    records['pre_intent'] = true_intent
    return records


# Reference to TemplateAction config
def get_hospital_name(records):
    return records['hospital_name']

def get_free_date(records):
    return "" 

def get_customer_info(records):
    return ""

