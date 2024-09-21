import folium
import pandas as pd

from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)

load_dotenv()


@app.route("/")
def index():
    start_coords = (40.635, -73.95)
    map = folium.Map(location=start_coords, zoom_start=12, tiles="cartodbpositron")

    brooklyn_nabes_url = "https://raw.githubusercontent.com/blackmad/neighborhoods/master/brooklyn.geojson"
    folium.GeoJson(brooklyn_nabes_url).add_to(map)

    prices_df = pd.read_csv("src/data.csv")
    for name, lat, lon, item, price in prices_df.itertuples(index=False):
        popup_text = f"{name}: {item}, ${price}"
        folium.Marker([float(lat), float(lon)], popup=popup_text).add_to(map)

    # TODO get neighborhood from lat/long
    prices_df["neighborhood"] = None

    folium.Choropleth(
        geo_data=brooklyn_nabes_url,
        data=prices_df,
        columns=["neighborhood", "price"],
        key_on="feature.properties.name",
        fill_color="RdYlGn_r",
        fill_opacity=0.8,
        line_opacity=0.3,
        nan_fill_color="white",
        legend_name="Average price for a BEC",
    ).add_to(map)

    return map._repr_html_()


if __name__ == "__main__":
    app.run(debug=True)
