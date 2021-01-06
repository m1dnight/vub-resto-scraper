import re, datetime
from lxml import html
from domain.day import Day
from domain.dish import Dish
from domain.menu import Menu


###########
# Helpers #
###########


def parse_html(html_src):
    return html.fromstring(html_src)


#############
# Tokenizer #
#############


def get_menus(src):
    """
    Given the parsed HTML source, parses the blocks that represent a menu.
    *There are four of them*: English/Dutch variants of both Jette and Etterbeek.
    :param html:
    :return: Returns a list of html tree items.
    """
    # / html / body / div[4] / div / div / div[1] / section[2] / div / div
    # / html / body / div[4] / div / div / div[1] / section[3] / div / div
    menus = src.xpath('/html/body/div[3]/div/div/div')
    return menus


def menu_days(src):
    """
    Returns each day for the given menu. Typically there are 5 days.
    :param src:
    :return:
    """
    days = src.xpath('./section[position() > 1 and position() < 9]/div/div')
    days_str = list(map(lambda d: html.tostring(d), days))
    return days


def day_date(src):
    """
    Returns the date string for the given day.
    :param src:
    :return:
    """
    return src.xpath('./h4[1]')[0]


def day_date_heading_switch(src):
    """
    Returns the date string for the given day.
    But sometimes the VUB people switch around headings. For example:

    Expected

    13.01.2020
    LUNCH

    But then for some reason they type:

    LUNCH
    13.01.2020

    So we have to change the div's xpath.

    :param src:
    :return:
    """
    return src.xpath('./p[2]')[0]


def day_dishes_noon(src):
    """
    Returns the dishes served at noon for this given day.
    :param src:
    :return:
    """
    noon = src.xpath('./ul[1]/li')
    if not noon:
        return []
    else:
        return noon


def day_dishes_evening(src):
    """
    Returns the dishes served in the evening for this day.
    :param src:
    :return:
    """
    evening = src.xpath('./ul[2]/li')
    if not evening:
        return []
    else:
        return evening


##########
# Parser #
##########

def menu_title(menu_src):
    """
    Given the parsed HTML source for a menu, this function returns the title of the menu.
    This is at the time of writing "(Weekmenu | Week Menu) (Etterbeek | Jette)"
    :param menu_src: Parsed HTML tree.
    :return: Returns a string containing the title of the menu.
    """
    headers = menu_src.xpath('./section[1]/div[1]/div[2]/h2')

    # Try second xpath for deviating page.
    if len(headers) < 1:
        headers = menu_src.xpath('./section[1]/div[1]/div/h2')

    title = headers[0]
    return title.text


# 6/7/2020
def is_valid_date(date_str):
    regex = "\d+\.\d+.\d{4}"
    return re.match(regex, date_str)


# Woensdag 7 September
def is_valid_date_2(date_str):
    regex = "(maandag|dinsdag|woensdag|donderdag|vrijdag|zaterdag|zondag)\s(\d+)\s(januari|februari|maart|april|mei|juni|juli|augustus|september|oktober|november|december)"
    return re.match(regex, date_str.lower())


# Wednesday September 7
def is_valid_date_3(date_str):
    regex = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s(january|february|march|april|may|june|july|august|september|october|november|december)\s(\d+)"
    result = re.match(regex, date_str.lower())
    return result

# Wednesday 7 September
def is_valid_date_4(date_str):
    regex = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s(\d+)\s(january|february|march|april|may|june|july|august|september|october|november|december)"
    result = re.match(regex, date_str.lower())
    return result


def parse_date_str(date_str):
    # Strip the date string from the intput string.
    date_str_clean = re.match("\d+\.\d+.\d{4}", date_str).group(0)
    return datetime.datetime.strptime(date_str_clean, "%d.%m.%Y")


def parse_date_str_2(date_str):
    # Strip the date string from the intput string.
    date_str_clean = re.match(
        "(maandag|dinsdag|woensdag|donderdag|vrijdag|zaterdag|zondag)\s(\d+)\s(januari|februari|maart|april|mei|juni|juli|augustus|september|oktober|november|december)",
        date_str.lower())

    months = {
        "januari": 1,
        "februari": 2,
        "maart": 3,
        "april": 4,
        "mei": 5,
        "juni": 6,
        "juli": 7,
        "augustus": 8,
        "september": 9,
        "oktober": 10,
        "november": 11,
        "december": 12,
    }
    day = date_str_clean.group(2)
    monthname = date_str_clean.group(3)
    year = datetime.datetime.now().year

    result = datetime.datetime.strptime("{}.{}.{}".format(day, months[monthname], year), "%d.%m.%Y")
    return result


