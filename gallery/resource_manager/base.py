# -*- coding: utf-8 -*-
from gallery.utils import db_cli


class BaseResource(object):
    def __init__(self, type):
        self._db = db_cli.resource
        self.type = type
        self.tags = []
        self.visit_log = []

    def save(self):
        self._save_disk()
        data = self._to_document()
        self._db.insert_one(data)

    def _save_disk(self):
        raise NotImplementedError

    def _to_document(self):
        raise NotImplementedError

