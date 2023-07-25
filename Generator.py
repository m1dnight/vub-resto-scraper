from Scraper import ParsedRestaurant, ParsedDay, ParsedItem


class Generator:
    default_color = '#f0eb93'  # very light yellow
    color_mapping = {'soep': '#fdb85b',  # yellow
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

    @staticmethod
    def generate(restaurant: ParsedRestaurant):
        generated_restaurant = []
        for day in restaurant:
            generated_day = Generator.generate_day(day)
            generated_restaurant.append(generated_day)
        return generated_restaurant

    @staticmethod
    def generate_day(day: ParsedDay):
        date_key = day['day'].strftime("%Y-%m-%d")
        dishes = [Generator.generate_dish(dish) for dish in day['menu']]
        return {"date": date_key, "menus": dishes}

    @staticmethod
    def generate_dish(dish: ParsedItem):
        dict = {'dish': dish['name'], 'color': Generator.generate_color(dish['type']), 'name': dish['type'].capitalize()}
        return dict

    @staticmethod
    def generate_color(type: str):
        if type in Generator.color_mapping:
            return Generator.color_mapping[type]
        else:
            return Generator.default_color
