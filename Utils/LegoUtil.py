import rebrick
import json
import pickle


def valid_key(key):
    try:
        rebrick.init(key)
        rebrick.lego.get_categories()
    except:
        return False
    return True


def save_key(key):
    with open('././settings.cfg', 'rb') as f:
        data = pickle.load(f)
        with open('././settings.cfg', 'wb') as f:
            data['API_KEY'] = key
            pickle.dump(data, f)


def get_key():
    with open('././settings.cfg', 'rb') as f:
        data = pickle.load(f)
        return data['API_KEY']


def get_part_categories():
    rebrick.init(get_key())
    return json.loads(rebrick.lego.get_categories().read())["results"]


def get_parts(category_id):
    page_id = 1
    next_page = True
    filtered = []
    rebrick.init(get_key())
    while next_page:
        response = rebrick.lego.get_parts(page=str(page_id), page_size=1000, part_cat_id=category_id)
        data = json.loads(response.read())
        parts = data["results"]
        for part in parts:
            if part['print_of'] is None:
                filtered.append(part)
        if data["next"] is None:
            next_page = False
        page_id += 1
    return filtered
