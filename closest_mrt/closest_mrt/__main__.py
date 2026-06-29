from __future__ import annotations

import argparse

from .optimizer import optimize
from .singapore_mrt import build_graph


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Suggest central Singapore MRT stations for a list of MRT stops."
    )
    parser.add_argument("stations", nargs="+", help="MRT station names or codes")
    parser.add_argument("-n", "--limit", type=int, default=10, help="number of results")
    parser.add_argument(
        "--transfer-penalty",
        type=int,
        default=2,
        help="extra cost added whenever a route changes MRT lines",
    )
    args = parser.parse_args()

    results = optimize(
        build_graph(),
        args.stations,
        limit=args.limit,
        transfer_penalty=args.transfer_penalty,
    )
    origins = list(results[0].distances) if results else []

    print("rank station total-cost max-cost " + " ".join(origins))
    for index, result in enumerate(results, start=1):
        distances = " ".join(str(result.distances[origin]) for origin in origins)
        print(
            f"{index:>4} {result.station.name:<24} "
            f"{result.total_distance:>5} {result.max_distance:>8} {distances}"
        )


if __name__ == "__main__":
    main()
