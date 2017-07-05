#!/usr/bin/env python3

import contextlib
import os
import pickle


class ModDB(contextlib.ContextDecorator):
    def __init__(self, path):
        self.db_path = path

    def __enter__(self):
        if os.path.exists(self.db_path):
            fo = open(self.db_path, 'rb')
            self.db = pickle.load(fo)
            fo.close()
        else:
            self.db = {}

        return self

    def __exit__(self, exc_type, exc, exc_tb):
        fo = open(self.db_path, 'wb')
        pickle.dump(self.db, fo)
        fo.close()

    def has_changed(self, path: str):
        path = os.path.abspath(path)

        if not os.path.exists(path):
            return True

        last_mod = self.db.get(path, 0)
        self.db[path] = os.stat(path).st_mtime

        return self.db[path] > last_mod
