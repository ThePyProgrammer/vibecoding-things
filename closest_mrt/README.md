# closest_mrt

`closest_mrt` suggests Singapore MRT stations that are central to a list of input MRT stations.

It models the MRT network as a graph and ranks every station by lowest total weighted distance from the input stations.

Each station-to-station ride costs 1. Changing MRT lines adds a configurable transfer penalty, which defaults to 2.

## Usage

```bash
python -m closest_mrt "Jurong East" Punggol Tampines
```

You can use station names or MRT codes:

```bash
python -m closest_mrt NS1 NE17 EW2 --limit 5
```

Set the line-change penalty to `0` for pure hop counts:

```bash
python -m closest_mrt NS1 NE17 EW2 --transfer-penalty 0
```

Example output columns:

```text
rank station total-cost max-cost Jurong East Punggol Tampines
   1 Serangoon                    29       13 13 5 11
```

## Web UI

Open `index.html` in a browser to use the static web interface. It runs the same weighted optimizer in browser-side JavaScript and does not need a server. Add one row per person, fill their incoming and outgoing MRT stations, and use the transfer penalty field to decide how much a line change should count.

Hover or focus an origin cost in the results table to see the route as a timeline. The segment colors show which MRT line is used between stops.

If you change the Python MRT line data, regenerate the HTML file:

```bash
python -m closest_mrt.generate_webui
```

## Notes

- Distances are weighted station-to-station costs, not travel minutes.
- Interchanges are represented as one station node.
- The bundled graph includes currently opened MRT stations on NSL, EWL, NEL, CCL, DTL, and TEL, including Hume and Punggol Coast.
- Future or unopened shell stations are not included as candidates.

## Test

```bash
python -m unittest discover -s tests
```
