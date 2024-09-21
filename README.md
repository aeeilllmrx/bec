Attempt at an agent-like workflow. The overall goal is to gather a bunch of
prices for bacon egg + cheese near me and display them on a map.

The overall flow is as follows:

1. look up place websites using Google Places API
2. download menu from website as a png
3. ask claude to find and extract bec prices
4. populate a database/sheet of bec prices
5. update map results
