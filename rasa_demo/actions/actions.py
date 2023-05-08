# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
import requests
import datetime


class ActionCheckLevel(Action):

    def name(self) -> Text:
        return "action_check_level"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        level  = next(tracker.get_latest_entity_values("level"), None).lower()
        
        if not level:
            msg = f"Which level would you like to get information about?"
            dispatcher.utter_message(text=msg)

        if not "specialization" in level and not "common" in level:
            dispatcher.utter_message(text=f"{level} is not available at ept")

        if  "common" in level:
            dispatcher.utter_message(template="utter_describe_common")

        if  "spe" in level:
            dispatcher.utter_message(template="utter_list_fields")

        return []

class ActionCheckField(Action):

    def name(self) -> Text:
        return "action_check_field"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        field  = next(tracker.get_latest_entity_values("field"), None)
        
        if not field:
            msg = f"Which field would you like to get information about?"
            dispatcher.utter_message(text=msg)

        if "computer" in field:
            dispatcher.utter_message(template="utter_describe_fields/git")
        elif "civil" in field:
            dispatcher.utter_message(template="utter_describe_fields/gc")
        elif "mecha" in field:
            dispatcher.utter_message(template="utter_describe_fields/gem")
        elif "industrial" in field:
            dispatcher.utter_message(template="utter_describe_fields/gi")
        elif "aero" in field:
            dispatcher.utter_message(template="utter_describe_fields/ga")
        else:
            dispatcher.utter_message(text=f"{field} is not available at EPT")

        return []

class ActionUtterOverview(Action):

    def name(self) -> Text:
        return "action_utter_menu_overview"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        API_URL = "http://localhost:5000/get_menu"
        menu = requests.get(API_URL).json()
        message = ""
        for day, dayMenu in menu.items():
            meals_time = []
            meals = []
            for meal_time, meal in dayMenu.items():
                key = day
                meals_time.append(meal_time)
                meals.append(meal.replace("/"," or"))
            message = message + f"On {key} there is {meals[0]} for {meals_time[0]} and for {meals_time[1]} there is {meals[1]} "
        dispatcher.utter_message(message)

        return []
    
class ActionMealsDay(Action):

    def name(self) -> Text:
        return "action_utter_meals_day"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        target_day  = next(tracker.get_latest_entity_values("day"), None).capitalize()

        days = ["Monday", "Tuesday", "Wednesday", "Thrusday", "Friday", "Saturday", "Sunday"]
        today = datetime.datetime.today().weekday()

        if target_day in ["today", "Today"]:
            target_day = days[today]

        if target_day in ["tomorrow", "Tomorrow"]:
            target_day = days[today + 1]

        if target_day in ["yesterday", "Yesterday"]:
            target_day = days[today - 1]

        if not target_day in days:
            msg = f"{target_day} is not a valid day of the week"
            dispatcher.utter_message(text=msg)

        API_URL = "http://localhost:5000/get_menu"
        menu = requests.get(API_URL).json()
        message = ""
        for day, dayMenu in menu.items():
            if day.lower() == target_day.lower():
                meals_time = []
                meals = []
                for meal_time, meal in dayMenu.items():
                    key = day
                    meals_time.append(meal_time)
                    meals.append(meal.replace("/"," or "))
                message = message + f"On {key} there is {meals[0]} for {meals_time[0]} and for {meals_time[1]} there is {meals[1]} "
        dispatcher.utter_message(message)

        return []
    

class ActionMealDay(Action):

    def name(self) -> Text:
        return "action_utter_meal_day"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        target_day  = next(tracker.get_latest_entity_values("day"), None).capitalize()
        target_meal_time = next(tracker.get_latest_entity_values("meal_time"), None)

        days = ["Monday", "Tuesday", "Wednesday", "Thrusday", "Friday", "Saturday", "Sunday"]
        today = datetime.datetime.today().weekday()

        target_dict = {
            "lunch": "lunch",
            "Lunch": "lunch",
            "Dinner": "dinner",
            "dinner": "dinner"
        }

        if target_day in ["today", "Today"]:
            target_day = days[today]

        if target_day in ["tomorrow", "Tomorrow"]:
            target_day = days[today + 1]

        if target_day in ["yesterday", "Yesterday"]:
            target_day = days[today - 1]

        if not target_day in days:
            msg = f"{target_day} is not a valid day of the week"
            dispatcher.utter_message(text=msg)

        if not target_meal_time in ['lunch', 'dinner', 'Lunch', 'Dinner']:
            msg = f"{target_meal_time} is not a valid meal time"
            dispatcher.utter_message(text=msg)

        API_URL = "http://localhost:5000/get_menu"
        menu = requests.get(API_URL).json()
        message = ""
        for day, dayMenu in menu.items():
            if day.lower() == target_day.lower():
                for meal_time, meal in dayMenu.items():
                    if meal_time == target_dict[target_meal_time]:
                        key = day
                        message = message + f"On {key} there is {meal} for {meal_time} "
        dispatcher.utter_message(message)

        return []
    
