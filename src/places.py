import math
import os
import sys

from dotenv import load_dotenv
from haversine import haversine
import googlemaps

load_dotenv()


def make_grid(gmaps_client, grid_element_side, location):
    # Search for location and get bounding box.
    # https://developers.google.com/maps/documentation/places/web-service/search-find-place

    resp = gmaps_client.find_place(location, "textquery", language="en")
    if resp.get("candidates") is None or len(resp.get("candidates")) == 0:
        print("Error: Location not found!")
        sys.exit(1)
    place_id = resp["candidates"][0]["place_id"]

    resp = gmaps_client.place(place_id, language="en")
    viewport = resp.get("result", dict()).get("geometry", dict()).get("viewport")
    if viewport is None:
        print("Error: viewport not found!")
        sys.exit(2)

    from_longitude = viewport.get("southwest").get("lng")
    from_latitude = viewport.get("southwest").get("lat")
    to_longitude = viewport.get("northeast").get("lng")
    to_latitude = viewport.get("northeast").get("lat")

    horiz_len_km = haversine(
        (from_latitude, from_longitude), (from_latitude, to_longitude)
    )
    vert_len_km = haversine(
        (from_latitude, from_longitude), (to_latitude, to_longitude)
    )

    n_horiz = math.ceil(horiz_len_km / grid_element_side)
    n_vert = math.ceil(vert_len_km / grid_element_side)

    grid_elements = []

    latitude_step = (to_latitude - from_latitude) / n_vert
    longitude_step = (to_longitude - from_longitude) / n_horiz

    for i in range(n_horiz):
        for j in range(n_vert):
            south_lat = from_latitude + j * latitude_step

            north_lat = south_lat + latitude_step
            north_lat = min(north_lat, to_latitude)

            west_lng = from_longitude + i * longitude_step
            east_lng = west_lng + longitude_step
            east_lng = min(east_lng, to_longitude)

            grid_elements.append(
                "rectangle:{},{}|{},{}".format(south_lat, west_lng, north_lat, east_lng)
            )

    return grid_elements, from_latitude, to_latitude, from_longitude, to_longitude


def get_places():
    results = []
    google_api_key = os.environ["GOOGLE_API_KEY"]
    gmaps_client = googlemaps.Client(key=google_api_key)

    location = 11222
    query = "egg and cheese"

    grid_element_side = 1.0
    grid_elements, from_latitude, to_latitude, from_longitude, to_longitude = make_grid(
        gmaps_client, grid_element_side, location
    )

    seen_place_ids = set()

    # Iterate across each subregion and perform search with given query in that region
    for location_bias in grid_elements:
        response = gmaps_client.find_place(
            query,
            "textquery",
            fields=["place_id", "name", "geometry", "formatted_address"],
            location_bias=location_bias,
            language="en",
        )
        # Iterate across search results and get contact info for each of them.
        # https://developers.google.com/maps/documentation/places/web-service/details
        for result in response.get("candidates", []):
            place_id = result.get("place_id")
            if place_id in seen_place_ids:
                continue

            latitude = result.get("geometry").get("location").get("lat")
            longitude = result.get("geometry").get("location").get("lng")

            if latitude < from_latitude or latitude > to_latitude:
                continue
            if longitude < from_longitude or longitude > to_longitude:
                continue

            seen_place_ids.add(place_id)

            place = gmaps_client.place(
                place_id,
                fields=["website"],
                language="en",
            )
            website = place.get("result", dict()).get("website")
            if website:
                row = {
                    "name": result.get("name"),
                    "address": result.get("formatted_address"),
                    "website": website,
                }
                results.append(row)

    return results
