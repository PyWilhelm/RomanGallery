# -*- coding: utf-8 -*-
import base64

import requests
from StringIO import StringIO

from bson.binary import Binary

from gallery.utils import db_cli, wechat


class BaseHandler(object):
    in_coll = db_cli['in_messages']
    out_coll = db_cli['out_messages']

    def __init__(self, message):
        self.msg_id = message.id
        self.source = message.source
        self.target = message.target
        self.timestamp = message.time
        self.type = message.type

    def make_meta(self):
        return {
            'msg_id': self.msg_id,
            'source': self.source,
            'target': self.target,
            'timestamp': self.timestamp,
            'type': self.type,
            'data': {},
            'response': False
        }


class TextReceiveHandler(BaseHandler):
    def __init__(self, message):
        super(TextReceiveHandler, self).__init__(message)
        self.content = message.content

    def save(self):
        meta = self.make_meta()
        meta['data'] = {'content': self.content}
        inserted_id = self.in_coll.insert_one(meta)
        return inserted_id


class ImageReceiveHandler(BaseHandler):
    image_coll = db_cli['images']

    def __init__(self, message):
        super(ImageReceiveHandler, self).__init__(message)
        self.picurl = message.picurl

    def save(self):
        meta = self.make_meta()
        image_data = requests.get(self.picurl).content
        b64_image = base64.b64encode(image_data)
        image_id = self.image_coll.insert_one({'data': b64_image, 'timestamp': self.timestamp, 'tags': []}).inserted_id
        meta['data'] = {'image': image_id}
        inserted_id = self.in_coll.insert_one(meta)
        return inserted_id, image_id


class ImageResponse(object):
    image_coll = db_cli['images']

    @classmethod
    def response(cls, image_id):
        return wechat.response_image('md1-r-JVyFBS6TCM6KBPLFrY48sBC-02e7JYPgZxw86TD6vO59x_bmCFsZp5vxbB')

        image_doc = cls.image_coll.find_one({'_id': image_id})
        if image_doc:
            image_data = base64.b64decode(image_doc['data'])
            print image_data
            resp = wechat.upload_media('image', StringIO(image_data), extension='jpg')
            response_xml = wechat.response_image(resp['media_id'])
            return response_xml
        else:
            return
