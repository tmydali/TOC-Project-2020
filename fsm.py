from transitions import Machine
from transitions.extensions import GraphMachine
import json
from utils import getAPODlink, getYTlink, getCarouselInputItem
from utils import send_text_message, send_button_template, send_image, send_image_carousel


class AstroMindMachine(Machine):

    date_offset = 0
    scenario = {}

    def __init__(self, **machine_configs):
        super().__init__(model=self, **machine_configs)
        with open("scenario.json", encoding="utf-8") as f:
            self.scenario = json.load(f)

    # Behavior on transitions
    def on_enter_Q1(self, event):
        q = self.scenario["Q1"]["content"]
        t = self.scenario["Q1"]["title"]
        send_button_template(event.reply_token, q, t, self.scenario["Q1"]["options"])
        print(q)

    def on_enter_Q2_1(self, event):
        q = self.scenario["Q2"]["content"]
        t = self.scenario["Q2"]["title"]
        send_button_template(event.reply_token, q, t, self.scenario["Q2"]["options"])
        print(q)

    def on_enter_Q2_2(self, event):
        q = self.scenario["Q2"]["content"]
        t = self.scenario["Q2"]["title"]
        send_button_template(event.reply_token, q, t, self.scenario["Q2"]["options"])
        print(q)

    def on_enter_Q2_3(self, event):
        q = self.scenario["Q2"]["content"]
        t = self.scenario["Q2"]["title"]
        send_button_template(event.reply_token, q, t, self.scenario["Q2"]["options"])
        print(q)

    def on_exit_Q2_1(self, event):
        if event.message.text == self.scenario["Escape"]["exit"]:
            return

        word2 = event.message.text
        t_index = 0
        for i in range(len(self.scenario["Q2"]["options"])):
            if word2 == self.scenario["Q2"]["options"][i]:
                t_index += i
                break
        reply = self.scenario["Q2"]["template"][t_index]
        send_text_message(event.reply_token, reply)
        print(reply)

    def on_exit_Q2_2(self, event):
        if event.message.text == self.scenario["Escape"]["exit"]:
            return

        word2 = event.message.text
        t_index = 1 * len(self.scenario["Q2"]["options"])
        for i in range(len(self.scenario["Q2"]["options"])):
            if word2 == self.scenario["Q2"]["options"][i]:
                t_index += i
                break
        reply = self.scenario["Q2"]["template"][t_index]
        send_text_message(event.reply_token, reply)
        print(reply)

    def on_exit_Q2_3(self, event):
        if event.message.text == self.scenario["Escape"]["exit"]:
            return

        word2 = event.message.text
        t_index = 2 * len(self.scenario["Q2"]["options"])
        for i in range(len(self.scenario["Q2"]["options"])):
            if word2 == self.scenario["Q2"]["options"][i]:
                t_index += i
                break
        reply = self.scenario["Q2"]["template"][t_index]
        send_text_message(event.reply_token, reply)
        print(reply)

    def on_enter_APOD(self, event):
        option = event.message.text
        user_id = event.source.user_id

        if option == self.scenario["APOD"]["options"][0]:
            self.date_offset += 1
            data, dayshift = getAPODlink(self.date_offset)
            self.date_offset += dayshift
            txt = self.scenario["APOD"]["template"]["dislike"]
            txt.format(title=data["title"])
            send_text_message(user_id, txt, False)
            send_image(user_id, [data["hdurl"], data["url"]])
            txt = self.scenario["APOD"]["template"]["date"]
            txt = txt.format(title=data["title"], explanation=data["explanation"], date=data["date"])
            send_text_message(user_id, txt, False)

            print(txt)
        else:
            data, dayshift = getAPODlink(self.date_offset)
            self.date_offset += dayshift
            send_image(user_id, [data["hdurl"], data["url"]])
            txt = self.scenario["APOD"]["template"]["default"]
            txt = txt.format(title=data["title"], explanation=data["explanation"])
            send_text_message(user_id, txt, False)
            print(txt)

        q = self.scenario["APOD"]["content"]
        options = self.scenario["APOD"]["options"]
        t = self.scenario["APOD"]["title"]
        send_button_template(user_id, q, t, options, False)

    def on_enter_Q3(self, event):
        q = self.scenario["Q3"]["content"]
        send_text_message(event.reply_token, q)
        itemset = getCarouselInputItem(
            self.scenario["Q3"]["options"],
            self.scenario["Q3"]["images"]
        )
        user_id = event.source.user_id
        send_image_carousel(user_id, itemset, False)
        print(q)

    def on_exit_Q3(self, event):
        if event.message.text == self.scenario["Escape"]["exit"]:
            return

        data = event.message.text
        person, link = getYTlink(data)
        reply = self.scenario["Q3"]["template"].format(data, person, link)
        send_text_message(event.reply_token, reply)
        print(reply)

    def on_enter_End(self, event):
        q = self.scenario["End"]["content"]
        user_id = event.source.user_id
        send_text_message(user_id, q, False)
        print(q)

    # Conditions
    def isOption1(self, event):
        data = event.message.text
        options = self.scenario["Q1"]["options"]
        return data == options[0]

    def isOption2(self, event):
        data = event.message.text
        options = self.scenario["Q1"]["options"]
        return data == options[1]

    def isOption3(self, event):
        data = event.message.text
        options = self.scenario["Q1"]["options"]
        return data == options[2]

    def isQ2Option(self, event):
        data = event.message.text
        options = self.scenario["Q2"]["options"]
        return data in options

    def isQ3Option(self, event):
        data = event.message.text
        options = self.scenario["Q3"]["options"]
        return data in options

    def isToStart(self, event):
        text = event.message.text
        options = self.scenario["End"]["options"]
        return text in options

    def isAPODOption(self, event):
        text = event.message.text
        options = self.scenario["APOD"]["options"]
        return text in options

    def isDislike(self, event):
        text = event.message.text
        options = self.scenario["APOD"]["options"]
        return text == options[0]

    def isDislike2(self, event):
        text = event.message.text
        options = self.scenario["APOD"]["options"]
        return text == options[1]

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
                "conditions": ["isAPODOption", "isDislike"]
            },
            # YT Recommendation
            {
                "trigger": "advance",
                "source": "APOD",
                "dest": "Q3",
                "conditions": ["isAPODOption", "isDislike2"]
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
        #show_conditions=True,
    )
    return machine

### User priority queue. Use Least Recently Used(LRU) policy ###
class Lru_queue():
    Uqueue = []
    MachineDict = {}
    counter = 0

    def __init__(self, maxUser=50):
        self.maxUser = maxUser

    def push(self, uid):
        if self.counter < self.maxUser:
            self.Uqueue.append(uid)
            self.MachineDict[uid] = FSMInitialize()
            self.counter += 1
        else:
            self.handleFull(uid)

    def handleFull(self, push_uid):
        pop_uid = self.Uqueue.pop(0)
        self.Uqueue.append(push_uid)
        self.MachineDict.pop(pop_uid)
        self.MachineDict[push_uid] = FSMInitialize()
        text = f"由於你閒置太久，所以你的狀態被刪掉了，輸入「開始」重新來一次吧"
        send_text_message(pop_uid, text, False)

    def getUserMachine(self, uid):
        try:
            Uindex = self.Uqueue.index(uid)
            pop = self.Uqueue.pop(Uindex)
            self.Uqueue.append(pop)

        except:
            self.push(uid)

        return self.MachineDict[uid]


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
        machine.advance(ev)
