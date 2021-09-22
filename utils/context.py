"""
Config policy and rule in chatbot && callbot 
"""
from home import graphs, actions
from home import model
import json 
import random 
import requests
import re 
from underthesea import ner
from vietnam_number import w2n 

f = open('config/api_config.json','r')
API_CONFIG = json.load(f)
f = open('regex/departments.json','r')
DEPARTMENTS = json.load(f)
ACTION_GREETING = 'action_ask_symptom_1'
THRESHOLD = 0.5

# Get bot's response
def get_message_response(message, records, true_intent, true_action, flag="text"):
    message = None
    properties = get_properties(true_action, records)
    print(f"properties: {properties}")
    message = get_message_text(true_action,true_intent, properties, records, flag)
    print(f"{true_action}: {message}")
    return message


"""
Using policy and rule to choose the best intent.
Cases depends on actions.

[format]
switch [pre_action]:
- case 'action_start': 
- case 'action_ask_symptom_1':
- case 'action_ask_department_2'
...
"""
def get_true_intent(message, records):
    try:
        true_intent = None
        pre_action = records['pre_action']
        pre_intent = records['pre_intent']
        true_intent = get_predict_intent(message, pre_action)
        
        if pre_action in ['action_start']:
            true_intent = "intent_start"
        
        if pre_action in ['action_ask_symptom_1']:
            true_intent = 'describe_symptom'
            records['customer_symptom'] = message

        if pre_action in ['action_ask_department_2']:
            true_department = None
            # regex to match department in client's response
            for department in DEPARTMENTS: 
                pattern = []
                for p in DEPARTMENTS[department]:
                    pattern.append(p)
                pattern = '|'.join(pattern)
                regex = re.compile(pattern)
                matched = regex.search(message)
                if matched:
                    print("choose department match: ", matched)
                    true_intent = 'choose_department'
                    true_department = department
                    records['choosen_department'] = true_department
            if true_department is None and true_intent in ['choose_department']:
                true_intent = 'choose_another_department'
            print(f"get_true_intent: true_intent: {true_intent} - true_department: {true_department}")
            # in case matched department
            if true_department:
                records['department'] = true_department
                records['this_week_free_date_status'] = True
                this_week_response, next_week_response = get_hospital_free_date()
                print("response:", this_week_response, next_week_response)
                this_week_free_date = json.loads(this_week_response)
                next_week_free_date = json.loads(next_week_response)

                if this_week_free_date['FreeStatus'] is True:
                    true_intent = 'free_booking'
                    records['this_week_free_date_status'] = True
                    records['free_date'] = this_week_free_date['ListFreeDay']
                if this_week_free_date['FreeStatus'] is False and next_week_free_date['FreeStatus'] is True:
                    true_intent = 'busy_booking'
                    records['this_week_free_date_status'] = False
                    records['free_date'] = next_week_free_date['ListFreeDay']

        if pre_action in ['action_ask_free_date_5','action_ask_free_date_repeat_18']:
            customer_pick_date = get_customer_pick_date(message)
            free_date_list = get_free_date_list(records)
            print(f"get_true_intent - customer_pick_date: {customer_pick_date} - free_date_list: {free_date_list}")
            if customer_pick_date is None:
                true_intent = "no_date"
            if customer_pick_date not in free_date_list:
                true_intent = "intent_fallback"
            else:
                customer_pick_date_detail = get_customer_pick_date_detail(customer_pick_date, records)
                true_intent = "pick_date"
                records['customer_pick_date'] = customer_pick_date
                records['customer_pick_date_detail'] = customer_pick_date_detail

        if pre_action in ['action_ask_name_6','action_ask_name_wrong_15']: 
            if true_intent in ["provide_name","ask_name_wrong"]:
                customer_name = get_customer_name(message)
                if customer_name is None:
                    true_intent = "intent_fallback"
                else:
                    true_intent = "provide_name"
                    records['customer_name'] = customer_name
        
        if pre_action in ['action_ask_gender_7','action_ask_gender_wrong_17']:
                customer_gender = get_customer_gender(message)
                if customer_gender is None:
                    true_intent = "intent_fallback"
                else:
                    true_intent = "provide_gender"
                    records['customer_gender'] = customer_gender

        if pre_action in ["action_ask_age_8",'action_ask_age_wrong_16']:
            customer_age = get_customer_age(message)
            if customer_age is None:
                true_intent = "intent_fallback"
            else:
                true_intent = "provide_age"
                records['customer_age'] = customer_age

        if pre_action in ["action_ask_priority_13"]:
            if true_intent in ["affirm_confirm"]:
                records['is_priority'] = True 
        
        if pre_action in ["action_ask_confirm_9"]:
            if true_intent in ['affirm_confirm']:
                meeting_hours = random.choice([""]) 
        print(f"get_true_intent - records: {records}")        
        return true_intent

    except Exception as e:
        print(f"Exception from get_true_intent: {e}")
        return "intent_fallback"

