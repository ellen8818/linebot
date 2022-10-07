from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, LocationSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('9QaYCi6hofOC4yspUNWE+iEt571mSA5Ep5jXQG/GcJ0ORCwqACBn/XBAFca3qImOvG4YEPoejJ2wWYX49/QB6Fr8rp20spFNWg4ktSuC5JmWbHQPSGwPPiDmrElwrIL23yQu22RI1ITH/5eD3BARcgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('b8767d42bb0634b5618132cf492f2751')

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


def searchKey(msg):
    word = {'聯成':'電腦補習班',
            '停水水':'沒水水水',
            '美女':'蔡 慈 倫',
            '?':'呵呵',
            '幹嘛 這啥':'白癡',
            '哈囉':'你好',
            '你好':'我不好',
            '蔡慈倫':'游凱文',
            '游凱文':'蔡慈倫',
            '哈哈哈':'嘿嘿嘿',
            '你很醜':'我不知道你在說什麼?',
            '鄭佩琳':'"叫屁"',
            '林沛瑜':'長腿美女喔齁',
            '鳳梨':'藍 風 霖 黑怎樣',
            '邱冠宏':'我怎麼有點同意kevin的說法',
            'Kevin':'你姓游還是張?',
            '幹嘛':'沒事',
            '你幹嘛啦~~~':'你是一個矮冬瓜嗎',
            '喔齁齁':'ㄟ黑黑',
            '我在做家事':'我在打麻將',
            }
    return word.get(msg,msg)
    #return word.get(msg,'不知道妳再說什麼?')
 
status =0



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    global status
    msg = event.message.text
    
    if '自行車' in msg:
        station,sbi,bemp=getTPBike()
        info = ''
        for i in range(10):
            info +=station[i]+'-'+str(sbi[i])+'-'+str(bemp[i])+'\n'
        msg = info
    elif '空氣品質' in msg:
        status = 1
        msg ='請輸入地區:'
    elif '圖' in msg:
        status = 99    
    elif 'map' in msg:
        status =98
    else:
        if status ==1:
            msg = getAir(msg)
        else:
            msg = searchKey(msg)
        status = 0
    if status ==99:
        message = ImageSendMessage(original_content_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrf6XWj7zvEQJ3ut_j_F-QmiGLxVsY1i9Ehg&usqp=CAU',preview_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrf6XWj7zvEQJ3ut_j_F-QmiGLxVsY1i9Ehg&usqp=CAU')
    elif status ==98:
        message =LocationSendMessage(title='聯成逢甲',address ='台中市逢甲路',
                                     latitude=24.177879,longitude=120.642695)
    else:
        message = TextSendMessage(text=msg) #回傳文字
    
    
    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
from getBike import getTPBike
from air import getAir

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
