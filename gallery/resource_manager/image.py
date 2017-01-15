# -*- coding: utf-8 -*-
import os
from PIL import Image
from datetime import datetime

from gallery.resource_manager.base import BaseResource


class ImageResource(BaseResource):

    def __init__(self, file_path, owner, create_time, upload_time, tags=None, visit_log=None):
        super(ImageResource, self).__init__(type='image')
        self.date = create_time
        self.upload_time = upload_time
        self.path = file_path
        self.owner = owner
        if tags:
            self.tags = tags
        if visit_log:
            self.visit_log = visit_log

    def _to_document(self):
        return {
            'path': self.path,
            'owner': self.owner,
            'date': self.date,
            'upload_time': self.upload_time,
            'type': self.type,
            'visit_log': self.visit_log,
            'tags': self.tags
        }

    def _save_disk(self):
        pass

    @classmethod
    def load_from_path(cls, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                if os.path.splitext(f)[-1].lower() not in {'.jpg', '.jpeg'}:
                    continue
                file_path = os.path.join(root, f)
                cls.load_image(file_path).save()

    @classmethod
    def load_image(cls, file_path):
        image = Image.open(file_path)
        date = datetime.strptime(image._getexif()[36867], '%Y:%m:%d %H:%M:%S')
        return cls(file_path, 'auto', date, datetime.now())

    @classmethod
    def load_from_database(cls, document):
        if document['type'] == 'image':
            return cls(document['path'], document['owner'], document['date'], document['upload_time'],
                       document['tags'], document['visit_log'])
        else:
            raise TypeError
