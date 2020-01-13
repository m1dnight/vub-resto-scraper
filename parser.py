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
    menus = src.xpath('/html/body/div[3]/div/div/div')
    return menus


def menu_days(src):
    """
    Returns each day for the given menu. Typically there are 5 days.
    :param src:
    :return:
    """
    days = src.xpath('./section[position() > 1 and position() < 7]/div/div')
    return days


def day_date(src):
    """
    Returns the date string for the given day.
    :param src:
    :return:
    """
    return src.xpath('./p[1]')[0]


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
    title = menu_src.xpath('./section[1]/div[1]/div[1]/h2')[0]
    return title.text


def is_valid_date(date_str):
    regex = "\d+\.\d+.\d{4}"
    return re.match(regex, date_str)


def parse_date_str(date_str):
    return datetime.datetime.strptime(date_str, "%d.%m.%Y")


def parse_date(day_src):
    date_str = day_date(day_src).text.strip()
    if is_valid_date(date_str):
        return parse_date_str(date_str)

    date_str = day_date_heading_switch(day_src).text.strip()
    if is_valid_date(date_str):
        return parse_date_str(date_str)
    else:
        return None


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
    [type, name] = dish_str.lower().split(':')
    return Dish(name.strip().title(), type.strip().title())


def parse_dishes_noon(day_src):
    dishes_noon_src = day_dishes_noon(day_src)

    dishes_noon = []
    for dish_noon_src in dishes_noon_src:
        dish_str = dish_noon_src.text_content()
        dish = parse_dish(dish_str)
        dishes_noon.append(dish)

    return dishes_noon


def parse_dishes_evening(day_src):
    dishes_evening_src = day_dishes_evening(day_src)

    dishes_evening = []
    for dish_evening_src in dishes_evening_src:
        dish_str = dish_evening_src.text_content()
        dish = parse_dish(dish_str)
        dishes_evening.append(dish)

    return dishes_evening


def parse_day(day_src):
    date = parse_date(day_src)
    dishes_noon = parse_dishes_noon(day_src)
    dishes_evening = parse_dishes_evening(day_src)

    return Day(dishes_noon, dishes_evening, date)


def parse_menu(menu_src):
    lang = parse_language(menu_src)
    location = parse_location(menu_src)

    days = []
    for day_src in menu_days(menu_src):
        day = parse_day(day_src)
        days.append(day)

    return Menu(days, lang, location)


def parse_menus(src):
    menus = get_menus(src)
    result = []

    for menu in menus:
        result.append(parse_menu(menu))

    return result
