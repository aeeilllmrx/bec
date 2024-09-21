#!/usr/bin/env python
import csv

from menus import download_menu
from places import get_places
from prices import get_item_and_price


def main():
    writer = csv.writer(open("data.csv", "w"))
    writer.writerow(["name", "address", "website", "item", "price"])

    places = get_places()
    for place in places:
        success = download_menu(
            place["name"],
            place["website"],
        )
        if not success:
            continue
        item, price = get_item_and_price(place["name"])
        if item and price:
            writer.writerow(
                [place["name"], place["address"], place["website"], item, price]
            )


if __name__ == "__main__":
    main()
