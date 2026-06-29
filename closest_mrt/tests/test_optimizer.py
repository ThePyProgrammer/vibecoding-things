import unittest

from closest_mrt.optimizer import Graph, Station, optimize, resolve_station
from closest_mrt.singapore_mrt import build_graph


class OptimizerTests(unittest.TestCase):
    def test_resolves_station_names_and_codes_case_insensitively(self):
        graph = build_graph()

        self.assertEqual(resolve_station(graph, "jurong east").name, "Jurong East")
        self.assertEqual(resolve_station(graph, "NS1").name, "Jurong East")
        self.assertEqual(resolve_station(graph, "ew24").name, "Jurong East")

    def test_graph_contains_currently_opened_hume_connection(self):
        graph = build_graph()

        hume = resolve_station(graph, "Hume")
        hillview = resolve_station(graph, "Hillview")
        beauty_world = resolve_station(graph, "Beauty World")

        self.assertIn(hillview.id, graph.neighbors[hume.id])
        self.assertIn(beauty_world.id, graph.neighbors[hume.id])

    def test_optimizer_finds_middle_station_on_symmetric_simple_graph(self):
        graph = Graph()
        for name in ["A", "B", "C", "D", "E"]:
            graph.add_station(Station(id=name, name=name, codes=(name,)))
        for left, right in [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")]:
            graph.connect(left, right)

        results = optimize(graph, ["A", "E"], limit=2)

        self.assertEqual(results[0].station.name, "C")
        self.assertEqual(results[0].distances, {"A": 2, "E": 2})

    def test_transfer_penalty_can_make_same_line_route_better_than_fewer_hops(self):
        graph = Graph()
        for name in ["A", "B", "C", "D", "E"]:
            graph.add_station(Station(id=name, name=name, codes=(name,)))
        graph.connect("A", "B", line="red")
        graph.connect("B", "C", line="blue")
        graph.connect("A", "D", line="red")
        graph.connect("D", "E", line="red")
        graph.connect("E", "C", line="red")

        results = optimize(graph, ["A"], limit=5, transfer_penalty=5)
        c_result = next(result for result in results if result.station.name == "C")

        self.assertEqual(c_result.distances, {"A": 3})

    def test_transfer_penalty_can_be_disabled_for_plain_hop_counts(self):
        graph = Graph()
        for name in ["A", "B", "C", "D", "E"]:
            graph.add_station(Station(id=name, name=name, codes=(name,)))
        graph.connect("A", "B", line="red")
        graph.connect("B", "C", line="blue")
        graph.connect("A", "D", line="red")
        graph.connect("D", "E", line="red")
        graph.connect("E", "C", line="red")

        results = optimize(graph, ["A"], limit=5, transfer_penalty=0)
        c_result = next(result for result in results if result.station.name == "C")

        self.assertEqual(c_result.distances, {"A": 2})

    def test_optimizer_ranks_by_lowest_total_cost_before_balance(self):
        graph = Graph()
        station_names = [
            "O1",
            "O2",
            "O3",
            "Y",
            "X",
            "Y1",
            "Y2",
            "Y3",
            "Y4",
            "Y5",
            "X1A",
            "X2A",
            "X3A",
            "X1B",
            "X2B",
            "X3B",
            "X1C",
            "X2C",
            "X3C",
        ]
        for name in station_names:
            graph.add_station(Station(id=name, name=name, codes=(name,)))
        for left, right in [
            ("Y", "O1"),
            ("Y", "O2"),
            ("Y", "Y1"),
            ("Y1", "Y2"),
            ("Y2", "Y3"),
            ("Y3", "Y4"),
            ("Y4", "Y5"),
            ("Y5", "O3"),
            ("X", "X1A"),
            ("X1A", "X2A"),
            ("X2A", "X3A"),
            ("X3A", "O1"),
            ("X", "X1B"),
            ("X1B", "X2B"),
            ("X2B", "X3B"),
            ("X3B", "O2"),
            ("X", "X1C"),
            ("X1C", "X2C"),
            ("X2C", "X3C"),
            ("X3C", "O3"),
        ]:
            graph.connect(left, right)

        results = optimize(graph, ["O1", "O2", "O3"], limit=2, transfer_penalty=0)

        self.assertEqual(results[0].station.name, "Y")
        self.assertEqual(results[0].total_distance, 8)
        self.assertEqual(results[0].max_distance, 6)

    def test_optimizer_ranks_candidates_for_real_mrt_inputs(self):
        graph = build_graph()

        results = optimize(graph, ["Jurong East", "Punggol", "Tampines"], limit=5)

        self.assertEqual(len(results), 5)
        self.assertLessEqual(results[0].total_distance, results[-1].total_distance)
        self.assertTrue(all("Jurong East" in result.distances for result in results))
        self.assertTrue(all("Punggol" in result.distances for result in results))
        self.assertTrue(all("Tampines" in result.distances for result in results))


if __name__ == "__main__":
    unittest.main()
