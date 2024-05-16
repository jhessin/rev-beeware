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

    @property
    def remote_date(self) -> datetime:
        date_res = requests.get(DATE_URL)
        response = json.loads(date_res.text)['REV_Timestamp'][0]['timestamp']
        return datetime.fromisoformat(response)

    @property
    def local_date(self) -> datetime | None:
        try:
            return datetime.fromisoformat(self.db.table('date').all()[0]['date'])
        except IndexError:
            return None

    @property
    def needs_update(self) -> bool:
        return not self.local_date or self.local_date < self.remote_date

    @property
    def bible(self):
        return self.db.table('REV_Bible').all()[0]

    def update(self):
        # Download Bible
        result = requests.get(BIBLE_URL)
        bible = json.loads(result.text)['REV_Bible'][0]
        self.db.table('REV_Bible').insert(bible)

        # Download Commentary
        result = requests.get(COMMENTARY_URL)
        commentary = json.loads(result.text)['REV_Commentary'][0]
        self.db.table('REV_Commentary').insert(commentary)

        # Download Appendix
        result = requests.get(APPENDICES_URL)
        appendix = json.loads(result.text)['REV_Appendices'][0]
        self.db.table('REV_Appendices').insert(appendix)

        # Update Date
        self.db.table('date').insert({'date': self.remote_date.isoformat()})
        pass
