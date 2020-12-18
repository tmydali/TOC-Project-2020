from transitions.extensions import GraphMachine
import json

from utils import send_text_message

def getAPODlink(date_offset=0):
    return f"<url> {date_offset}"

def getYTlink(word1):
    return word1 + " <url>"

class AstroMindMachine(GraphMachine):

    date_offset = 0
    scenario = {}

    def __init__(self, **machine_configs):
        super().__init__(model=self, **machine_configs)
        with open("scenario.json", encoding="utf-8") as f:
            self.scenario = json.load(f)

    # Behavior on transitions
    def on_enter_Q1(self, event):
        q = self.scenario["Q1"]["content"]
        print(q)

    def on_enter_Q2_1(self, event):
        q = self.scenario["Q2"]["content"]
        print(q)

    def on_enter_Q2_2(self, event):
        q = self.scenario["Q2"]["content"]
        print(q)

    def on_enter_Q2_3(self, event):
        q = self.scenario["Q2"]["content"]
        print(q)

    def on_exit_Q2_1(self, event):
        word1 = self.scenario["Q1"]["options"][0]
        data = event.postback.data
        tokens = data.split("&!")
        word2 = tokens[-1]
        reply = self.scenario["Q2"]["template"].format(word1, word2)
        print(reply)

    def on_exit_Q2_2(self, event):
        word1 = self.scenario["Q1"]["options"][1]
        data = event.postback.data
        tokens = data.split("&!")
        word2 = tokens[-1]
        reply = self.scenario["Q2"]["template"].format(word1, word2)
        print(reply)

    def on_exit_Q2_3(self, event):
        word1 = self.scenario["Q1"]["options"][2]
        data = event.postback.data
        tokens = data.split("&!")
        word2 = tokens[-1]
        reply = self.scenario["Q2"]["template"].format(word1, word2)
        print(reply)

    def on_enter_APOD(self, event):
        data = event.postback.data
        tokens = data.split("&!")
        option = tokens[-1]
        if option == self.scenario["APOD"]["options"][0]:
            print("How about this?")
        img_link = getAPODlink(self.date_offset)
        print(img_link)

    def on_enter_Q3(self, event):
        q = self.scenario["Q3"]["content"]
        print(q)

    def on_exit_Q3(self, event):
        data = event.postback.data
        tokens = data.split("&!")
        word1 = tokens[-1]
        reply = self.scenario["Q3"]["template"].format(word1)
        link = getYTlink(word1)
        print(reply)
        print(link)

    def on_enter_End(self, event):
        q = self.scenario["End"]["content"]
        print(q)

    # Conditions
    def isOption1(self, event):
        data = event.postback.data
        tokens = data.split("&!")
        options = self.scenario["Q1"]["options"]
        return tokens[-1] == options[0]

    def isOption2(self, event):
        data = event.postback.data
        tokens = data.split("&!")
        options = self.scenario["Q1"]["options"]
        return tokens[-1] == options[1]

    def isOption3(self, event):
        data = event.postback.data
        tokens = data.split("&!")
        options = self.scenario["Q1"]["options"]
        return tokens[-1] == options[2]

    def isQ2Option(self, event):
        data = event.postback.data
        tokens = data.split("&!")
        options = self.scenario["Q2"]["options"]
        return tokens[-1] in options

    def isQ3Option(self, event):
        data = event.postback.data
        tokens = data.split("&!")
        options = self.scenario["Q3"]["options"]
        return tokens[-1] in options

    def isToStart(self, event):
        text = event.message.text
        options = self.scenario["End"]["options"]
        return text in options

    def isAPODOption(self, event):
        text = event.message.text
        options = self.scenario["APOD"]["options"]
        return text in options

def FSMInitialize():
    machine = AstroMindMachine(
        states=["User", "Q1", "Q2_1", "Q2_2", "Q2_3", "APOD", "Q3", "End"],
        transitions=[
            ### Normal flow ###
            # Psycho quiz
            {
                "trigger": "advance",
                "source": "User",
                "dest": "Q1",
                "conditions": "isToStart"
            },
            {
                "trigger": "advance",
                "source": "Q1",
                "dest": "Q2_1",
                "conditions": "isOption1"
            },
            {
                "trigger": "advance",
                "source": "Q1",
                "dest": "Q2_2",
                "conditions": "isOption2"
            },
            {
                "trigger": "advance",
                "source": "Q1",
                "dest": "Q2_3",
                "conditions": "isOption3"
            },

            # Astronomical pictures
            {
                "trigger": "advance",
                "source": ["Q2_1", "Q2_2", "Q2_3"],
                "dest": "APOD",
                "conditions": "isQ2Option"
            },
            {
                "trigger": "advance",
                "source": "APOD",
                "dest": "APOD",
                "conditions": "isAPODOption"
            },
            # YT Recommendation
            {
                "trigger": "advance",
                "source": "APOD",
                "dest": "Q3",
            },
            {
                "trigger": "advance",
                "source": "Q3",
                "dest": "End",
                "conditions": "isQ3Option"
            },
            {
                "trigger": "advance",
                "source": "End",
                "dest": "Q1",
                "conditions": "isToStart"
            },

            ### Escape ###
            {
                "trigger": "exit",
                "source": "*",
                "dest": "End"
            },
        ],
        initial="User",
        auto_transitions=False,
        show_conditions=True,
    )
    return machine


if __name__ == "__main__":
    class Postback:
        data = ''
    class Mesg:
        text = ''
    class Event:
        postback = Postback()
        message = Mesg()

    machine = FSMInitialize()
    ev = Event()

    while(1):
        text = input("Wait for input: ")
        ev.message.text = text
        ev.postback.data = "A01&!" + text
        machine.advance(ev)
