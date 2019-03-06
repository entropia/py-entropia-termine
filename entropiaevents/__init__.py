import json
import re
import locale
from datetime import datetime, timedelta
from obelixtools import API

class Event:
    def __init__(self, date_str, time_str, location, description):
        self._defaults = dict(
            locale='de_DE',
            duration=timedelta(hours=2)
        )
        self._parse_date(date_str, time_str)
        self.location = location
        self.description = description

    @property
    def start_date(self):
        if not self._dates:
            return 'Date parsing error!'
        return self._dates[0].strftime('%x %X')

    @property
    def end_date(self):
        if not self._dates[1]:
            return (self._dates[0] + self.default_event_duration).strftime('%x %X')
        return self._dates[1].strftime('%x %X')

    def set_locale(self, value='de_DE'):
        self._defaults['locale'] = value;

    @property
    def locale(self):
        return self._defaults['locale']

    def set_default_event_duration(self, hours=2):
        self._defaults['duration'] = timedelta(hours=hours)

    @property
    def default_event_duration(self):
        return self._defaults['duration']

    def _parse_date(self, date_str, time_str):
        locale.setlocale(locale.LC_TIME, self.locale)
        date_str = date_str.split('-')
        if len(date_str) == 2:
            fmt = '%a, %d.%m.%Y'
            try:
                self._dates = [datetime.strptime(el.strip(), fmt) for el in date_str]
            except:
                self._dates = False
        else:
            full_date = date_str[0].strip() + ' ' + time_str.strip()
            self._dates = [datetime.strptime(full_date, '%a, %d.%m.%Y ab %H:%M'), False]

    def __str__(self):
        return u'{} : {} - {location} - {description}'.format(self.start_date, self.end_date, **self.__dict__)

class WikiEvents:
    API_URL = 'https://entropia.de/api.php?format=json&action=parse&page=Vorlage:Termine'

    def __init__(self):
        self._api = API(WikiEvents.API_URL, 'json')
        self._api.query()
        self._html = self._api.content['parse']['text']['*'].replace("\n", "")
        self._parse_rows()
        self._parse_events()

    def _parse_rows(self):
        row_re = re.compile("<tr>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>")
        self._rows = row_re.finditer(self._html, re.I)

    def _strip_html(self, data):
        return re.sub('<[^<]+?>', '', data)

    def _parse_events(self):
        self._events = []
        for row in self._rows:
            date, time, place, desc = [self._strip_html(col).strip() for col in row.groups()]
            self._events.append(Event(date, time, place, desc))

    def to_json_file(self, filename):
        with file(filename, 'wb') as f:
            f.write(json.dumps(self.events, ensure_ascii=False).encode('utf8'))

    @property
    def events(self):
        return self._events
