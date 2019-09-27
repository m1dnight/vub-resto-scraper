# Version 1 JSON:
#
# [
#   {
#     "date": "2019-09-23",
#     "menus": [
#       {
#         "dish": "Tomato soup",
#         "color": "#fdb85b",
#         "name": "Soup"
#       }
#     ]
#   }
# ]
import json
import parser
from main import get_html, URL


def generate_json_dish(dish):
    dish_dict = {'dish': dish.name, 'name': dish.type, 'color': "#fdb85b"}
    return dish_dict


def generate_json_day(day):
    menu = {'date': day.date.strftime("%Y-%m-%d")}

    dishes = []
    for dish in day.dishes_noon:
        json_dish = generate_json_dish(dish)
        dishes.append(json_dish)

    menu['menus'] = dishes

    return menu


def generate_json_menu(menu):
    day_dicts = []
    for day in menu.days:
        day_dicts.append(generate_json_day(day))

    return day_dicts

def write_json_to_file(json_dict):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=2)


def generate_files(menus):
    for menu in menus:
        menus_dict = list(map(generate_json_menu(menu)))



        write_json_to_file(menus_dict, destination)

