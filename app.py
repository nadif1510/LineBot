from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageSendMessage)
from linebot.models import *



app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Khr3Dfs1gykCRh/2Nz14dRK2jpLRggpN0wp9zM7TRF8wtpIS2WiMufC1t9SPDrycfpfwFDO+LLp5f+VMiiYnvFZuxHJxu06UVHxTA40BkrHawOvcIPrxUsXUaI4FoGbUW+Y0AMtiocjZH15pYhhdSAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('98bdd4462c58d1b3b61f77b22f196ec5')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
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
def handle_message(event):
	if event.message.text=="MVP":
		message = TextSendMessage(text="Durant")
		line_bot_api.reply_message(event.reply_token,message)
	elif event.message.text=="Durant昶志":
		message = TextSendMessage(text="拜託揪他打球，他很可憐沒球友")
		line_bot_api.reply_message(event.reply_token,message)
	elif event.message.text=="抽":
		message = ImageSendMessage(
		original_content_url='https://i.imgur.com/8sNfqJl.jpg',
		preview_image_url='https://i.imgur.com/ebLtiKR.jpg')
		line_bot_api.reply_message(event.reply_token, message)
	elif event.message.text=="uat":
		message = TextSendMessage(text="帳號cmtest001~003\n密碼Heaven@4394")
		line_bot_api.reply_message(event.reply_token,message)
	elif event.message.text=="按鈕":
		message = TemplateSendMessage(
			alt_text='Buttons template',
			template=ButtonsTemplate(
				thumbnail_image_url='http://i.imgur.com/AJKHnvf.jpg',
				title='Menu',
				text='Please select',
				actions=[
					PostbackTemplateAction(
						label='postback',
						text='postback text',
						data='action=buy&itemid=1'
					),
					MessageTemplateAction(
						label='message',
						text='message text'
					),
					URITemplateAction(
						label='uri',
						uri='http://yahoo.com/'
					)
				]
			)
		)		
		line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
