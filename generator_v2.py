# Version 2 JSON:
#
# [
#   {
#     "date": "2019-09-23",
#     "noon": [
#       {
#         "dish": "Tomato soup",
#         "color": "#fdb85b",
#         "name": "Soup"
#       }
#     ]
#     "evening": [
#       {
#         "dish": "Tomato soup",
#         "color": "#fdb85b",
#         "name": "Soup"
#       }
#     ]
#   }
# ]
import json
from fuzzywuzzy import fuzz

# Mapping of colors for the menus.
DEFAULT_COLOR = '#f0eb93'  # very light yellow
COLOR_MAPPING = {
    'soep': '#fdb85b',  # yellow
    'soup': '#fdb85b',  # yellow
    'menu 1': '#68b6f3',  # blue
    'dag menu': '#68b6f3',  # blue
    'dagmenu': '#68b6f3',  # blue
    'health': '#ff9861',  # orange
    'vis': '#ff9861',  # orange
    'fish': '#ff9861',  # orange
    'menu 2': '#cc93d5',  # purple
    'meals of the world': '#cc93d5',  # purple
    'fairtrade': '#cc93d5',  # purple
    'fairtrade menu': '#cc93d5',  # purple
    'veggie': '#87b164',  # green
    'veggiedag': '#87b164',  # green
    'pasta': '#de694a',  # red
    'pasta bar': '#de694a',  # red
    'wok': '#6c4c42',  # brown
}


def color_for_dish(input_type):
    max_type = None
    max_dist = -1
    for type, color in COLOR_MAPPING.items():
        r = fuzz.ratio(type.lower(), input_type.lower())
        if r > max_dist:
            max_color = color
            max_dist = r
    return color


def generate_json_dish(dish):
    dish_dict = {'dish': dish.name, 'name': dish.type, 'color': color_for_dish(dish.type)}
    return dish_dict


def generate_json_day(day):
    try:
        menu = {'date': day.date.strftime("%Y-%m-%d")}

        noon = []
        for dish in day.dishes_noon:
            json_dish = generate_json_dish(dish)
            noon.append(json_dish)
        menu['noon'] = noon

        evening = []
        for dish in day.dishes_evening:
            json_dish = generate_json_dish(dish)
            evening.append(json_dish)

        menu['evening'] = evening

        return menu
    except AttributeError:
        return None


def generate_json_menu(menu):
    day_dicts = []
    for day in menu.days:
        day_dicts.append(generate_json_day(day))

    return day_dicts


def write_json_to_file(json_dict):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=2)
