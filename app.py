from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('uKHKLyck1PsQqJ42m+QNIxpaw54BgtPlpOVkmVmk6ZiuwJ/lbUzA6vXj53xpw2ed3w+9udkeNI6QK4kBf2KfOEP36pe+KjLTUPWLFfZyCIg/xsA5g/IPopLjoNZW4Y3HKiM77lEzSzYK50KUiDcL2gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('59e26daa3ced31f96dd879e821f2aeeb')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()