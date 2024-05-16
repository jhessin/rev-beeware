"""
This will handle everything about downloading the REV and storing it to the
local hard drive.

I will try to use TinyDB and toga.paths.Paths.data for a location.
"""
from datetime import datetime
import os

from tinydb import TinyDB
from os import path
from toga import App
from rev_beeware.constants import *
import requests
import json


class Storage:
    db: TinyDB

    def __init__(self, app: App):
        db_path = path.join(app.paths.data, 'db.json')
        if not os.path.exists(db_path):
            os.mkdir(app.paths.data)
            open(db_path, 'a').close()
        self.db = TinyDB(path.join(app.paths.data, 'db.json'))
        self.db.insert({'null': 'null'})
        date_res = requests.get(DATE_URL)
        response = json.loads(date_res.text)['REV_Timestamp'][0]['timestamp']
        self.remote_date = datetime.fromisoformat(response)

    @property
    def local_date(self) -> datetime | None:
        try:
            return datetime.fromisoformat(self.db.table('date').all()[0]['date'])
        except IndexError:
            return None


if __name__ == '__main__':
    storage = Storage(App('REV'))