# Request to HospitalAPI to get free date in this week and next week
def get_hospital_free_date(records):
    true_department = records['choosen_department']
    if true_department == 'thần kinh':
        true_department = 'than kinh'
    if true_department == 'tim mạch':
        true_department = 'tim mach'
    if true_department == 'hô hấp':
        true_department = 'ho hap'
    if true_department == 'tai mắt miệng':
        true_department = 'tai mat mieng'
    if true_department == 'xương khớp':
        true_department = 'xuong khop'
    if true_department == 'khám nội':
        true_department = 'kham noi'
    if true_department == 'khám sức khỏe tổng hợp':
        true_department = 'kham suc khoe tong the'    
    this_week_endpoint = API_CONFIG['hospital-api'][0]['endpoint'] + true_department
    next_week_endpoint = API_CONFIG['hospital-api'][1]['endpoint'] + true_department
    this_week_response = requests.get(this_week_endpoint).text
    next_week_response = requests.get(next_week_endpoint).text
    return this_week_response, next_week_response

# Example Output: 'thứ 3'
def get_customer_pick_date(message):
    ans = None
    f = open('regex/date.json','r')
    dates = json.load(f)
    for date in dates:
        pattern = []
        for d in dates[date]:
            pattern.append(d)
        pattern = '|'.join(pattern)
        regex = re.compile(pattern)
        matched = regex.search(message)
        if matched:
            ans = date
    return ans

# Example Output: '22/09/2021'
def get_customer_pick_date_detail(customer_pick_date, records):
    ans = None 
    free_dates = records['free_date']
    for free_date in free_dates:
        if customer_pick_date == 'thứ 2' and free_date['order'] == 2:
            ans = free_date['date']
        if customer_pick_date == 'thứ 3' and free_date['order'] == 3:
            ans = free_date['date']
        if customer_pick_date == 'thứ 4' and free_date['order'] == 4:
            ans = free_date['date']
        if customer_pick_date == 'thứ 5' and free_date['order'] == 5:
            ans = free_date['date']
        if customer_pick_date == 'thứ 6' and free_date['order'] == 6:
            ans = free_date['date']
        if customer_pick_date == 'thứ 7' and free_date['order'] == 7:
            ans = free_date['date']
        if customer_pick_date == 'chủ nhật' and free_date['order'] == 8:
            ans = free_date['date']
    if ans is not None:
        ans = ans.split('/')
        ans = ans[1] + '/' + ans[0] + '/' + ans[2]
    return ans

# Example Output: 'Nguyễn Văn Hòa'
def get_customer_name(message):
    ans = []
    message = message.title() 
    tokens = ner(message)
    print(f"get_customer_name - message: {message} - tokens: {tokens}")
    for token in tokens:
        if "PER" in token[-1]:
            ans.append(token[0])
    if ans == []:
        if len(tokens) == 1 and tokens[0][-1] == "O":
            ans.append(tokens[0])
    return ans[-1]

# Example Output: 21
def get_customer_age(message):
    message = message.replace('năm nay', '')
    try:
        message = str(w2n(message))
    except Exception as e:
        print(f"Exception in recognize word to number: {e}")
    print(f"get_customer_age - w2n: {message}")
    ans = None
    pattern = '\d+'
    numbers = re.findall(pattern, message)
    print(f"get_customer_age: {numbers}")
    if len(numbers):
        ans = numbers[-1]
    return ans 

# Example Output: 'nam' or 'nữ'
def get_customer_gender(message):
    ans = None
    f = open('regex/gender.json','r')
    genders = json.load(f)
    for gender in genders:
        pattern = []
        for p in genders[gender]:
            pattern.append(p)
        pattern = '|'.join(pattern)
        regex = re.compile(pattern)
        matched = regex.search(message)
        if matched:
            ans = gender
        
    return ans
        
# Example Output: 'provide_name'
def get_predict_intent(message, pre_action):
    predict_label, prob = model.predict(message)
    print(f"get_predict_intent - label: {predict_label} - prob: {prob}")
    if pre_action in ['action_ask_symptom_1']:
        predict_label = "describe_symptom"
        return predict_label

    if prob < THRESHOLD:
        predict_label = "intent_fallback"
    
    return predict_label
    
"""
Get properties of chat status: the first time, repeat
"""
# Example Output: 'repeat'
def get_properties(true_action, records):
    properties = None
    
    if records['time_repeat'] != 0:
        properties = "repeat"
    else:
        properties = "first_time"
    return properties

"""
Replace all references in action templates
"""
def get_message_text(true_action, true_intent, properties, records, flag):
    message = None
    reponses = actions[true_action]
    for response in reponses:
        if response['properties'] == properties:
            if flag == "text":
                message = response['text']
                break
            if flag == "text_tts":
                message = response['text_tts']
                break
    message = message.replace("{get_hospital_name}", get_hospital_name(records))
    message = message.replace("{get_free_date}", get_free_date(records, flag))
    message = message.replace("{get_customer_info}", get_customer_info(records))
    message = message.replace("{get_meeting_time}", get_meeting_time(records))
    message = message.replace("{get_choosen_department}", get_choosen_department(records))
    return message

