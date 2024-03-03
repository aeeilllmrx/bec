import csv
import os
import requests

google_api_key = os.environ["GOOGLE_API_KEY"]

places = [
    "Five Leaves",
    "Baker's Dozen",
    "Bagel Point",
    "Frankel's Delicatessen",
    "Brooklyn Standard Deli",
    "Moe's Doughs",
    "Three Decker Diner",
    "Lite Bites Cafe",
]

locations = []

for place in places:
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={place}&key={google_api_key}"
    response = requests.get(url)
    data = response.json()
    try:
        lat, lon = data["results"][0]["geometry"]["location"].values()
        locations.append((place, lat, lon))
    except:
        pass

with open("locations.csv", "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(locations)
