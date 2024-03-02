import csv
import folium

from flask import Flask
from folium.plugins import HeatMap

app = Flask(__name__)

@app.route('/')
def index():
    start_coords = (40.6782, -73.9442)
    map = folium.Map(location=start_coords, zoom_start=13)

    # TODO allow adding locations with google forms
    # TODO cache the map so it is not being recomputed each time?

    prices = []

    with open('locations.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for name, lat, lon, price in csv_reader:
            prices.append([float(lat), float(lon), float(price)])

            folium.Marker(
                [lon, lat], 
                popup=folium.Popup(name, parse_html=True)
            ).add_to(map)

    HeatMap(prices).add_to(map)

    return map._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)