class ActionMeals(Action):

    def name(self) -> Text:
        return "action_utter_meals"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        target_meal_time = next(tracker.get_latest_entity_values("meal_time"), None)

        target_dict = {
            "lunches": "lunch",
            "Lunches": "lunch",
            "Dinners": "dinner",
            "dinners": "dinner"
        }

        if not target_meal_time in ['lunches', 'dinners', 'Lunches', 'Dinners']:
            msg = f"{target_meal_time} is not a valid meal time"
            dispatcher.utter_message(text=msg)

        API_URL = "http://localhost:5000/get_menu"
        menu = requests.get(API_URL).json()
        message = ""
        for day, dayMenu in menu.items():
            for meal_time, meal in dayMenu.items():
                if meal_time == target_dict[target_meal_time]:
                    key = day
                    message = message + f"On {key} there is {meal} "
        dispatcher.utter_message(message)

        return []
    
class ActionSpecificMeal(Action):

    def name(self) -> Text:
        return "action_utter_specific_meal"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        target_meal = next(tracker.get_latest_entity_values("meal"), None)

        API_URL = "http://localhost:5000/get_menu"
        menu = requests.get(API_URL).json()
        message = f"{target_meal} is available "
        for day, dayMenu in menu.items():
            for meal_time, meal in dayMenu.items():
                if meal.lower().find(target_meal.lower()) != -1:
                    key = day
                    message = message + f"on {key} for {meal_time} "

        if message != f"{target_meal} is available ":
            dispatcher.utter_message(message)
        else:
            dispatcher.utter_message(f"{target_meal} is not on the menu")

        return []

