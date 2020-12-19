import os
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)

load_dotenv()
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)


def send_text_message(token, text, isReply=True):
    if isReply:
        line_bot_api.reply_message(token, TextSendMessage(text=text))
    else:
        line_bot_api.push_message(token, TextSendMessage(text=text))

    return "OK"

def send_button_template(reply_token, text, options):
    actions = []
    for i in options:
        item = MessageTemplateAction(label=i, text=i)
        actions.append(item)
    line_bot_api.reply_message(
        reply_token,
        TemplateSendMessage(
            alt_text="Buttons template",
            template=ButtonsTemplate(
                text=text,
                actions=actions
            )
        )
    )

    return "OK"


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""

### APOD ###
def getAPODlink(date_offset=0):
    return f"<url> {date_offset}"


### YT ###
def getYTlink(word1):
    return word1 + " <url>"