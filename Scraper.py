import datetime
import json
import re
from datetime import datetime
from typing import TypedDict, List, Union

import requests as requests
from requests.cookies import RequestsCookieJar

RawDay = TypedDict('RawDay', {'id': str, 'descr': str, 'meta': TypedDict('MetaDict', {'start': str, 'end': str})})
ParsedItem = TypedDict('ParsedItem', {'type': str, 'name': str})
ParsedMenu = list[ParsedItem]
ParsedDay = TypedDict('ParsedDay', {'day': datetime, 'menu': ParsedMenu})
ParsedRestaurant = list[ParsedDay]


class Scraper:
    etterbeek_nl = 124364829
    etterbeek_en = 124364862
    jette_nl = 124364865
    jette_en = 124364868
    cookies: RequestsCookieJar = {}

    def get_cookie(self):
        r = requests.get("https://wearestudent.vub.be/idi/create")
        self.cookies = r.cookies

    @staticmethod
    def sanitize_str(to_sanitize: str) -> str:
        return to_sanitize.replace('\xa0', ' ').replace('\n\t', '\n')

    @staticmethod
    def item_type(item: str) -> str:
        if item.lower().startswith("soup:") or item.lower().startswith("soep:"):
            return "soup"
        elif item.lower().startswith("menu 1:"):
            return "menu 1"
        elif item.lower().startswith("menu 2:"):
            return "menu 2"
        elif item.lower().startswith("fish:"):
            return "fish"
        elif item.lower().startswith("vis:"):
            return "fish"
        elif item.lower().startswith("veggie:"):
            return "veggie"
        elif item.lower().startswith("pasta:"):
            return "pasta"
        elif item.lower().startswith("wok:"):
            return "wok"
        else:
            return "none"

    @staticmethod
    def item_name(item: str) -> str:
        [_, name] = item.split(':')
        name = name.strip()
        return name

    @staticmethod
    def menu_date(menu: RawDay) -> datetime:
        date_str = menu['meta']['start']

        if re.match("^\d\d\d\d-\d\d-\d\d$", date_str):
            date_str = date_str
        elif re.match("(\d\d\d\d-\d\d-\d\d) \d\d:\d\d:\d\d", date_str):
            date_str = re.match("(\d\d\d\d-\d\d-\d\d) \d\d:\d\d:\d\d", date_str).groups()[0]
        else:
            raise RuntimeError("They invented yet another format for their timestamps. This time it's {}".format(date_str))

        return datetime.strptime(date_str, "%Y-%m-%d")

    @staticmethod
    def possible_item(item: str) -> bool:
        item = item.lower()
        for prefix in ["soup", "soep", "wok", "fish", "vis", "veggie", "menu 1", "menu 2", "pasta", "wok"]:
            if item.startswith(prefix):
                return True
        return False

    @staticmethod
    def parse_item(item: str) -> Union[None, ParsedItem]:
        if re.match(".*restaurant.*gesloten.*", item, flags=re.IGNORECASE):
            return {'type': "closed", 'name': 'restaurant closed'}
        elif Scraper.possible_item(item):
            type = Scraper.item_type(item)
            name = Scraper.item_name(item)
            return {'type': type, 'name': name}
        else:
            # print("Invalid item: {}".format(item))
            return None

    @staticmethod
    def parse_menu(raw_day: RawDay) -> ParsedMenu:
        descr = Scraper.sanitize_str(raw_day['descr'])
        items = descr.split('\n')
        items = [Scraper.parse_item(item) for item in items]
        items = [item for item in items if item is not None]
        return items

    @staticmethod
    def parse_restaurant(menu: List[RawDay]) -> ParsedRestaurant:
        parsed = [{'day': Scraper.menu_date(day), 'menu': Scraper.parse_menu(day)} for day in menu]
        return parsed

    def get_menu_raw(self, sourceId):
        self.get_cookie()
        headers = {"Accept": "application/json", "Accept-Encoding": "gzip", "content-type": "application/json"}
        data = {'channelId': 8476, 'sourceIds': [sourceId], 'size': 9999, 'offset': 0}
        r = requests.post("https://wearestudent.vub.be/api/timeline", cookies=self.cookies, headers=headers, data=json.dumps(data))
        if 200 <= r.status_code < 300:
            result = r.json()
            items = result['data']['articles']
            return items
        else:
            raise RuntimeError("Failed to get the data from the endpoint.")

    def get_restaurant(self, sourceId):
        raw = self.get_menu_raw(sourceId)
        parsed = self.parse_restaurant(raw)
        return parsed