class ActionCheckIntentAndRespond(Action):
    def name(self) -> Text:
        return "action_check_current_intent_and_respond"
    
    def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_intent = tracker.get_intent_of_latest_message()

        API_URL = f"http://localhost:5000/get_schedule?classe=dic2&field=git"
        schedule = requests.get(API_URL).json()

        print(schedule)
        
        days = ["Monday", "Tuesday", "Wednesday", "Thrusday", "Friday", "Saturday", "Sunday"]
        today = datetime.datetime.today().weekday()

        times= {
            "afternoon": ['08', '09', '10', '11', '12'],
            "morning": ['15', '16', '17', '18', '19']
        }

        # works
        if current_intent == "ask_schedule_overview":
            message = ""
            for day, daySchedule in schedule.items():
                classes = {}
                for hour, classe in daySchedule.items():
                    if classe not in classes.keys():
                        classes[classe] = {"start": hour, "end": ""}
                    if classe in classes.keys():
                        classes[classe]["end"] = hour
                if len(classes.keys()) > 1:
                    message += f"On {day}"
                    for key in classes.keys():
                        if key == "":
                            message += f" free time {calculate_duration(classes[key])} then "
                        else:
                            message += f" {key} {calculate_duration(classes[key])} then "
                else:
                    for key in classes.keys():
                        if key == "":
                            message += f"On {day} free time {calculate_duration(classes[key])} "
                        else:
                            message += f"On {day} {key} {calculate_duration(classes[key])} "

        # works
        if current_intent == "ask_subjects_day":
            target_day = next(tracker.get_latest_entity_values("day"), None).capitalize()

            if target_day in ["today", "Today"]:
                target_day = days[today]

            if target_day in ["tomorrow", "Tomorrow"]:
                target_day = days[today + 1]

            if target_day in ["yesterday", "Yesterday"]:
                target_day = days[today - 1]

            if not target_day in days[:-1]:
                msg = f"{target_day} is not a valid day of the week"
                dispatcher.utter_message(text=msg)

            message = ""
            classes = {}
            for day, daySchedule in schedule.items():
                for hour, classe in daySchedule.items():
                    if day.lower() == target_day.lower():
                        if classe not in classes.keys():
                            classes[classe] = {"start": hour, "end": ""}
                        if classe in classes.keys():
                            classes[classe]["end"] = hour
                if day.lower() == target_day.lower():
                    if len(classes.keys()) > 1:
                        message += f"On {day}"
                        for key in classes.keys():
                            if key == "":
                                message += f" free time {calculate_duration(classes[key])} then "
                            else:
                                message += f" {key} {calculate_duration(classes[key])} then "
                    else:
                        for key in classes.keys():
                            if key == "":
                                message += f"On {day} free time {calculate_duration(classes[key])} "
                            else:
                                message += f"On {day} {key} {calculate_duration(classes[key])} "

        if current_intent == "ask_subjects_specific_time":
            target_day = next(tracker.get_latest_entity_values("day"), None).capitalize()
            target_time = next(tracker.get_latest_entity_values("subject_time"), None)

            ALLOWED_TIMES = ['08', '09', '10', '11', '12', '15', '16', '17', '18', '19']

            if target_day in ["today", "Today"]:
                target_day = days[today]

            if target_day in ["tomorrow", "Tomorrow"]:
                target_day = days[today + 1]

            if target_day in ["yesterday", "Yesterday"]:
                target_day = days[today - 1]

            if not target_day in days[:-1]:
                msg = f"{target_day} is not a valid day of the week"
                dispatcher.utter_message(text=msg)
            
            if target_time in ["Afternoon", "afternoon", "Morning", "morning"]:
                limit_start = times[target_time.lower()][0]
                limit_end = times[target_time.lower()][-1]
            elif target_time in ALLOWED_TIMES:
                index = ALLOWED_TIMES.index(target_time)
                limit_start = ALLOWED_TIMES[index]
                limit_end =ALLOWED_TIMES[index+1]
            else:
                msg = f"{target_time} is not a valid time option. Options are {ALLOWED_TIMES}"
                dispatcher.utter_message(text=msg)

            message = ""
            classes = {}
            for day, daySchedule in schedule.items():
                for hour, classe in daySchedule.items():
                    if day.lower() == target_day.lower():
                        if classe not in classes.keys():
                            classes[classe] = {"start": hour, "end": ""}
                        if classe in classes.keys():
                            classes[classe]["end"] = hour
                if day.lower() == target_day.lower():
                    if len(classes.keys()) > 1:
                        for key in classes.keys():
                            if key == "":
                                if int(limit_start) in calculate_range(classes[key]) or int(limit_end) in calculate_range(classes[key]) :
                                    message += f"{day} free time {calculate_duration(classes[key])} "
                            else:
                                if int(limit_start) in calculate_range(classes[key]) or int(limit_end) in calculate_range(classes[key]) :
                                    message += f"{day} {key} {calculate_duration(classes[key])} "
                    else:
                        for key in classes.keys():
                            if key == "":
                                if int(limit_start) in calculate_range(classes[key]) or int(limit_end) in calculate_range(classes[key]) :
                                    message += f"{day} free time {calculate_duration(classes[key])} "
                            else:
                                if int(limit_start) in calculate_range(classes[key]) or int(limit_end) in calculate_range(classes[key]) :
                                    message += f"{day} {key} {calculate_duration(classes[key])} "

        # works
        if current_intent == "ask_times_subjects":
            target_subject = next(tracker.get_latest_entity_values("subject"), None).title()

            message = ""
            for day, daySchedule in schedule.items():
                classes = {}
                for hour, classe in daySchedule.items():
                    if classe not in classes.keys():
                        classes[classe] = {"start": hour, "end": ""}
                    if classe in classes.keys():
                        classes[classe]["end"] = hour
                if len(classes.keys()) > 1:
                    for key in classes.keys():
                        if target_subject.lower() in key.lower():
                            message += f"On {day} we have {target_subject} {calculate_duration(classes[key])} "
                else:
                    for key in classes.keys():
                        if target_subject.lower() in key.lower():
                            message += f"On {day} we have {target_subject} {calculate_duration(classes[key])} "
            if message == "":
                message = f"{target_subject} is not on the schedule"
            else:
                message += f" for a total of {message.count(target_subject)} times"

        if current_intent == "ask_exam_time":
            time_type = next(tracker.get_latest_entity_values("time_type"), None)

            ALLOWED_TYPES = ["free", "exam", "exams", "free"]

            if time_type not in ALLOWED_TYPES:
                msg = f"{time_type} not in options. The options are {ALLOWED_TYPES}"
                dispatcher.utter_message(text=msg)

            message = ''
            for day, daySchedule in schedule.items():
                classes = {}
                for hour, classe in daySchedule.items():
                    if classe not in classes.keys():
                        classes[classe] = {"start": hour, "end": ""}
                    if classe in classes.keys():
                        classes[classe]["end"] = hour
                if len(classes.keys()) > 1:
                    for key in classes.keys():
                        if "free" in time_type:
                            if key == "":
                                message += f"On {day} free time {calculate_duration(classes[key])} "
                        if "exam" in time_type:
                            if "Evaluation" in key:
                                message += f"On {day} {key} {calculate_duration(classes[key])} "
                else:
                    for key in classes.keys():
                        if "free" in time_type:
                            if key == "":
                                message += f"On {day}  free time {calculate_duration(classes[key])} "
                        if "exam" in time_type:
                            if "Evaluation" in key:
                                message += f"On {day} {key} {calculate_duration(classes[key])} "
            if message == "":
                message = f"There is no {time_type} on the schedule"
            if "Evaluation" in message:
                message = "There are these exams " + message

        dispatcher.utter_message(text=message)

        return []
    
def calculate_duration(dic):
  start = dic["start"][0:2]
  end = dic["end"][-3:-1]
  duration = f"from {start} to {end}"
  return duration

def calculate_range(dic):
  start = int(dic["start"][0:2])
  end = int(dic["end"][-3:-1])
  return  range(start, end+1)
