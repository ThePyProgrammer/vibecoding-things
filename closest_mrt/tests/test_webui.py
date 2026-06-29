import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

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
        self.assertIn("function shortestPaths", html)
        self.assertIn("function routeTimeline", html)
        self.assertIn("function lineColor", html)
        self.assertIn("function showRoutePopover", html)
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

    def test_generated_app_is_written_to_index_html(self):
        html = build_index_html()

        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "index.html"
            path.write_text(html, encoding="utf-8")
            self.assertIn("Closest MRT", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
