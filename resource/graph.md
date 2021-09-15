> action_start > intent_start > action_ask_symptom_1

# action_ask_symptom_1
> action_ask_symptom_1 > describe_symptom > action_ask_department_2
> action_ask_symptom_1 > cant_hear > action_ask_symptom_1
> action_ask_symptom_1 > intent_fallback > action_ask_symptom_1 
> action_ask_symptom_1 > intent_fallback_again > action_ask_symptom_1
> action_ask_symptom_1 > repeat_three_times > action_bye_12

# action_ask_department_2
> action_ask_department_2 > choose_another_department > action_bye_3
> action_ask_department_2 > choose_department > action_ask_department_2
> action_ask_department_2 > free_booking > action_ask_free_date_5
> action_ask_department_2 > busy_booking > action_ask_next_week_4
> action_ask_department_2 > intent_fallback > action_ask_department_2
> action_ask_department_2 > intent_fallback_again > action_ask_department_2
> action_ask_department_2 > repeat_three_times > action_bye_12

# action_ask_next_week_4 
> action_ask_next_week_4 > deny_confirm > action_bye_14
> action_ask_next_week_4 > affirm_confirm > action_ask_free_date_5 
> action_ask_next_week_4 > intent_fallback > action_ask_next_week_4
> action_ask_next_week_4 > intent_fallback_again > action_ask_next_week_4
> action_ask_next_week_4 > repeat_three_times > action_bye_12

# action_ask_free_date_5
> action_ask_free_date_5 > pick_date > action_ask_name_6
> action_ask_free_date_5 > cant_hear > action_ask_free_date_5
> action_ask_free_date_5 > intent_fallback > action_ask_free_date_5 
> action_ask_free_date_5 > intent_fallback_again > action_ask_free_date_5
> action_ask_free_date_5 > repeat_three_times > action_bye_12

# action_ask_name_6
> action_ask_name_6 > provide_name > action_ask_gender_7
> action_ask_name_6 > cant_hear > action_ask_name_6
> action_ask_name_6 > intent_fallback > action_ask_name_6
> action_ask_name_6 > intent_fallback_again > action_ask_name_6
> action_ask_name_6 > repeat_three_times > action_bye_12

# action_ask_gender_7
> action_ask_gender_7 > provide_gender > action_ask_age_8
> action_ask_gender_7 > cant_hear > action_ask_gender_7
> action_ask_gender_7 > intent_fallback > action_ask_gender_7
> action_ask_gender_7 > intent_fallback_again > action_ask_gender_7
> action_ask_gender_7 > repeat_three_times > action_bye_12

# action_ask_age_8
> action_ask_age_8 > provide_age > action_ask_priority_13
> action_ask_age_8 > cant_hear > action_ask_age_8
> action_ask_age_8 > intent_fallback > action_ask_age_8
> action_ask_age_8 > intent_fallback_again > action_ask_age_8 
> action_ask_age_8 > repeat_three_times > action_bye_12

# action_ask_priority_13
> action_ask_priority_13 > deny_confirm > action_ask_confirm_9
> action_ask_priority_13 > affirm_confirm > action_ask_confirm_9
> action_ask_priority_13 > cant_hear > action_ask_priority_13
> action_ask_priority_13 > intent_fallback > action_ask_priority_13
> action_ask_priority_13 > intent_fallback_again > action_ask_priority_13
> action_ask_priority_13 > repeat_three_times > action_bye_12

# action_ask_confirm_9 
> action_ask_confirm_9 > affirm_confirm > action_bye_11
> action_ask_confirm_9 > deny_confirm > action_ask_wrong_information_10
> action_ask_confirm_9 > cant_hear > action_ask_confirm_9
> action_ask_confirm_9 > intent_fallback > action_ask_confirm_9
> action_ask_confirm_9 > intent_fallback_again > action_ask_confirm_9 
> action_ask_confirm_9 > repeat_three_times > action_ask_confirm_9

# action_ask_wrong_information_10
> action_ask_wrong_information_10 > ask_name_repeat > action_ask_name_repeat_15
> action_ask_wrong_information_10 > provide_name > action_ask_confirm_9
> action_ask_wrong_information_10 > ask_age_repeat > action_ask_age_repeat_16
> action_ask_wrong_information_10 > provide_age > action_ask_confirm_9
> action_ask_wrong_information_10 > ask_gender_repeat > action_ask_gender_repeat_17
> action_ask_wrong_information_10 > provide_gender > action_ask_gender_repeat_17
> action_ask_wrong_information_10 > ask_date_repeat > action_ask_free_date_repeat_18
> action_ask_wrong_information_10 > pick_date > action_ask_free_date_repeat_18
> action_ask_wrong_information_10 > intent_fallback > action_ask_wrong_information_10
> action_ask_wrong_information_10 > intent_fallback_again > action_ask_wrong_information_10
> action_ask_wrong_information_10 > repeat_three_times > action_ask_wrong_information_10

# action_ask_name_repeat_15
> action_ask_name_repeat_15 > provide_name > action_ask_confirm_9
> action_ask_name_repeat_15 > cant_hear > action_ask_name_repeat_15
> action_ask_name_repeat_15 > intent_fallback > action_ask_name_repeat_15
> action_ask_name_repeat_15 > intnet_fallback_again > action_ask_name_repeat_15
> action_ask_name_repeat_15 > repeat_three_times > action_bye_12 

# action_ask_age_repeat_16
> action_ask_age_repeat_16 > provide_name > action_ask_confirm_9
> action_ask_age_repeat_16 > cant_hear > action_ask_age_repeat_16
> action_ask_age_repeat_16 > intent_fallback > action_ask_age_repeat_16
> action_ask_age_repeat_16 > intnet_fallback_again > action_ask_age_repeat_16
> action_ask_age_repeat_16 > repeat_three_times > action_bye_12 

# action_ask_gender_repeat_17
> action_ask_gender_repeat_17 > provide_name > action_ask_confirm_9
> action_ask_gender_repeat_17 > cant_hear > action_ask_gender_repeat_17
> action_ask_gender_repeat_17 > intent_fallback > action_ask_gender_repeat_17
> action_ask_gender_repeat_17 > intnet_fallback_again > action_ask_gender_repeat_17
> action_ask_gender_repeat_17 > repeat_three_times > action_bye_12 

# action_ask_free_date_repeat_18
> action_ask_free_date_repeat_18 > provide_name > action_ask_confirm_9
> action_ask_free_date_repeat_18 > cant_hear > action_ask_free_date_repeat_18
> action_ask_free_date_repeat_18 > intent_fallback > action_ask_free_date_repeat_18
> action_ask_free_date_repeat_18 > intnet_fallback_again > action_ask_free_date_repeat_18
> action_ask_free_date_repeat_18 > repeat_three_times > action_bye_12 