def parse_date_str_3(date_str):
    # Strip the date string from the intput string.
    date_str_clean = re.match(
        "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s(january|february|march|april|may|june|july|august|september|october|november|december)\s(\d+)",
        date_str.lower())

    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12,
    }
    day = date_str_clean.group(3)
    monthname = date_str_clean.group(2)
    year = datetime.datetime.now().year

    result = datetime.datetime.strptime("{}.{}.{}".format(day, months[monthname], year), "%d.%m.%Y")
    return result


def parse_date_str_4(date_str):
    # Strip the date string from the intput string.
    date_str_clean = re.match(
        "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s(\d+)\s(january|february|march|april|may|june|july|august|september|october|november|december)",
        date_str.lower())

    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12,
    }
    day = date_str_clean.group(2)
    monthname = date_str_clean.group(3)
    year = datetime.datetime.now().year

    result = datetime.datetime.strptime("{}.{}.{}".format(day, months[monthname], year), "%d.%m.%Y")
    return result


def parse_date(day_src):
    try:
        date_str = day_date(day_src).text.strip()
        if is_valid_date(date_str):
            return parse_date_str(date_str)

        if is_valid_date_2(date_str):
            return parse_date_str_2(date_str)

        if is_valid_date_3(date_str):
            return parse_date_str_3(date_str)

        if is_valid_date_4(date_str):
            return parse_date_str_4(date_str)

        date_str = day_date_heading_switch(day_src).text.strip()
        if is_valid_date(date_str):
            return parse_date_str(date_str)
        return None
    except:
        return None


def parse_date_2(day_src):
    date_str = day_date(day_src).text.strip()
    if is_valid_date_2(date_str):
        return parse_date_str_2(date_str)


def parse_language(menu_src):
    """
    Returns whether this menu is in English or dutch.
    :param menu_src: The html representation of the menu.
    :return: Returns the string "nl" or "en"
    """
    title = menu_title(menu_src).strip().lower()
    if title.startswith('weekmenu'):
        return "nl"
    else:
        return "en"


def parse_location(menu_src):
    """
    Returns whether this menu is for Jette or Etterbeek.
    :param menu_src: The html representation of the menu.
    :return: Returns the string "etterbeek" or "jette"
    """
    title = menu_title(menu_src).strip().lower()
    if "etterbeek" in title:
        return "etterbeek"
    else:
        return "jette"


def parse_dish(dish_str):
    try:
        [type, name] = dish_str.lower().split(':')
        return Dish(name.strip().title(), type.strip().title())
    except ValueError: # In case the format is not "Dish Type : Name"
        return None


def parse_dishes_noon(day_src):
    dishes_noon_src = day_dishes_noon(day_src)

    dishes_noon = []
    for dish_noon_src in dishes_noon_src:
        dish_str = dish_noon_src.text_content()
        dish = parse_dish(dish_str)
        if dish is not None:
            dishes_noon.append(dish)

    return dishes_noon


def parse_dishes_evening(day_src):
    dishes_evening_src = day_dishes_evening(day_src)

    dishes_evening = []
    for dish_evening_src in dishes_evening_src:
        dish_str = dish_evening_src.text_content()
        dish = parse_dish(dish_str)
        if dish is not None:
            dishes_evening.append(dish)

    return dishes_evening


def parse_day(day_src):
    date = parse_date(day_src)
    if date is None:
        return None
    else:
        dishes_noon = parse_dishes_noon(day_src)
        dishes_evening = parse_dishes_evening(day_src)

        return Day(dishes_noon, dishes_evening, date)


def parse_menu(menu_src):
    lang = parse_language(menu_src)
    location = parse_location(menu_src)

    days = []
    for day_src in menu_days(menu_src):
        str = html.tostring(day_src)
        day = parse_day(day_src)
        if day is not None:
            days.append(day)

    return Menu(days, lang, location)


def parse_menus(src):
    # A menu is a menu for a location + a language.
    # I.e., etterbeek english, etterbeek dutch, jette dutch, and jette english.
    menus = get_menus(src)
    result = []

    for menu in menus:
        result.append(parse_menu(menu))

    return result
