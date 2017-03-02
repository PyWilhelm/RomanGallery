# -*- coding: utf-8 -*-
from flask import request
from wechat_sdk.messages import TextMessage, ImageMessage, VoiceMessage, LinkMessage

from gallery.handler import TextReceiveHandler, ImageReceiveHandler, ImageResponse
from gallery.main import app
from gallery.utils import wechat


@app.route('/wx', methods=['GET', 'POST'])
def main_handler():
    signature = request.args.get('signature')
    msg_signature = request.args.get('msg_signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    if not wechat.check_signature(signature, timestamp, nonce):
        return
    if request.method == 'GET':
        return request.args.get('echostr')
    if request.method == 'POST':
        wechat.parse_data(request.data, msg_signature=msg_signature, timestamp=timestamp, nonce=nonce)
        message = wechat.message
        print message.raw
        if isinstance(message, TextMessage):
            TextReceiveHandler(message)
            response = ImageResponse.response('')
            return response
        elif isinstance(message, ImageMessage):
            _, image_id = ImageReceiveHandler(message).save()
            print('saved')
            response = ImageResponse.response(image_id)
            print response
            return response or 'success'
        return 'success'
