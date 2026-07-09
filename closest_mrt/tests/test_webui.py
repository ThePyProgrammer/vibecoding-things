import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from closest_mrt.optimizer import normalize
from closest_mrt.singapore_mrt import LINES
from closest_mrt.station_coordinates import STATION_COORDINATES
from closest_mrt.webui import build_index_html


class WebUiTests(unittest.TestCase):
    def test_generates_static_html_app_with_optimizer_data(self):
        html = build_index_html()

        self.assertIn("<!doctype html>", html.lower())
        self.assertIn("results-body", html)
        self.assertIn("incoming-station", html)
        self.assertIn("outgoing-station", html)
        self.assertIn("person-list", html)
        self.assertIn("function addPerson", html)
        self.assertIn("function optimizerOrigins", html)
        self.assertIn("<span>Endpoints</span>", html)
        self.assertIn("transfer-penalty", html)
        self.assertIn("route-popover-layer", html)
        self.assertIn("result-map", html)
        self.assertIn("const STATION_COORDINATES", html)
        self.assertIn("const SINGAPORE_OUTLINE", html)
        self.assertIn("function shortestPaths", html)
        self.assertIn("function routeTimeline", html)
        self.assertIn("function renderResultMap", html)
        self.assertIn("function showResultOnMap", html)
        self.assertIn("function hideResultOnMap", html)
        self.assertIn("function routeOverlaySvg", html)
        self.assertIn("function routeSegments", html)
        self.assertIn("function routeLineForStep", html)
        self.assertIn("function mapPoint", html)
        self.assertIn("function singaporeOutlinePath", html)
        self.assertIn("function markerSvg", html)
        self.assertIn("function stationLineColors", html)
        self.assertIn("map-tooltip", html)
        self.assertIn('class="map-marker"', html)
        self.assertIn("<svg", html)
        self.assertIn("marker-end", html)
        self.assertIn("arrow-head", html)
        self.assertIn("data-result-index", html)
        self.assertNotIn("<canvas", html)
        self.assertNotIn("getContext", html)
        self.assertIn("function lineColor", html)
        self.assertIn("function showRoutePopover", html)
        self.assertIn("renderResults(results, origins)", html)
        self.assertIn('direction: endpointLabel', html)
        self.assertIn(
            'const displayRoute = item.origin.direction === "out" ? [...item.route].reverse() : item.route;',
            html,
        )
        self.assertNotIn("cursor: help", html)
        self.assertIn("position: fixed", html)
        self.assertIn("Best total cost", html)
        self.assertNotIn("Best imbalance", html)
        self.assertNotIn("<th>Balance</th>", html)
        self.assertNotIn(
            "Pick Singapore MRT stations and rank meeting points", html
        )
        self.assertIn(".actions .control-row", html)
        self.assertIn("Jurong East", html)
        self.assertIn("Punggol Coast", html)
        self.assertIn("function optimize", html)
        self.assertLess(html.index('class="map-card"'), html.index('class="table-wrap"'))
        self.assertNotIn('["#106c5b", "incoming"]', html)
        self.assertNotIn('["#d4412f", "outgoing"]', html)
        self.assertNotIn("{ lat: 1.237, lng: 103.829 }", html)

    def test_generated_app_is_written_to_index_html(self):
        html = build_index_html()

        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "index.html"
            path.write_text(html, encoding="utf-8")
            self.assertIn("Closest MRT", path.read_text(encoding="utf-8"))

    def test_station_coordinates_cover_every_web_station(self):
        missing = sorted(
            {
                name
                for stops in LINES.values()
                for name, _codes in stops
                if normalize(name) not in STATION_COORDINATES
            }
        )

        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
