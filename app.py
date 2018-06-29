# coding=utf8

from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from lxml import etree
import requests 
from bs4 import BeautifulSoup
from urllib.request import urlretrieve



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

def movie():
	target_url = 'https://movies.yahoo.com.tw/'
	rs = requests.session()
	res = rs.get(target_url, verify=False)
	res.encoding = 'utf-8'
	soup = BeautifulSoup(res.text, 'html.parser')   
	content = ""
	for index, data in enumerate(soup.select('div.movielist_info h1 a')):
		if index ==15 :
			return content
		print(data)
		title = data.text
		link = data['href']
		content+='{}\n{}\n'.format(title,link)
		#content+=link
	return content

def apple_news2():
	target_url = 'https://tw.appledaily.com/new/realtime'
	rs = requests.session()
	res = rs.get(target_url, verify=False)
	res.encoding = 'utf-8'
	soup = BeautifulSoup(res.text, 'html.parser')   
	content = ""
	for index, data in enumerate(soup.select('div.item a')):
		if index ==15:           
			return content
		print(data)  
		title = data.find('img')['alt']
		link =  data['href']
		link2 = 'https:'+ data.find('img')['data-src']
		#content+='{}\n{}\n{}\n'.format(title,link,link2)
		content+='{}\n{}\n'.format(title,link)
	return content

	target_url = 'https://www.cwb.gov.tw/V7/forecast/town368/7Day/6301000.htm'
	rs = requests.session()
	res = rs.get(target_url, verify=False)
	res.encoding = 'utf-8'
	soup = BeautifulSoup(res.text, 'html.parser')
	print(res.text)
	content = ""
	for data in enumerate(soup.select('td img')):
		print(data)
		title = data.find['alt']
		#if title !="":
		#	link = 'https:' + data.find('img')['src']
		#content+='{}\n{}\n'.format(title,link)
		content+=title
	return content
def neihu_weather():
	target_url = 'https://www.cwb.gov.tw/V7/forecast/town368/7Day/6301000.htm'
	rs = requests.session()
	res = rs.get(target_url, verify=False)
	res.encoding = 'utf-8'
	selector = etree.HTML(res.text)
	content = ""
	title = selector.xpath('//img/@title')
	link = selector.xpath('//img[@title]/@src')
	day = selector.xpath('//td[text()="日期"]/../td[@colspan]//text()')
	night = selector.xpath('//td[text()="時間"]/../*[text()!="時間"]//text()')
	for i in range(len(link)):
		link[i] = 'https://www.cwb.gov.tw'+link[i]
	for i in range(14):
		content+='{},{},{},{}\n'.format(day[i],night[i],title[i],link[i])
	return content
	
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
	elif event.message.text == "位置":
		line_bot_api.reply_message(event.reply_token,LocationSendMessage(title='my location', address='Tainan', latitude=22.994821, longitude=120.196452))
	elif event.message.text == "貼圖":
		line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=2))
	elif event.message.text == "Buttons Template":
		buttons_template = TemplateSendMessage(
		alt_text='Buttons Template',
		template=ButtonsTemplate(
			title='這是ButtonsTemplate',
			text='ButtonsTemplate可以傳送text,uri',
			thumbnail_image_url='https://i.imgur.com/ebLtiKR.jpg',
			actions=[
				MessageTemplateAction(
					label='ButtonsTemplate',
					text='抽'
				),
				URITemplateAction(
					label='VIDEO1',
					uri='https://i.imgur.com/ebLtiKR.jpg'
				),
				PostbackTemplateAction(
					label='postback',
					text='postback text',
					data='postback1'
				)
			]
			)
		)
		line_bot_api.reply_message(event.reply_token, buttons_template)
	elif event.message.text == "Confirm template":
		print("Confirm template")       
		Confirm_template = TemplateSendMessage(
		alt_text='目錄 template',
		template=ConfirmTemplate(
		title='這是ConfirmTemplate',
			text='這就是ConfirmTemplate,用於兩種按鈕選擇',
			actions=[                              
				PostbackTemplateAction(
					label='Y',
					text='Y',
					data='action=buy&itemid=1'
				),
				MessageTemplateAction(
					label='N',
					text='N'
                )
			]
			)
		)
		line_bot_api.reply_message(event.reply_token,Confirm_template)
	elif event.message.text == "Carousel template":
		Carousel_template = TemplateSendMessage(
		alt_text='Carousel template',
		template=CarouselTemplate(
		columns=[
			CarouselColumn(
				thumbnail_image_url='https://i.imgur.com/8sNfqJl.jpg',
				title='this is menu1',
				text='description1',
				actions=[
					PostbackTemplateAction(
						label='postback1',
						text='postback text1',
						data='action=buy&itemid=1'
					),
					MessageTemplateAction(
						label='message1',
						text='message text1'
					),
					URITemplateAction(
						label='uri1',
						uri='http://example.com/1'
					)
				]
			),
			CarouselColumn(
				thumbnail_image_url='https://i.imgur.com/8sNfqJl.jpg',
				title='this is menu2',
				text='description2',
				actions=[
					PostbackTemplateAction(
						label='postback2',
						text='postback text2',
						data='action=buy&itemid=2'
					),
					MessageTemplateAction(
						label='message2',
						text='message text2'
					),
					URITemplateAction(
						label='連結2',
						uri='http://example.com/2'
					)
				]
            )
        ]
		)
		)
		line_bot_api.reply_message(event.reply_token,Carousel_template)
		
	elif event.message.text == "最新電影":
		a=movie()
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
	elif event.message.text == "最新新聞":
		a=apple_news2()
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
	elif event.message.text == "內湖天氣預報":
		print('內湖天氣預報')
		a=neihu_weather()
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))		
		
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
