import os
import requests
import datetime
import random
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.models import (
    MessageEvent,
    TextMessage,
    ImageSendMessage,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    MessageAction,
    ImageCarouselTemplate,
    ImageCarouselColumn
)
### Read api keys
load_dotenv()
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)
apod_api = os.getenv("APOD_API_KEY", None)


def send_text_message(token, text, isReply=True):
    if isReply:
        line_bot_api.reply_message(token, TextSendMessage(text=text))
    else:
        line_bot_api.push_message(token, TextSendMessage(text=text))

    return "OK"

def send_button_template(token, text, options, isReply=True):
    actions = []
    for i in options:
        item = MessageTemplateAction(label=i, text=i)
        actions.append(item)

    if isReply:
        line_bot_api.reply_message(
            token,
            TemplateSendMessage(
                alt_text="Buttons template",
                template=ButtonsTemplate(
                    text=text,
                    actions=actions
                )
            )
        )
    else:
        line_bot_api.push_message(
            token,
            TemplateSendMessage(
                alt_text="Buttons template",
                template=ButtonsTemplate(
                    text=text,
                    actions=actions
                )
            )
        )
    return "OK"

def send_image(userid, img_urls):
    ### img_urls: list()
    line_bot_api.push_message(
        userid,
        ImageSendMessage(
            original_content_url=img_urls[0],
            preview_image_url=img_urls[1]
        )
    )

    return "OK"

def send_image_carousel(token, itemsets, isReply=True):
    ### itemsets: [ (option1, image1),  (option2, image2), ...]
    # options: string.
    # images: url string.
    columns = []
    for op, img in itemsets:
        t = ImageCarouselColumn(
            image_url=img,
            action=MessageAction(
                label=op,
                text=op,
            )
        )
        columns.append(t)

    if isReply:
        line_bot_api.reply_message(
            token,
            TemplateSendMessage(
                alt_text='ImageCarousel template',
                template=ImageCarouselTemplate(
                    columns=columns
                )
            )
        )
    else:
        line_bot_api.push_message(
            token,
            TemplateSendMessage(
                alt_text='ImageCarousel template',
                template=ImageCarouselTemplate(
                    columns=columns
                )
            )
        )



### APOD ###
def getAPODlink(date_offset=0):
    today = datetime.date.today()
    limit = 10
    content = {}
    dayshift = 0

    # Break while loop until data correct or reaching attempt limit
    for i in range(limit):
        delta = datetime.timedelta(days=date_offset+dayshift)
        date = today - delta
        url = f"https://api.nasa.gov/planetary/apod?api_key={apod_api}&date={date.isoformat()}"
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            content = r.json()
            break
        else:
            dayshift += 1

    return content, dayshift

### YT ###
def getYTlink(text):
    linkset = ["https://youtu.be/6K0K9kFDJ_I", "https://youtu.be/llje-FhGktY"]
    link = linkset[random.randint(0, len(linkset)-1)]
    return link

def getCarouselInputItem(list1, list2):
    return list(map(lambda x, y: (x, y), list1, list2))