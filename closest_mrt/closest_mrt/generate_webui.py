from __future__ import annotations

from .webui import write_index_html


def main() -> None:
    path = write_index_html()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
