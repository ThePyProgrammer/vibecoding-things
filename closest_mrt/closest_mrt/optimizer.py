from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from re import sub


def normalize(value: str) -> str:
    return sub(r"[^a-z0-9]+", "", value.lower())


@dataclass(frozen=True)
class Station:
    id: str
    name: str
    codes: tuple[str, ...] = ()


@dataclass(frozen=True)
class OptimizationResult:
    station: Station
    distances: dict[str, int]
    max_distance: int
    total_distance: int
    imbalance: int
    score: tuple[int, int, str]


class Graph:
    def __init__(self) -> None:
        self.stations: dict[str, Station] = {}
        self.neighbors: dict[str, set[str]] = {}
        self.edge_lines: dict[tuple[str, str], set[str]] = {}
        self.aliases: dict[str, str] = {}

    def add_station(self, station: Station) -> None:
        if station.id in self.stations:
            existing = self.stations[station.id]
            codes = tuple(dict.fromkeys((*existing.codes, *station.codes)))
            station = Station(id=existing.id, name=existing.name, codes=codes)

        self.stations[station.id] = station
        self.neighbors.setdefault(station.id, set())
        for alias in (station.name, station.id, *station.codes):
            self.aliases[normalize(alias)] = station.id

    def connect(self, left_id: str, right_id: str, line: str = "line") -> None:
        if left_id not in self.stations or right_id not in self.stations:
            raise ValueError(f"Cannot connect unknown stations: {left_id}, {right_id}")
        self.neighbors[left_id].add(right_id)
        self.neighbors[right_id].add(left_id)
        self.edge_lines.setdefault((left_id, right_id), set()).add(line)
        self.edge_lines.setdefault((right_id, left_id), set()).add(line)


def resolve_station(graph: Graph, value: str) -> Station:
    try:
        return graph.stations[graph.aliases[normalize(value)]]
    except KeyError as exc:
        suggestions = _suggestions(graph, value)
        suffix = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
        raise ValueError(f"Unknown station '{value}'.{suffix}") from exc


def optimize(
    graph: Graph,
    inputs: list[str],
    limit: int = 10,
    transfer_penalty: int = 2,
) -> list[OptimizationResult]:
    if not inputs:
        raise ValueError("Provide at least one MRT station.")
    if limit < 1:
        raise ValueError("Limit must be at least 1.")
    if transfer_penalty < 0:
        raise ValueError("Transfer penalty cannot be negative.")

    origins = [resolve_station(graph, value) for value in inputs]
    distances_by_origin = {
        origin.id: _shortest_distances(graph, origin.id, transfer_penalty)
        for origin in origins
    }

    results: list[OptimizationResult] = []
    for candidate in graph.stations.values():
        candidate_distances: dict[str, int] = {}
        for origin in origins:
            distance = distances_by_origin[origin.id].get(candidate.id)
            if distance is None:
                break
            candidate_distances[origin.name] = distance
        else:
            values = list(candidate_distances.values())
            max_distance = max(values)
            total_distance = sum(values)
            imbalance = max(values) - min(values)
            score = (total_distance, max_distance, candidate.name)
            results.append(
                OptimizationResult(
                    station=candidate,
                    distances=candidate_distances,
                    max_distance=max_distance,
                    total_distance=total_distance,
                    imbalance=imbalance,
                    score=score,
                )
            )

    return sorted(results, key=lambda result: result.score)[:limit]


def _shortest_distances(
    graph: Graph, start_id: str, transfer_penalty: int = 2
) -> dict[str, int]:
    if not graph.edge_lines:
        return _plain_shortest_distances(graph, start_id)

    best_by_state: dict[tuple[str, str | None], int] = {(start_id, None): 0}
    queue: list[tuple[int, str, str | None]] = [(0, start_id, None)]

    while queue:
        cost, current_id, current_line = heappop(queue)
        if cost != best_by_state[(current_id, current_line)]:
            continue

        for neighbor_id in graph.neighbors[current_id]:
            edge_lines = graph.edge_lines.get((current_id, neighbor_id), {"line"})
            for edge_line in edge_lines:
                line_change_cost = (
                    transfer_penalty
                    if current_line is not None and edge_line != current_line
                    else 0
                )
                next_cost = cost + 1 + line_change_cost
                next_state = (neighbor_id, edge_line)
                if next_cost < best_by_state.get(next_state, float("inf")):
                    best_by_state[next_state] = next_cost
                    heappush(queue, (next_cost, neighbor_id, edge_line))

    distances: dict[str, int] = {}
    for (station_id, _line), cost in best_by_state.items():
        distances[station_id] = min(cost, distances.get(station_id, cost))

    return distances


def _plain_shortest_distances(graph: Graph, start_id: str) -> dict[str, int]:
    distances = {start_id: 0}
    queue = deque([start_id])

    while queue:
        current = queue.popleft()
        for neighbor in graph.neighbors[current]:
            if neighbor in distances:
                continue
            distances[neighbor] = distances[current] + 1
            queue.append(neighbor)

    return distances


def _suggestions(graph: Graph, value: str) -> list[str]:
    needle = normalize(value)
    if not needle:
        return []

    matches = [
        station.name
        for station in graph.stations.values()
        if needle in normalize(station.name)
    ]
    return sorted(matches)[:5]
