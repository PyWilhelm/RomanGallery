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
            'response': False,
            'tags': []
        }


class TextReceiveHandler(BaseHandler):
    def __init__(self, message):
        super(TextReceiveHandler, self).__init__(message)
        self.content = message.content

    def save(self):
        meta = self.make_meta()
        lines = self.content.split('\n')
        title = lines[0].strip()
        if title.find(u'写给') == 0:
            content = '\n'.join(lines[1:])
            meta['data'] = {'type': 'letter', 'content': content, 'title': title}
            self.in_coll.insert_one(meta)

        elif title.find(u'标签') == 0:
            tags = title.split(' ')[1:]
            item = self.in_coll.find().sort({'timestamp': -1}).limit(1)[0]
            self.in_coll.update({'_id': item['_id']}, {'tags': tags})


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


class Response(BaseHandler):

    def __init__(self, message):
        super(Response, self).__init__(message)

        content = message.content.strip()
        if content.find(u'想看留言') == 0:
            item = self.in_coll.find({'data.type': 'message', 'response': False}).sort({'timestamp': -1}).limit(1)[0]
            resp_content = item['data']['content']
            resp_type = 'message'
            self.in_coll.update({'_id': item['_id']}, {'response': True})


        elif content.find(u'想看信') == 0:
            item = self.in_coll.find({'data.type': 'letter', 'response': False}).sort({'timestamp': -1}).limit(1)[0]
            resp_content = item['data']['content']
            resp_title = item['data']['title']
            resp_type = 'article'
            self.in_coll.update({'_id': item['_id']}, {'response': True})
        elif content.find(u'美美哒') == 0:
            pass