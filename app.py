# coding=utf8

from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from lxml import etree
import requests 
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import string
import re
import urllib.request
from random import randrange
import quickstart
from googleapiclient import discovery


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
def apple_news():
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
	day1=""
	day2=""
	for i in range(0,14,2):
		day1+=" "+day[i]
	day1=day1.split()
	for i in range(1,14,2):
		day2+=" "+day[i]
	day2=day2.split()
	for i in range(7):
		day1[i]=day1[i]+day2[i]
	for i in range(len(link)):
		link[i] = 'https://www.cwb.gov.tw'+link[i]
	for i in range(14):
		content+='{},{},{},{}\n'.format(day[i],night[i],title[i],link[i])
	return title,link,day1,night	

def sheet():
	credentials = quickstart.creds
	service = discovery.build('sheets', 'v4', credentials=credentials)
	spreadsheet_id = '1JFbvWJU1qVa8ZijU27ZlKgkobDp-meJC9makyVk1Ps8'
	range_ = 'A:C'
	major_dimension = 'COLUMNS'
	request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_, majorDimension=major_dimension)
	response = request.execute()
	return response['values'][0][0]
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	if "MVP" in event.message.text:
		message = TextSendMessage(text="Durant")
		line_bot_api.reply_message(event.reply_token,message)
	elif "@Durant昶志" in event.message.text or "打球" in event.message.text:
		message = TextSendMessage(text="拜託揪他打球，他很可憐沒球友，然後還有不要一直叫他請雞排，他很窮。")
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
		line_bot_api.reply_message(event.reply_token,LocationSendMessage(title='my location', address='台北市信義區菸廠路', latitude=25.044545, longitude=121.561457))
	elif "讚" in event.message.text :
		line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=13))
	elif event.message.text == "按鈕":
		Confirm_template = TemplateSendMessage(
		alt_text='目錄 template',
		template=ConfirmTemplate(
		title='這是ConfirmTemplate',
			text='這就是ConfirmTemplate,用於兩種按鈕選擇',
			actions=[                              
				PostbackTemplateAction(
					label='Y 這個會回傳一個值在背後',
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
	elif event.message.text == "內湖天氣":
		title1,link1,day1,night1=neihu_weather()
		Carousel_template = TemplateSendMessage(
		alt_text='Carousel template',
		template=CarouselTemplate(
		columns=[
			CarouselColumn(
				title=day1[0],
				text='白天:'+title1[0]+'\n晚上:'+title1[1],
				thumbnail_image_url=link1[0],
				actions=[
					URITemplateAction(
					label='來源網站',
					uri='https://www.cwb.gov.tw/V7/forecast/town368/7Day/6301000.htm'
				)
				]
			),
			CarouselColumn(
				title=day1[1],
				text='白天:'+title1[2]+'\n晚上:'+title1[3],
				thumbnail_image_url=link1[2],
				actions=[
					URITemplateAction(
					label='來源網站',
					uri='https://www.cwb.gov.tw/V7/forecast/town368/7Day/6301000.htm'
				)
				]
            ),
			CarouselColumn(
				title=day1[2],
				text='白天:'+title1[4]+'\n晚上:'+title1[5],
				thumbnail_image_url=link1[4],
				actions=[
					URITemplateAction(
					label='來源網站',
					uri='https://www.cwb.gov.tw/V7/forecast/town368/7Day/6301000.htm'
				)
				]
            ),
			CarouselColumn(
				title=day1[3],
				text='白天:'+title1[6]+'\n晚上:'+title1[7],
				thumbnail_image_url=link1[6],
				actions=[
					URITemplateAction(
					label='來源網站',
					uri='https://www.cwb.gov.tw/V7/forecast/town368/7Day/6301000.htm'
				)
				]
            ),
			CarouselColumn(
				title=day1[4],
				text='白天:'+title1[8]+'\n晚上:'+title1[9],
				thumbnail_image_url=link1[8],
				actions=[
					URITemplateAction(
					label='來源網站',
					uri='https://www.cwb.gov.tw/V7/forecast/town368/7Day/6301000.htm'
				)
				]
            ),
			CarouselColumn(
				title=day1[5],
				text='白天:'+title1[10]+'\n晚上:'+title1[11],
				thumbnail_image_url=link1[10],
				actions=[
					URITemplateAction(
					label='來源網站',
					uri='https://www.cwb.gov.tw/V7/forecast/town368/7Day/6301000.htm'
				)
				]
            ),
			CarouselColumn(
				title=day1[6],
				text='白天:'+title1[12]+'\n晚上:'+title1[13],
				thumbnail_image_url=link1[12],
				actions=[
					URITemplateAction(
					label='來源網站',
					uri='https://www.cwb.gov.tw/V7/forecast/town368/7Day/6301000.htm'
				)
				]
            )
		]
		)
		)
		line_bot_api.reply_message(event.reply_token,Carousel_template)	
	elif event.message.text == "電影":
		a=movie()
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
	elif event.message.text == "新聞":
		a=apple_news()
		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))
	elif event.message.text=="緯創的事":
		message = TextSendMessage(text="一日緯創人終身嚇死人")
		line_bot_api.reply_message(event.reply_token,message)
	elif event.message.text=="你":
		message = TextSendMessage(text="你他媽的閉嘴")
		line_bot_api.reply_message(event.reply_token,message)
	elif event.message.text=="少":
		message = TextSendMessage(text="少什麼少!!!老子都不老子了")
		line_bot_api.reply_message(event.reply_token,message)
	elif event.message.text=="管":
		message = TextSendMessage(text="管中閔的是你們才少管")
		line_bot_api.reply_message(event.reply_token,message)
	elif event.message.text=="你少管":
		message = TextSendMessage(text="我就住海邊阿不行嗎?")
		line_bot_api.reply_message(event.reply_token,message)
	elif event.message.text=="廖健凱":
		message = TextSendMessage(text="他會代替月亮逞罰你?")
		line_bot_api.reply_message(event.reply_token,message)
	elif event.message.text=="林昶志":
		message = TextSendMessage(text="帥哥")
		line_bot_api.reply_message(event.reply_token,message)
	elif event.message.text=="找正妹":
		message = TextSendMessage(text="帥哥")
		line_bot_api.reply_message(event.reply_token,message)
#	elif event.message.text=="sheet":
#		time,name,question=sheet()
#		a=[]
#		for i in range(len(time)):
#			a.append(time[i]+" "+name[i]+" "+question[i])
#		random_index = randrange(1,len(a))
#		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a[random_index]))
#	elif event.message.text=="表單內容":
#		a=sheet()
#		line_bot_api.reply_message(event.reply_token,TextSendMessage(text=a))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
