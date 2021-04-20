from threading import Lock
from copy import deepcopy


class Repo(object):

    def __init__(self, url, commit_hash):
        self.url = url
        self.commit_hash = commit_hash

    def format_key(self):
        return f"{self.url}:{self.commit_hash}"

class Store(object):

    def __init__(self):
        self._lock = Lock()
        self._store = {}

    def add(self, key, value):
        with self._lock:
            self._store[key] = value

    @property
    def json(self):
        with self._lock:
            return deepcopy(self._store)

class Counter(object):

    def __init__(self):
        self._lock = Lock()
        self._count = 0

    @property
    def value(self):
        with self._lock:
            return self._count

    def add(self, value):
        with self._lock:
            self._count += value
