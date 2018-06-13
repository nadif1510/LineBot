from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

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
    message = TextSendMessage(text="Hello Durant")
    line_bot_api.reply_message(
        event.reply_token,
        message)
		
if MessageEvent=="MVP":
	@handler.add(MessageEvent, message=TextMessage)
def handle_message_MVP(event):
    message = TextSendMessage(text="Durant")
    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
