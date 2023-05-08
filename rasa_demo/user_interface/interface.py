from tkinter import Tk, Label, Button, LabelFrame, Text
from PIL import Image, ImageTk
import sys
import speech_recognition as sr     # import the library
import pyttsx3
import requests

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voice")
engine.setProperty("voice", 'voices[1].id')


def bot_voice(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("Bot says: How may I assist you?")
        bot_voice("How may I assist you?")
        r.adjust_for_ambient_noise(source=source)
        r.energy_threshold = 150
        audio = r.listen(source)
        try:
            message = r.recognize_google(audio)
            print(f"You said: {message}")
        except Exception as e:
            print("Bot says: Sorry I did not hear your statement. Could you repeat it?")
            bot_voice("Sorry I did not hear your statement. Could you repeat it?")
    return message


def runBot():
    bot_message = ""
    while bot_message not in ["bye", "thanks", "goodbye"]:
        message = listen()
        if len(message) == 0:
            continue
        r = requests.post(
            'http://localhost:5002/webhooks/rest/webhook', json={"message": message})
        for i in r.json():
            bot_message = i['text'].lower()
            print(f"Bot says: {bot_message}")
            bot_voice(bot_message)

print("Loading the voice assistant")

class Widget:
    def __init__(self):
        root = Tk()
        root.title('Voicebot UI')
        root.geometry('840x520')

        img = ImageTk.PhotoImage(Image.open(
            r"C:/Users/Mme Sene/Desktop/English/rasa_demo/user_interface/assets/stockphoto.jpg"))
        panel = Label(root, image=img)
        panel.pack(side="right", fill="both", expand="no")

        toolbar = LabelFrame(root, text="Voicebot")
        toolbar.pack(fill="both", expand="yes")
        text = Text(toolbar, wrap="word")
        text.pack(side="top", fill="both", expand="yes")
        text.tag_configure("stderr", foreground="#b22222")

        sys.stdout = TextRedirector(text, "stdout")
        sys.stderr = TextRedirector(text, "stderr")

        btn = Button(root, text="Start", font=(
            "railways", 10, "bold"), bg="red", fg="white", command=self.clicked)
        btn.pack(fill="x", expand="no")
        btn2 = Button(root, text="Quit", font=("railways", 10, "bold"), bg="yellow",
                      fg="black", command=root.destroy)
        btn2.pack(fill="x", expand="no")

        bot_voice("Welcome I am a bot designed to help you")
        print("Welcome I am a bot designed to help you")

        root.mainloop()

    def clicked(self):
        runBot()


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")

if __name__ == "__main__":
    Widget()