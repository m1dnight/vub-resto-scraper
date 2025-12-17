import datetime
from enum import Enum
import json
import re
from datetime import datetime, date
from typing import List, Union
from bs4 import BeautifulSoup

from openai import OpenAI
from decimal import Decimal

import requests as requests
from requests.cookies import RequestsCookieJar

from pydantic import BaseModel

class RawDayMeta(BaseModel):
    start: str
    end: str

class RawDay(BaseModel):
    id: str
    descr: str
    meta: RawDayMeta

class ParsedMenuName(str, Enum):
    closed = "closed"
    menu1 = "menu 1"
    menu2 = "menu 2"
    soup = "soup"
    fish = "fish"
    wok = "wok"
    pasta = "pasta"
    unknown = "unknown"

    @staticmethod
    def from_str(s: str):
        try:
            return ParsedMenuName(s)
        except:
            return ParsedMenuName.unknown

class ParsedMenu(BaseModel):
    type: ParsedMenuName
    name: str

class ParsedDay(BaseModel):
    day: date
    menu: list[ParsedMenu]

class ParsedRestaurant(BaseModel):
    days: list[ParsedDay]
    used_llm: bool

PRICES = {
    "gpt-3.5-turbo-1106": {
        "output": Decimal(2) / Decimal(1000) / Decimal(1000),
        "input": Decimal(1) / Decimal(1000) / Decimal(1000),
    },
    "gpt-4-1106-preview": {
        "output": Decimal(3) / Decimal(100) / Decimal(1000),
        "input": Decimal(1) / Decimal(100) / Decimal(1000),
    },
    "gpt-4-0125-preview": {
        "output": Decimal(3) / Decimal(100) / Decimal(1000),
        "input": Decimal(1) / Decimal(100) / Decimal(1000),
    },
    "gpt-4-turbo-2024-04-09": {
        "output": Decimal(3) / Decimal(100) / Decimal(1000),
        "input": Decimal(1) / Decimal(100) / Decimal(1000),
    },
    "gpt-4o": {
        "output": Decimal(15) / Decimal(1000) / Decimal(1000),
        "input": Decimal(5) / Decimal(1000) / Decimal(1000),
    },
    "gpt-4o-mini": {
        "output": Decimal(60) / Decimal(100) / Decimal(1000) / Decimal(1000),
        "input": Decimal(15) / Decimal(100) / Decimal(1000) / Decimal(1000),
    },
    "gpt-4-vision-preview": {
        "output": Decimal(3) / Decimal(100) / Decimal(1000),
        "input": Decimal(1) / Decimal(100) / Decimal(1000),
    },
    "gpt-5-mini": {
        "output": Decimal(200) / Decimal(100) / Decimal(1000) / Decimal(1000),
        "input": Decimal(25) / Decimal(100) / Decimal(1000) / Decimal(1000),
    },
    "gpt-5-nano": {
        "output": Decimal(40) / Decimal(100) / Decimal(1000) / Decimal(1000),
        "input": Decimal(5) / Decimal(100) / Decimal(1000) / Decimal(1000),
    },
    # Per second
    "whisper-1": Decimal(6) / Decimal(1000) / Decimal(60),
    # Per 1M chars
    "tts-1": Decimal(30),
}

MODEL = "gpt-4o-mini"

OUTPUT_PRICE = PRICES[MODEL]["output"]
INPUT_PRICE = PRICES[MODEL]["input"]

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
        return to_sanitize.replace('\xa0', ' ').replace('\n\t', '\n').replace('\u200b', '')

    @staticmethod
    def item_type(item: str) -> str:
        item = item.lower().strip("•").strip()
        if item.startswith("soup") or item.startswith("soep"):
            return "soup"
        elif item.startswith("menu 1"):
            return "menu 1"
        elif item.startswith("menu 2"):
            return "menu 2"
        elif item.startswith("fish"):
            return "fish"
        elif item.startswith("vis"):
            return "fish"
        elif item.startswith("veggie"):
            return "veggie"
        elif item.startswith("pasta"):
            return "pasta"
        elif item.startswith("wok"):
            return "wok"
        else:
            return "none"

    @staticmethod
    def item_name(item: str) -> str:
        ch = ':'
        if ':' not in item:
            ch = ' '
        [_, name] = item.split(ch, 1)
        name = name.strip()
        return name

    @staticmethod
    def menu_date(menu: RawDay) -> str:
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
        item = item.lower().strip("•").strip()
        for prefix in ["soup", "soep", "wok", "fish", "vis", "veggie", "menu 1", "menu 2", "pasta", "wok"]:
            if item.startswith(prefix):
                return True
        return False

    @staticmethod
    def parse_item(item: str) -> Union[None, ParsedMenu]:
        if item is None:
            return

        item = item.strip()
        if len(item) < 5:
            return None

        if re.match(".*restaurant.*gesloten.*", item, flags=re.IGNORECASE):
            return ParsedMenu(type= "closed", name = 'restaurant closed')
        elif Scraper.possible_item(item):
            type = Scraper.item_type(item)
            name = Scraper.item_name(item)
            return ParsedMenu(type = ParsedMenuName.from_str(type), name = name)
        elif item.strip() != None:
            return ParsedMenu(type= "unknown", name = item)
        else:
            # print("Invalid item: {}".format(item))
            return None

    @staticmethod
    def parse_menu(raw_day: RawDay) -> list[ParsedMenu]:
        descr = Scraper.sanitize_str(raw_day['descr'])
        items = descr.split('\n')
        items = [Scraper.parse_item(item) for item in items]

        # You can uncomment this exception to fall back onto the OpenAI-based parser
        #raise Exception("woopsie")

        # If they messed up their newline behaviour, let's try parsing the HTML instead
        if len(items) < 2:
            content = BeautifulSoup(raw_day['content'], features='html.parser')
            content = content.find_all("li")
            items = [Scraper.parse_item(str(item.string)) for item in content]
        items = [item for item in items if item is not None]

        return items

    @staticmethod
    def parse_restaurant_openai(menu: list[RawDay]) -> ParsedRestaurant:
        client = OpenAI()
        response = client.responses.parse(
            model=MODEL,
            # reasoning={'effort': 'low'},
            input=[
                {"role": "system", "content": "Extract the menu information as JSON.  Do not guess the menu type if unclear; use `unknown` if uncertain, but always include every menu. There can only be one of a menu type per day, except for pasta.  There will always be one soup."},
                {
                    "role": "user",
                    "content": str(menu),
                },
            ],
            text_format=ParsedRestaurant,
        )

        out_cost = OUTPUT_PRICE * response.usage.output_tokens
        reason_cost = OUTPUT_PRICE * response.usage.output_tokens_details.reasoning_tokens
        in_cost = INPUT_PRICE * response.usage.input_tokens
        cost = out_cost + in_cost

        print(f"Cost: €{cost} (€{reason_cost} for reasoning)")

        output = response.output_parsed
        if not output.used_llm:
            print("Strange, the LLM thought it's not an LLM")
        output.used_llm = True

        return response.output_parsed

    @staticmethod
    def parse_restaurant(menu: List[RawDay]) -> ParsedRestaurant:
        try:
            parsed = [ParsedDay(day= Scraper.menu_date(day), menu = Scraper.parse_menu(day)) for day in menu]
            return ParsedRestaurant(days=parsed, used_llm=False)
        except Exception as e:
            # Fallback to LLM
            print(f"Falling back to LLM because {e}")
            return Scraper.parse_restaurant_openai(menu)

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
