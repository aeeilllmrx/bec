from flask import Flask

import folium

app = Flask(__name__)

@app.route('/')
def index():
    start_coords = (40.6782, -73.9442)
    map = folium.Map(location=start_coords, zoom_start=13)

    # TODO abstract this out into a text file
    # TODO allow appends to this file using google forms
    # TODO cache the map so it is not being recomputed each time?
    locations = [
        {'lat': -73.96307, 'lon': 40.67626, 'name': 'Bar Meridian', 'heat_type': 'leg lamp'},
        {'lat': -73.9628, 'lon': 40.68683, 'name': 'Izzy Rose', 'heat_type': 'fire pit'}
    ]

    for loc in locations:
        html = '{}<br>{}'.format(loc['name'], loc['heat_type'])
        iframe = folium.IFrame(html, width=100, height=100)
        folium.Marker(
            [loc['lon'], loc['lat']], 
            popup=folium.Popup(iframe)
        ).add_to(map)

    return map._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)
