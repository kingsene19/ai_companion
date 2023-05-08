### Voicebot Chat App

This an app developped using Python, Rasa and Flutter which aims to perform OCR on the timetables and menus of EPT.<br/>
First we have a Python API where we have the ocr model and the text is extracted and saved in a dictionnary format which contains the relevant information pertaining 
to the classes students have each day as well as the time for which they are programmed as well as the dishes that are going to be on menu based on the day and the time..
The voicechat app is created using Flutter and we have integrated a chatbot developped with RASA which we use to awnser user inquiries.
When we have questions pertaining to a dish or class, the chatbot accesses the API to retrieve the relevant information and answers the inquiry.
