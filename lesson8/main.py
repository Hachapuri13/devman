import json
import requests
from geopy import distance
import folium
from dotenv import load_dotenv
import os


def declension(number, word):
    forms = {
        "метр": ["метр", "метра", "метров"],
        "километр": ["километр", "километра", "километров"],
    }

    word_forms = forms[word]

    if not number.is_integer():
        return word_forms[2]  # Для дробей — всегда "метров" или "километров"

    num = int(number)
    last_two = num % 100
    last_digit = num % 10

    if 11 <= last_two <= 14:
        return word_forms[2]
    elif last_digit == 1:
        return word_forms[0]
    elif 2 <= last_digit <= 4:
        return word_forms[1]
    else:
        return word_forms[2]


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()["response"]["GeoObjectCollection"]["featureMember"]

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant["GeoObject"]["Point"]["pos"].split(" ")
    return lon, lat


def get_distance(shop):
    return shop["distance"]


def main():
    load_dotenv()
    apikey = os.environ["apikey"]

    with open("coffee.json", "r", encoding="CP1251") as coffeeshops_file:
        file_contents = coffeeshops_file.read()
    coffeeshops = json.loads(file_contents)

    location = input("Где вы находитесь? ")
    location_coords = fetch_coordinates(apikey, location)
    location_coords_back = (location_coords[1], location_coords[0])
    structured_coffeeshops = []

    for coffeeshop in coffeeshops:
        shop_coords = coffeeshop["geoData"]["coordinates"]
        shop_coords_back = (shop_coords[1], shop_coords[0])
        distance_between = distance.distance(location_coords_back,
                                             shop_coords_back).km
        coffee_shop = {
            "title": coffeeshop["Name"],
            "distance": distance_between,
            "latitude": shop_coords[1],
            "longtitude": shop_coords[0],
        }
        structured_coffeeshops.append(coffee_shop)

    sorted_shops = sorted(structured_coffeeshops, key=get_distance)
    nearest_shops = sorted_shops[:5]

    m = folium.Map(location_coords_back, zoom_start=18)

    for shop in nearest_shops:
        shop["distance"] = round(shop["distance"], 3)
        if shop["distance"] < 1:
            shop["distance"] = shop["distance"] * 1000
            measurement = declension(shop["distance"], "метр")
        else:
            measurement = declension(shop["distance"], "километр")

        if shop["distance"].is_integer():
            shop["distance"] = int(shop["distance"])

        folium.Marker(
            location=[shop["latitude"], shop["longtitude"]],
            tooltip="{} {}".format(shop["distance"], measurement),
            popup=shop["title"],
            icon=folium.Icon(icon="cloud"),
        ).add_to(m)

    m.save("index.html")


if __name__ == "__main__":
    main()
