import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
# แก้เป็น *
from linebot.models import *

app = Flask(__name__)
# แก้ token
# get channel_secret and channel_access_token from your environment variable
channel_secret = 'a1d1185644dc263552923ce5df3a1708'
channel_access_token = '7A5fj4Wru6SpUaN9tsSJDrJYQSDILrkVLqzXZrZCaPFvQW1uH4XedhO3EsiXy5krh7jqIIEYO1BWudW8ysLW106rU5a1R6I5816I/yY9igOsKSdsGJcdBIoaruDLQdjMzW8Pw3wADsWZZ697qcWjUQdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(channel_access_token)#ตัวส่ง api
handler = WebhookHandler(channel_secret)

# แก้ route
@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):

    # line_bot_api.reply_message(
    #     event.reply_token,#ได้ reply token
    #     TextSendMessage(text=event.message.text)#ส่ง text
    # )

    text_fromuser = event.message.text #ข้อความจาก user
    Reply_token = event.reply_token
    # userid='U4dd62d9af204ed4fa2f0a3f58c47db19'

    # image_message_1 = ImageSendMessage(
    #     original_content_url='https://image.shutterstock.com/image-photo/beautiful-water-drop-on-dandelion-260nw-789676552.jpg',
    #     preview_image_url='https://image.shutterstock.com/image-photo/beautiful-water-drop-on-dandelion-260nw-789676552.jpg'
    # )

    # text_fromuser_1 = TextSendMessage(text='Pop1',quick_reply=None)
    # text_fromuser_2 = TextSendMessage(text='Pop2',quick_reply=None)

    # line_bot_api.reply_message(Reply_token,messages=[text_fromuser_1,text_fromuser_2,image_message_1])#ส่งได้ 5 ข้อความ แบบ array
    # line_bot_api.push_message(to=userid,messages=[text_fromuser_1,text_fromuser_2,image_message_1])

    if 'check' in text_fromuser:
        from Resource.bxAPI import GetBxPrice
        from random import randint
        num = randint(1,10)
        data = GetBxPrice(Number_to_get=num)
        from Resource.FlexMessage import setCarousel,setbubble
        flex = setCarousel(data)
        from Resource.reply import SetMenuMessage_Object,send_flex
        flex = SetMenuMessage_Object(flex)
        send_flex(Reply_token,file_data=flex,bot_access_key=channel_access_token)
    else:
        text_list=[
            'ฉันไม่เข้าใจที่คุณพูด กรุณารองใหม่อีกครัง','ขออภัย ฉันไม่เข้าใจจริงๆ','ขอโทษนะครับ ไม่ทราบว่ามีความหมายอย่างไรครับ','กรุณาพิมพ์ใหม่'
        ]
        from random import choice
        text_data = choice(text_list)
        text =TextSendMessage(text=text_data)
        line_bot_api.reply_message(Reply_token,text)

@handler.add(FollowEvent)
def RegisRichmenu(event):    
    userid = event.source.user_id
    disname = line_bot_api.get_profile(user_id=userid).display_name
    button_1 = QuickReplyButton(action=MessageAction(label='check',text='check'))
    button_2 = QuickReplyButton(action=MessageAction(label='เช็คข่าวสาร',text='เช็คข่าวสาร'))
    
    qbtn = QuickReply(items=[button_1,button_2])
    text = TextSendMessage(text = 'สวัดดีคุณ {} ยินดีต้อนรับสู่บริการ chatbot'.format(disname)) 
    text_2 = TextSendMessage(text = 'กรุณาเลือกเมนูที่ท่านต้องการ',quick_reply=qbtn)
    line_bot_api.reply_message(event.reply_token,messages=[text,text_2])
    line_bot_api.link_rich_menu_to_user(userid,'richmenu-f6e53f719874057846d393e99534ba09')     


if __name__ == "__main__":
    app.run(port=200)