# Example Ouptut: "action_bye_12"
def get_true_action(true_intent, records):
    cur_action = None
    pre_action = records['pre_action']
    if pre_action == None:
        pre_action = 'action_start'
    if true_intent == "intent_start":
        cur_action = ACTION_GREETING
        return cur_action
    if true_intent in ['intent_fallback', 'cant_hear']:
        if records['time_repeat'] == 0:
            true_intent = 'intent_fallback'
        if records['time_repeat'] == 1:
            true_intent = 'intent_fallback_again'
        if records['time_repeat'] == 2:
            true_intent = 'repeat_three_times'
    if true_intent not in graphs[pre_action]:
        if pre_action != 'action_start':
            true_intent = 'intent_fallback'
        else:
            true_intent = 'intent_start'
    cur_action = graphs[pre_action][true_intent]
   
    if cur_action in ['action_ask_confirm_9']:
        records['confirm_repeat'] += 1
    if records['confirm_repeat'] > 2:
        cur_action = 'action_bye_12'
    
    if cur_action == pre_action:
        records['time_repeat'] += 1
    else:
        records['time_repeat'] = 0    
    return cur_action
    
"""
Update records after bot responses
"""
def update_records(records, true_intent, true_action):
    records['pre_action'] = true_action
    records['pre_intent'] = true_intent
    if "bye" in records['pre_action']:
        records['pre_action'] = 'action_start'
    

def get_free_date_list(records):
    free_dates = records['free_date']
    if free_dates == None:
        return ""
    dates = []
    this_week_free_date_status = records['this_week_free_date_status']
    for element in free_dates:
        print(element)
        order = element['order']
        if order == 2:
            dates.append("thứ 2")
        if order == 3:
            dates.append("thứ 3")
        if order == 4:
            dates.append("thứ 4")
        if order == 5:
            dates.append("thứ 5")
        if order == 6:
            dates.append("thứ 6")
        if order == 7:
            dates.append("thứ 7")
        if order == 8:
            dates.append("chủ nhật")
    return dates
    

#----------------- Reference to template action config -----------------#
def get_hospital_name(records):
    return records['hospital_name']


def get_free_date(records, flag):
    free_dates = records['free_date']
    if free_dates == None:
        return ""
    dates = []
    this_week_free_date_status = records['this_week_free_date_status']
    for element in free_dates:
        print(element)
        order = element['order']
        if order == 2:
            dates.append("thứ 2")
        if order == 3:
            dates.append("thứ 3")
        if order == 4:
            if flag == "text":
                dates.append("thứ 4")
            else:
                dates.append("thứ tư")
        if order == 5:
            dates.append("thứ 5")
        if order == 6:
            dates.append("thứ 6")
        if order == 7:
            dates.append("thứ 7")
        if order == 8:
            dates.append("chủ nhật")
    response = ", ".join(dates)
    if this_week_free_date_status == True:
        response += " trong tuần này"
    else:
        response += " trong tuần sau"
    return response


def get_customer_info(records):
    customer_name = records['customer_name']
    customer_age = records['customer_age']
    customer_gender = records['customer_gender']
    customer_pick_date = records['customer_pick_date']
    if customer_pick_date == "thứ 4":
        customer_pick_date = "thứ tư"
    response = ""
    this_week_free_date_status = records['this_week_free_date_status']
    if this_week_free_date_status is None or this_week_free_date_status == True:
        response = f"bệnh nhân {customer_name}, giới tính {customer_gender}, {customer_age} tuổi, chọn ngày {customer_pick_date} tuần này đến khám bệnh"
    else:
        response = f"bệnh nhân {customer_name}, giới tính {customer_gender}, {customer_age} tuổi, chọn ngày {customer_pick_date} tuần sau đến khám bệnh"
    return response


def get_meeting_time(records):
    response = "" 
    this_week_free_date_status = records['this_week_free_date_status']
    customer_pick_date = records['customer_pick_date']
    if customer_pick_date == "thứ 4":
        customer_pick_date = "thứ tư"
    customer_pick_date_detail = records['customer_pick_date_detail']
    detail_time = random.choice(list(range(7,18)))
    if this_week_free_date_status == True:
        response = f"{detail_time} giờ, {customer_pick_date} tuần này, ngày {customer_pick_date_detail}"
    if this_week_free_date_status == False:
        response = f"{detail_time} giờ, {customer_pick_date} tuần sau, ngày {customer_pick_date_detail}"
    return response

def get_choosen_department(records):
    if records['choosen_department'] is not None:
        choosen_department = "khoa " + records['choosen_department']
        return choosen_department
    return ""