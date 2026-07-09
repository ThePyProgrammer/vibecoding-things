from __future__ import annotations

import json
from pathlib import Path

from .singapore_mrt import LINES, LINE_GROUPS
from .station_coordinates import STATION_COORDINATES


def build_index_html() -> str:
    line_data = json.dumps(LINES, indent=2)
    line_groups = json.dumps(LINE_GROUPS, indent=2)
    station_coordinates = json.dumps(STATION_COORDINATES, indent=2)
    return TEMPLATE.replace("__LINE_DATA__", line_data).replace(
        "__LINE_GROUPS__", line_groups
    ).replace(
        "__STATION_COORDINATES__", station_coordinates
    )


def write_index_html(path: str | Path = "index.html") -> Path:
    output_path = Path(path)
    output_path.write_text(build_index_html(), encoding="utf-8")
    return output_path


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Closest MRT</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #1b2628;
      --muted: #607071;
      --line: #d7dfdc;
      --paper: #f4f1e8;
      --panel: #fffdf7;
      --panel-strong: #fdf5df;
      --green: #106c5b;
      --red: #d4412f;
      --yellow: #f0b43c;
      --blue: #2463a6;
      --shadow: 0 18px 50px rgba(23, 40, 41, 0.12);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background:
        linear-gradient(90deg, rgba(27, 38, 40, 0.05) 1px, transparent 1px),
        linear-gradient(180deg, rgba(27, 38, 40, 0.04) 1px, transparent 1px),
        var(--paper);
      background-size: 24px 24px;
      color: var(--ink);
      font-family: Avenir Next, Trebuchet MS, Verdana, sans-serif;
      min-height: 100vh;
    }

    main {
      width: min(1180px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 34px 0 48px;
    }

    .masthead {
      border-bottom: 3px solid var(--ink);
      padding-bottom: 22px;
    }

    h1 {
      margin: 0;
      max-width: 760px;
      font-family: Georgia, Iowan Old Style, serif;
      font-size: clamp(2.4rem, 7vw, 6.8rem);
      font-weight: 900;
      letter-spacing: 0;
      line-height: 0.9;
    }

    .workspace {
      display: grid;
      grid-template-columns: minmax(320px, 420px) minmax(0, 1fr);
      gap: 22px;
      margin-top: 24px;
      align-items: start;
    }

    .panel {
      background: var(--panel);
      border: 2px solid var(--ink);
      box-shadow: var(--shadow);
    }

    .controls {
      position: sticky;
      top: 18px;
      padding: 18px;
    }

    .control-row {
      display: grid;
      gap: 8px;
      margin-bottom: 16px;
    }

    label {
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }

    .input-line {
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 10px;
    }

    input {
      width: 100%;
      min-height: 44px;
      border: 2px solid var(--ink);
      background: #ffffff;
      color: var(--ink);
      font: inherit;
      padding: 9px 11px;
      outline: none;
    }

    input:focus {
      box-shadow: 0 0 0 4px rgba(240, 180, 60, 0.35);
    }

    button {
      min-height: 44px;
      border: 2px solid var(--ink);
      background: var(--ink);
      color: #fffdf7;
      cursor: pointer;
      font: inherit;
      font-weight: 800;
      padding: 9px 14px;
      transition: transform 140ms ease, box-shadow 140ms ease;
    }

    button:hover {
      box-shadow: 4px 4px 0 var(--yellow);
      transform: translate(-2px, -2px);
    }

    button.secondary {
      background: var(--panel-strong);
      color: var(--ink);
    }

    .chips {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      min-height: 36px;
      margin: 8px 0 16px;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      border: 2px solid var(--ink);
      background: var(--panel-strong);
      padding: 6px 8px;
      font-weight: 800;
    }

    .chip span {
      color: var(--muted);
      font-size: 0.78rem;
      font-weight: 700;
    }

    .chip button {
      width: 24px;
      height: 24px;
      min-height: 24px;
      padding: 0;
      line-height: 1;
    }

    .person-list {
      display: grid;
      gap: 12px;
      margin-bottom: 16px;
    }

    .person-row {
      background: var(--panel-strong);
      border: 2px solid var(--ink);
      padding: 10px;
    }

    .person-header {
      align-items: center;
      display: flex;
      justify-content: space-between;
      margin-bottom: 10px;
    }

    .person-title {
      font-weight: 900;
    }

    .endpoint-grid {
      display: grid;
      gap: 10px;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    }

    .person-row .control-row {
      margin-bottom: 0;
    }

    .remove-person {
      min-height: 30px;
      padding: 2px 8px;
    }

    .actions {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) auto;
      gap: 10px;
      align-items: end;
    }

    .actions .control-row {
      margin-bottom: 0;
    }

    .actions input {
      max-width: 120px;
    }

    .actions button {
      align-self: end;
    }

    .message {
      min-height: 22px;
      margin: 14px 0 0;
      color: var(--red);
      font-weight: 800;
    }

    .summary {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      border-bottom: 2px solid var(--ink);
      background: var(--panel-strong);
    }

    .metric {
      padding: 14px 16px;
      border-right: 2px solid var(--ink);
    }

    .metric:last-child {
      border-right: 0;
    }

    .metric strong {
      display: block;
      font-family: Georgia, Iowan Old Style, serif;
      font-size: 1.8rem;
      line-height: 1;
    }

    .metric span {
      display: block;
      color: var(--muted);
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.07em;
      margin-top: 5px;
      text-transform: uppercase;
    }

    .table-wrap {
      overflow-x: auto;
    }

    .map-card {
      background:
        linear-gradient(135deg, rgba(36, 99, 166, 0.08), transparent 44%),
        linear-gradient(315deg, rgba(240, 180, 60, 0.22), transparent 38%),
        #dfe9e0;
      border-bottom: 2px solid var(--ink);
      padding: 14px;
    }

    .map-header {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
    }

    .map-title {
      font-family: Georgia, Iowan Old Style, serif;
      font-size: 1.2rem;
      font-weight: 900;
      line-height: 1;
    }

    .map-status {
      color: var(--muted);
      font-size: 0.76rem;
      font-weight: 900;
      letter-spacing: 0.07em;
      text-align: right;
      text-transform: uppercase;
    }

    .map-shell {
      border: 2px solid var(--ink);
      background: #bad8dc;
      min-height: 250px;
      position: relative;
    }

    .result-map {
      display: block;
      width: 100%;
      height: auto;
      min-height: 250px;
    }

    .map-marker {
      cursor: pointer;
      outline: none;
    }

    .map-marker circle,
    .map-marker path {
      vector-effect: non-scaling-stroke;
    }

    .map-marker:focus .marker-hit,
    .map-marker:hover .marker-hit {
      stroke-width: 4;
    }

    .route-overlay {
      fill: none;
      opacity: 0.9;
      stroke-linecap: round;
      stroke-linejoin: round;
      stroke-width: 3.5;
      vector-effect: non-scaling-stroke;
    }

    .marker-label {
      fill: var(--ink);
      font: 800 12px Avenir Next, Trebuchet MS, sans-serif;
      paint-order: stroke;
      pointer-events: none;
      stroke: rgba(255, 253, 247, 0.9);
      stroke-linejoin: round;
      stroke-width: 4;
    }

    .map-tooltip {
      background: var(--ink);
      border: 2px solid var(--ink);
      box-shadow: 4px 4px 0 rgba(240, 180, 60, 0.85);
      color: #fffdf7;
      display: none;
      font-size: 0.82rem;
      font-weight: 800;
      left: 0;
      line-height: 1.25;
      max-width: min(260px, calc(100% - 24px));
      padding: 9px 10px;
      pointer-events: none;
      position: absolute;
      top: 0;
      transform: translate(12px, -50%);
      z-index: 3;
    }

    .map-tooltip.is-visible {
      display: block;
    }

    .map-tooltip span {
      color: #d7dfdc;
      display: block;
      font-size: 0.72rem;
      letter-spacing: 0.06em;
      margin-top: 3px;
      text-transform: uppercase;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 720px;
    }

    th,
    td {
      border-bottom: 1px solid var(--line);
      padding: 12px 14px;
      text-align: left;
      vertical-align: top;
    }

    th {
      background: #ffffff;
      color: var(--muted);
      font-size: 0.74rem;
      font-weight: 900;
      letter-spacing: 0.07em;
      position: sticky;
      top: 0;
      text-transform: uppercase;
      z-index: 1;
    }

    tbody tr:nth-child(odd) {
      background: rgba(16, 108, 91, 0.045);
    }

    tbody tr[data-result-index] {
      cursor: pointer;
    }

    tbody tr[data-result-index]:hover,
    tbody tr[data-result-index]:focus-within,
    tbody tr[data-result-index].is-map-active {
      background: rgba(240, 180, 60, 0.24);
    }

    .rank {
      width: 56px;
      color: var(--blue);
      font-weight: 900;
    }

    .station-name {
      font-weight: 900;
    }

    .codes {
      color: var(--muted);
      display: block;
      font-size: 0.82rem;
      font-weight: 700;
      margin-top: 3px;
    }

    .distance-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    .distance-pill {
      background: #ffffff;
      border: 1px solid var(--line);
      color: var(--ink);
      display: inline-flex;
      gap: 6px;
      padding: 4px 7px;
      white-space: nowrap;
    }

    .distance-pill:focus {
      box-shadow: 0 0 0 4px rgba(240, 180, 60, 0.35);
      outline: none;
    }

    .distance-pill strong {
      color: var(--green);
    }

    .route-popover {
      background: var(--ink);
      border: 2px solid var(--ink);
      box-shadow: var(--shadow);
      color: #fffdf7;
      display: none;
      left: 0;
      max-height: min(560px, calc(100vh - 32px));
      overflow: auto;
      padding: 12px;
      position: fixed;
      top: 0;
      width: min(420px, calc(100vw - 32px));
      white-space: normal;
      z-index: 1000;
    }

    .route-popover.is-visible {
      display: block;
    }

    .route-title {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      font-size: 0.78rem;
      font-weight: 900;
      letter-spacing: 0.06em;
      margin-bottom: 10px;
      text-transform: uppercase;
    }

    .route-timeline {
      display: grid;
      gap: 0;
      margin: 0;
      padding: 0;
    }

    .route-step {
      display: grid;
      grid-template-columns: 20px minmax(0, 1fr);
      min-height: 28px;
      position: relative;
    }

    .route-step::before {
      background: var(--route-color, var(--line));
      content: "";
      display: block;
      grid-column: 1;
      justify-self: center;
      margin-top: 18px;
      min-height: 18px;
      width: 5px;
    }

    .route-step:last-child::before {
      display: none;
    }

    .route-dot {
      background: #fffdf7;
      border: 3px solid var(--route-color, var(--yellow));
      border-radius: 50%;
      grid-column: 1;
      height: 15px;
      left: 2px;
      position: absolute;
      top: 2px;
      width: 15px;
    }

    .route-stop {
      grid-column: 2;
      line-height: 1.25;
      padding: 0 0 10px 4px;
    }

    .route-stop strong {
      color: #fffdf7;
      display: block;
      font-size: 0.88rem;
    }

    .route-stop span {
      color: #d7dfdc;
      display: block;
      font-size: 0.76rem;
      margin-top: 2px;
    }

    .empty {
      padding: 42px 20px;
      color: var(--muted);
      text-align: center;
    }

    @media (max-width: 860px) {
      main {
        width: min(100vw - 22px, 680px);
        padding-top: 22px;
      }

      .masthead,
      .workspace {
        grid-template-columns: 1fr;
      }

      .controls {
        position: static;
      }

      .actions {
        grid-template-columns: 1fr;
      }

      .endpoint-grid {
        grid-template-columns: 1fr;
      }

      .summary {
        grid-template-columns: 1fr;
      }

      .map-header {
        align-items: flex-start;
        flex-direction: column;
      }

      .map-status {
        text-align: left;
      }

      .metric {
        border-right: 0;
        border-bottom: 2px solid var(--ink);
      }

      .metric:last-child {
        border-bottom: 0;
      }
    }
  </style>
</head>
<body>
  <main>
    <header class="masthead">
      <h1>Closest MRT</h1>
    </header>

    <section class="workspace" aria-label="MRT central station optimizer">
      <form class="panel controls" id="optimizer-form">
        <div class="person-list" id="person-list" aria-live="polite"></div>
        <button class="secondary" type="button" id="add-person">Add person</button>
        <datalist id="station-options"></datalist>

        <div class="actions">
          <div class="control-row">
            <label for="result-limit">Results</label>
            <input id="result-limit" type="number" min="1" max="25" value="10" />
          </div>
          <div class="control-row">
            <label for="transfer-penalty">Transfer penalty</label>
            <input id="transfer-penalty" type="number" min="0" max="12" value="2" />
          </div>
          <button type="submit">Find centre</button>
        </div>

        <p class="message" id="message" role="status" aria-live="polite"></p>
        <button class="secondary" type="button" id="load-example">Use example</button>
      </form>

      <section class="panel results" aria-label="Ranked station results">
        <div class="summary">
          <div class="metric"><strong id="station-count">0</strong><span>Endpoints</span></div>
          <div class="metric"><strong id="best-total">-</strong><span>Best total cost</span></div>
          <div class="metric"><strong id="best-max">-</strong><span>Best max cost</span></div>
        </div>

        <div class="map-card" aria-label="Coordinate sketch of generated station options">
          <div class="map-header">
            <span class="map-title">Very serious coordinate map</span>
            <span class="map-status" id="map-status">Hover a result</span>
          </div>
          <div class="map-shell">
            <svg class="result-map" id="result-map" viewBox="0 0 900 430" role="img" aria-label="Interactive Singapore sketch map of generated MRT options"></svg>
            <div class="map-tooltip" id="map-tooltip"></div>
          </div>
        </div>

        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Rank</th>
                <th>Station</th>
                <th>Total cost</th>
                <th>Max cost</th>
                <th>Origin costs</th>
              </tr>
            </thead>
            <tbody id="results-body">
              <tr><td class="empty" colspan="5">Add at least one incoming or outgoing station, then run the optimizer.</td></tr>
            </tbody>
          </table>
        </div>
      </section>
    </section>
  </main>
  <aside class="route-popover" id="route-popover-layer" role="tooltip" aria-hidden="true"></aside>

  <script>
    const LINE_DATA = __LINE_DATA__;
    const LINE_GROUPS = __LINE_GROUPS__;
    const STATION_COORDINATES = __STATION_COORDINATES__;
    const SINGAPORE_OUTLINE = [
      [
        { lat: 1.304, lng: 103.604 },
        { lat: 1.336, lng: 103.632 },
        { lat: 1.363, lng: 103.676 },
        { lat: 1.386, lng: 103.728 },
        { lat: 1.430, lng: 103.782 },
        { lat: 1.466, lng: 103.832 },
        { lat: 1.454, lng: 103.884 },
        { lat: 1.417, lng: 103.934 },
        { lat: 1.385, lng: 104.012 },
        { lat: 1.335, lng: 104.035 },
        { lat: 1.302, lng: 103.992 },
        { lat: 1.285, lng: 103.926 },
        { lat: 1.255, lng: 103.861 },
        { lat: 1.246, lng: 103.801 },
        { lat: 1.266, lng: 103.736 },
        { lat: 1.282, lng: 103.670 },
        { lat: 1.304, lng: 103.604 }
      ]
    ];
    const LINE_COLORS = {
      "North South Line": "#d42e12",
      "East West Line": "#009645",
      "North East Line": "#9900aa",
      "Circle Line": "#fa9e0d",
      "Downtown Line": "#005ec4",
      "Thomson-East Coast Line": "#9d5b25"
    };
    const EXAMPLE_PEOPLE = [
      { incoming: "Jurong East", outgoing: "Orchard" },
      { incoming: "Punggol", outgoing: "HarbourFront" },
      { incoming: "Tampines", outgoing: "Expo" }
    ];
    const MAP_WIDTH = 900;
    const MAP_HEIGHT = 430;
    const MAP_PADDING = 42;

    const state = {
      people: [],
      nextPersonId: 1,
      mapItems: [],
      mapHoverItem: null,
      mapProjection: null,
      graph: buildGraph(LINE_DATA)
    };

    const datalist = document.querySelector("#station-options");
    const personList = document.querySelector("#person-list");
    const form = document.querySelector("#optimizer-form");
    const message = document.querySelector("#message");
    const resultLimit = document.querySelector("#result-limit");
    const transferPenalty = document.querySelector("#transfer-penalty");
    const resultsBody = document.querySelector("#results-body");
    const stationCount = document.querySelector("#station-count");
    const bestTotal = document.querySelector("#best-total");
    const bestMax = document.querySelector("#best-max");
    const routePopover = document.querySelector("#route-popover-layer");
    const resultMap = document.querySelector("#result-map");
    const mapStatus = document.querySelector("#map-status");
    const mapTooltip = document.querySelector("#map-tooltip");

    hydrateDatalist();
    addPerson();
    renderResultMap([], []);
    resultMap.addEventListener("mouseleave", hideMapTooltip);

    document.querySelector("#add-person").addEventListener("click", () => {
      addPerson();
    });

    document.querySelector("#load-example").addEventListener("click", () => {
      state.people = EXAMPLE_PEOPLE.map((person) => ({
        id: state.nextPersonId++,
        incoming: person.incoming,
        outgoing: person.outgoing
      }));
      renderPeople();
      runOptimizer();
    });

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      runOptimizer();
    });

    function normalize(value) {
      return String(value).toLowerCase().replace(/[^a-z0-9]+/g, "");
    }

    function buildGraph(lines) {
      const stations = new Map();
      const neighbors = new Map();
      const edgeLines = new Map();
      const aliases = new Map();

      for (const stops of Object.values(lines)) {
        for (const [name, codes] of stops) {
          const id = normalize(name);
          if (!stations.has(id)) {
            stations.set(id, { id, name, codes: [] });
            neighbors.set(id, new Set());
          }
          const station = stations.get(id);
          for (const code of codes) {
            if (!station.codes.includes(code)) station.codes.push(code);
          }
          [station.name, station.id, ...station.codes].forEach((alias) => {
            aliases.set(normalize(alias), station.id);
          });
        }
      }

      for (const [lineName, stops] of Object.entries(lines)) {
        const line = LINE_GROUPS[lineName] || lineName;
        for (let index = 0; index < stops.length - 1; index += 1) {
          const left = normalize(stops[index][0]);
          const right = normalize(stops[index + 1][0]);
          neighbors.get(left).add(right);
          neighbors.get(right).add(left);
          addEdgeLine(edgeLines, left, right, line);
          addEdgeLine(edgeLines, right, left, line);
        }
      }

      return { stations, neighbors, edgeLines, aliases };
    }

    function addEdgeLine(edgeLines, from, to, line) {
      const key = `${from}|${to}`;
      if (!edgeLines.has(key)) edgeLines.set(key, new Set());
      edgeLines.get(key).add(line);
    }

    function hydrateDatalist() {
      const options = [...state.graph.stations.values()]
        .sort((a, b) => a.name.localeCompare(b.name))
        .flatMap((station) => [
          station.name,
          ...station.codes.map((code) => `${code} - ${station.name}`)
        ]);

      datalist.innerHTML = options.map((option) => `<option value="${escapeHtml(option)}"></option>`).join("");
    }

    function resolveStation(value) {
      const cleaned = String(value).split(" - ")[0].trim();
      const stationId = state.graph.aliases.get(normalize(cleaned));
      if (!stationId) {
        throw new Error(`Unknown station: ${value}`);
      }
      return state.graph.stations.get(stationId);
    }

    function addPerson() {
      state.people.push({ id: state.nextPersonId++, incoming: "", outgoing: "" });
      renderPeople();
    }

    function renderPeople() {
      personList.innerHTML = state.people.map((person, index) => `
        <section class="person-row" data-person-id="${person.id}">
          <div class="person-header">
            <span class="person-title">Person ${personLabel(index)}</span>
            <button class="secondary remove-person" type="button" data-remove-person="${person.id}" aria-label="Remove Person ${personLabel(index)}">Remove</button>
          </div>
          <div class="endpoint-grid">
            <div class="control-row">
              <label for="incoming-station-${person.id}">Incoming</label>
              <input id="incoming-station-${person.id}" class="incoming-station" list="station-options" autocomplete="off" placeholder="Coming from" value="${escapeAttribute(person.incoming)}" data-endpoint="incoming" />
            </div>
            <div class="control-row">
              <label for="outgoing-station-${person.id}">Outgoing</label>
              <input id="outgoing-station-${person.id}" class="outgoing-station" list="station-options" autocomplete="off" placeholder="Going to" value="${escapeAttribute(person.outgoing)}" data-endpoint="outgoing" />
            </div>
          </div>
        </section>
      `).join("");

      personList.querySelectorAll("[data-remove-person]").forEach((button) => {
        button.addEventListener("click", () => {
          state.people = state.people.filter((person) => String(person.id) !== button.dataset.removePerson);
          if (!state.people.length) addPerson();
          renderPeople();
        });
      });

      personList.querySelectorAll("input[data-endpoint]").forEach((input) => {
        input.addEventListener("input", () => {
          const row = input.closest(".person-row");
          const person = state.people.find((item) => String(item.id) === row.dataset.personId);
          if (person) person[input.dataset.endpoint] = input.value;
        });
      });
    }

    function personLabel(index) {
      return String.fromCharCode(65 + index);
    }

    function optimize(origins, limit, lineChangePenalty) {
      const pathsByOrigin = new Map(
        origins.map((origin) => [origin.key, shortestPaths(origin.stationId, lineChangePenalty)])
      );

      return [...state.graph.stations.values()]
        .map((candidate) => {
          const distances = origins.map((origin) => {
            const pathInfo = pathsByOrigin.get(origin.key).get(candidate.id);
            return {
              origin,
              hops: pathInfo?.cost,
              route: pathInfo?.path || []
            };
          });
          if (distances.some((item) => item.hops === undefined)) return null;

          const values = distances.map((item) => item.hops);
          const max = Math.max(...values);
          const min = Math.min(...values);
          const total = values.reduce((sum, value) => sum + value, 0);

          return {
            station: candidate,
            distances,
            maxDistance: max,
            imbalance: max - min,
            totalDistance: total
          };
        })
        .filter(Boolean)
        .sort((a, b) =>
          a.totalDistance - b.totalDistance ||
          a.maxDistance - b.maxDistance ||
          a.station.name.localeCompare(b.station.name)
        )
        .slice(0, limit);
    }

    function shortestPaths(startId, lineChangePenalty) {
      const bestByState = new Map([[`${startId}|`, 0]]);
      const pathsByState = new Map([[`${startId}|`, [{ stationId: startId, line: "" }]]]);
      const queue = [{ cost: 0, stationId: startId, line: "" }];

      while (queue.length) {
        queue.sort((a, b) => b.cost - a.cost);
        const current = queue.pop();
        const currentKey = `${current.stationId}|${current.line}`;
        if (current.cost !== bestByState.get(currentKey)) continue;

        for (const neighbor of state.graph.neighbors.get(current.stationId)) {
          const edgeKey = `${current.stationId}|${neighbor}`;
          const edgeLines = state.graph.edgeLines.get(edgeKey) || new Set(["line"]);
          for (const edgeLine of edgeLines) {
            const transferCost = current.line && edgeLine !== current.line ? lineChangePenalty : 0;
            const nextCost = current.cost + 1 + transferCost;
            const nextKey = `${neighbor}|${edgeLine}`;
            if (nextCost < (bestByState.get(nextKey) ?? Infinity)) {
              bestByState.set(nextKey, nextCost);
              pathsByState.set(nextKey, [
                ...pathsByState.get(currentKey),
                { stationId: neighbor, line: edgeLine }
              ]);
              queue.push({ cost: nextCost, stationId: neighbor, line: edgeLine });
            }
          }
        }
      }

      const distances = new Map();
      for (const [key, cost] of bestByState.entries()) {
        const [stationId] = key.split("|");
        const previous = distances.get(stationId);
        if (!previous || cost < previous.cost) {
          distances.set(stationId, { cost, path: pathsByState.get(key) });
        }
      }
      return distances;
    }

    function runOptimizer() {
      clearMessage();
      let origins;
      try {
        origins = optimizerOrigins();
      } catch (error) {
        showMessage(error.message);
        return;
      }
      if (!origins.length) {
        showMessage("Add at least one incoming or outgoing MRT station.");
        return;
      }
      stationCount.textContent = String(origins.length);

      const limit = Math.max(1, Math.min(25, Number(resultLimit.value) || 10));
      resultLimit.value = String(limit);
      const lineChangePenalty = Math.max(0, Math.min(12, Number(transferPenalty.value) || 0));
      transferPenalty.value = String(lineChangePenalty);
      const results = optimize(origins, limit, lineChangePenalty);
      renderResults(results, origins);
    }

    function optimizerOrigins() {
      const origins = [];
      state.people.forEach((person, index) => {
        const label = personLabel(index);
        for (const endpoint of ["incoming", "outgoing"]) {
          const value = person[endpoint].trim();
          if (!value) continue;
          const station = resolveStation(value);
          const endpointLabel = endpoint === "incoming" ? "in" : "out";
          origins.push({
            ...station,
            key: `${person.id}-${endpoint}-${station.id}`,
            direction: endpointLabel,
            stationId: station.id,
            name: `${label} ${endpointLabel}: ${station.name}`
          });
        }
      });
      return origins;
    }

    function renderResults(results, origins) {
      if (!results.length) {
        resultsBody.innerHTML = `<tr><td class="empty" colspan="5">No connected station candidates found.</td></tr>`;
        bestTotal.textContent = "-";
        bestMax.textContent = "-";
        hideRoutePopover();
        renderResultMap([], origins);
        return;
      }

      hideRoutePopover();
      bestTotal.textContent = String(results[0].totalDistance);
      bestMax.textContent = String(results[0].maxDistance);
      renderResultMap(results, origins);
      resultsBody.innerHTML = results.map((result, index) => `
        <tr data-result-index="${index}" tabindex="0">
          <td class="rank">${index + 1}</td>
          <td>
            <span class="station-name">${escapeHtml(result.station.name)}</span>
            <span class="codes">${escapeHtml(result.station.codes.join(" / "))}</span>
          </td>
          <td>${result.totalDistance}</td>
          <td>${result.maxDistance}</td>
          <td>
            <div class="distance-grid">
              ${result.distances.map((item) => `
                <span class="distance-pill" tabindex="0" data-route="${escapeAttribute(routeTimeline(item, result.station))}">
                  ${escapeHtml(item.origin.name)} <strong>${item.hops}</strong>
                </span>
              `).join("")}
            </div>
          </td>
        </tr>
      `).join("");

      resultsBody.querySelectorAll("[data-result-index]").forEach((row) => {
        const result = results[Number(row.dataset.resultIndex)];
        row.addEventListener("mouseenter", () => showResultOnMap(result, Number(row.dataset.resultIndex), row));
        row.addEventListener("focusin", () => showResultOnMap(result, Number(row.dataset.resultIndex), row));
        row.addEventListener("mouseleave", () => hideResultOnMap(row));
        row.addEventListener("focusout", () => hideResultOnMap(row));
      });

      resultsBody.querySelectorAll(".distance-pill").forEach((pill) => {
        pill.addEventListener("mouseenter", () => showRoutePopover(pill));
        pill.addEventListener("focus", () => showRoutePopover(pill));
        pill.addEventListener("mouseleave", hideRoutePopover);
        pill.addEventListener("blur", hideRoutePopover);
      });
    }

    function showResultOnMap(result, index, row) {
      resultsBody.querySelectorAll("[data-result-index]").forEach((item) => {
        item.classList.toggle("is-map-active", item === row);
      });
      renderMapSvg({ ...result, rank: index + 1 });
      mapStatus.textContent = `Showing ${result.station.name}: in -> option -> out routes`;
    }

    function hideResultOnMap(row) {
      row.classList.remove("is-map-active");
      renderMapSvg();
      mapStatus.textContent = state.lastResults?.length
        ? "Hover a result to plot its exact routes"
        : "Singapore shadow ready";
    }

    function renderResultMap(results, origins) {
      const coordinates = [
        ...Object.values(STATION_COORDINATES),
        ...SINGAPORE_OUTLINE.flat()
      ];
      const projection = mapProjection(coordinates, MAP_WIDTH, MAP_HEIGHT, MAP_PADDING);
      const candidates = results.map((result, index) => ({
        id: result.station.id,
        name: result.station.name,
        codes: result.station.codes,
        rank: index + 1,
        kind: "candidate",
        detail: `${result.totalDistance} total, ${result.maxDistance} max`,
        coordinate: STATION_COORDINATES[result.station.id]
      })).filter((item) => item.coordinate);
      const endpoints = origins.map((origin) => ({
        id: origin.stationId,
        name: origin.name,
        codes: origin.codes,
        rank: null,
        kind: "endpoint",
        direction: origin.direction,
        detail: `${origin.codes.join(" / ")} endpoint`,
        coordinate: STATION_COORDINATES[origin.stationId]
      })).filter((item) => item.coordinate);

      state.lastResults = results;
      state.lastOrigins = origins;
      state.mapProjection = projection;
      state.mapItems = [
        ...endpoints.map((item) => ({ ...item, layer: "endpoint" }))
      ].map((item) => {
        const point = mapPoint(item.coordinate, projection);
        return {
          ...item,
          x: point.x,
          y: point.y,
          colors: stationLineColors(item.codes),
          radius: 4.5
        };
      });
      renderMapSvg();

      mapStatus.textContent = candidates.length
        ? "Hover a result to plot its exact routes"
        : "Singapore shadow ready";
    }

    function renderMapSvg(activeResult) {
      const candidate = activeResult
        ? {
            ...activeResult.station,
            kind: "candidate",
            rank: activeResult.rank,
            detail: `${activeResult.totalDistance} total, ${activeResult.maxDistance} max`,
            coordinate: STATION_COORDINATES[activeResult.station.id]
          }
        : null;
      const candidatePoint = candidate?.coordinate ? mapPoint(candidate.coordinate, state.mapProjection) : null;
      const candidateItem = candidatePoint
        ? {
            ...candidate,
            x: candidatePoint.x,
            y: candidatePoint.y,
            colors: stationLineColors(candidate.codes),
            radius: 6
          }
        : null;
      resultMap.innerHTML = [
        svgDefs(),
        `<rect class="map-water" width="${MAP_WIDTH}" height="${MAP_HEIGHT}" fill="url(#map-water-gradient)"></rect>`,
        cloudSvg(),
        singaporeOutlinePath(state.mapProjection),
        coordinateGridSvg(MAP_WIDTH, MAP_HEIGHT, MAP_PADDING),
        activeResult ? routeOverlaySvg(activeResult) : "",
        ...state.mapItems.filter((item) => item.kind === "endpoint").map(markerSvg),
        candidateItem ? markerSvg(candidateItem) : "",
        candidateItem ? labelSvg(candidateItem, 0) : "",
        legendSvg(MAP_WIDTH, MAP_HEIGHT)
      ].join("");

      resultMap.querySelectorAll(".map-marker").forEach((marker) => {
        marker.addEventListener("mouseenter", () => showMapTooltip(marker));
        marker.addEventListener("focus", () => showMapTooltip(marker));
        marker.addEventListener("mouseleave", hideMapTooltip);
        marker.addEventListener("blur", hideMapTooltip);
      });
    }

    function mapProjection(coordinates, width, height, padding) {
      const projected = coordinates.map((coordinate) => projectCoordinate(coordinate));
      const xs = projected.map((point) => point.x);
      const ys = projected.map((point) => point.y);
      const minX = Math.min(...xs);
      const maxX = Math.max(...xs);
      const minY = Math.min(...ys);
      const maxY = Math.max(...ys);
      const scale = Math.min(
        (width - padding * 2) / (maxX - minX),
        (height - padding * 2) / (maxY - minY)
      );
      const mapWidth = (maxX - minX) * scale;
      const mapHeight = (maxY - minY) * scale;
      return {
        minX,
        maxY,
        scale,
        offsetX: (width - mapWidth) / 2,
        offsetY: (height - mapHeight) / 2,
        width,
        height,
        padding
      };
    }

    function projectCoordinate(coordinate) {
      const meanLatitude = 1.35 * Math.PI / 180;
      return {
        x: coordinate.lng * Math.cos(meanLatitude),
        y: coordinate.lat
      };
    }

    function mapPoint(coordinate, projection) {
      const projected = projectCoordinate(coordinate);
      return {
        x: projection.offsetX + (projected.x - projection.minX) * projection.scale,
        y: projection.offsetY + (projection.maxY - projected.y) * projection.scale
      };
    }

    function svgDefs() {
      return `
        <defs>
          <linearGradient id="map-water-gradient" x1="0" x2="1" y1="0" y2="1">
            <stop offset="0" stop-color="#9fc5cb"></stop>
            <stop offset="0.55" stop-color="#c8dedb"></stop>
            <stop offset="1" stop-color="#f4dfad"></stop>
          </linearGradient>
          <filter id="land-shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="10" dy="12" stdDeviation="7" flood-color="#1b2628" flood-opacity="0.22"></feDropShadow>
          </filter>
          <marker id="arrow-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="2.4" markerHeight="2.4" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"></path>
          </marker>
        </defs>
      `;
    }

    function cloudSvg() {
      return Array.from({ length: 9 }, (_item, index) => {
        const x = MAP_WIDTH * (0.12 + index * 0.1);
        const radius = 24 + index * 4;
        return `<circle cx="${x}" cy="${MAP_HEIGHT * 0.18}" r="${radius}" fill="rgba(255, 253, 247, 0.24)"></circle>`;
      }).join("");
    }

    function singaporeOutlinePath(projection) {
      return SINGAPORE_OUTLINE.map((ring) => {
        const d = ring.map((coordinate, index) => {
          const point = mapPoint(coordinate, projection);
          return `${index === 0 ? "M" : "L"} ${point.x.toFixed(2)} ${point.y.toFixed(2)}`;
        }).join(" ");
        return `
          <path d="${d} Z" fill="rgba(255, 253, 247, 0.72)" filter="url(#land-shadow)"></path>
          <path d="${d} Z" fill="none" stroke="rgba(27, 38, 40, 0.28)" stroke-width="2" vector-effect="non-scaling-stroke"></path>
        `;
      }).join("");
    }

    function coordinateGridSvg(width, height, padding) {
      const lines = [];
      for (let index = 0; index <= 6; index += 1) {
        const x = padding + ((width - padding * 2) / 6) * index;
        const y = padding + ((height - padding * 2) / 6) * index;
        lines.push(`<line x1="${x}" y1="${padding}" x2="${x}" y2="${height - padding}"></line>`);
        lines.push(`<line x1="${padding}" y1="${y}" x2="${width - padding}" y2="${y}"></line>`);
      }
      return `<g stroke="rgba(27, 38, 40, 0.1)" stroke-width="1" vector-effect="non-scaling-stroke">${lines.join("")}</g>`;
    }

    function routeOverlaySvg(result) {
      const overlays = result.distances.flatMap((item, routeIndex) => {
        const displayRoute = item.origin.direction === "out" ? [...item.route].reverse() : item.route;
        return routeSegments(displayRoute, item.origin.direction).map((segment, segmentIndex) => {
          const color = lineColor(segment.line);
          const opacity = item.origin.direction === "out" ? 0.42 : 0.58;
          const dash = item.origin.direction === "out" ? ' stroke-dasharray="8 5"' : "";
          return `
            <path
              class="route-overlay"
              d="M ${segment.from.x.toFixed(2)} ${segment.from.y.toFixed(2)} L ${segment.to.x.toFixed(2)} ${segment.to.y.toFixed(2)}"
              stroke="${color}"
              opacity="${opacity}"
              marker-end="url(#arrow-head)"
              data-route-index="${routeIndex}"
              data-segment-index="${segmentIndex}"${dash}>
            </path>
          `;
        });
      });
      return `<g class="route-overlays">${overlays.join("")}</g>`;
    }

    function routeSegments(route, direction) {
      const segments = [];
      for (let index = 0; index < route.length - 1; index += 1) {
        const step = route[index];
        const nextStep = route[index + 1];
        const fromCoordinate = STATION_COORDINATES[step.stationId];
        const toCoordinate = STATION_COORDINATES[nextStep.stationId];
        if (!fromCoordinate || !toCoordinate) continue;
        segments.push({
          from: mapPoint(fromCoordinate, state.mapProjection),
          to: mapPoint(toCoordinate, state.mapProjection),
          line: routeLineForStep(step, nextStep, direction)
        });
      }
      return segments;
    }

    function routeLineForStep(step, nextStep, direction) {
      return direction === "out"
        ? step.line || nextStep.line || ""
        : nextStep.line || step.line || "";
    }

    function markerSvg(item) {
      const isBest = item.kind === "candidate" && item.rank === 1;
      const label = item.kind === "candidate" ? `#${item.rank} ${item.name}` : item.name;
      const rings = isBest
        ? `<circle cx="${item.x}" cy="${item.y}" r="${item.radius + 5}" fill="none" stroke="rgba(240, 180, 60, 0.75)" stroke-width="3" vector-effect="non-scaling-stroke"></circle>`
        : "";
      return `
        <g class="map-marker" tabindex="0" role="button" aria-label="${escapeAttribute(label)}" data-label="${escapeAttribute(label)}" data-detail="${escapeAttribute(item.detail)}">
          <title>${escapeHtml(label)} ${escapeHtml(item.detail)}</title>
          ${rings}
          ${stationMarkerSvg(item.x, item.y, item.radius, item.colors)}
          <circle class="marker-hit" cx="${item.x}" cy="${item.y}" r="${item.radius}" fill="none" stroke="#1b2628" stroke-width="${isBest ? 3 : 2}" vector-effect="non-scaling-stroke"></circle>
        </g>
      `;
    }

    function stationMarkerSvg(x, y, radius, colors) {
      const markerColors = colors.length ? colors : ["#d7dfdc"];
      if (markerColors.length === 1) {
        return `<circle cx="${x}" cy="${y}" r="${radius}" fill="${markerColors[0]}"></circle>`;
      }

      return markerColors.map((color, index) => {
        const start = -Math.PI / 2 + (Math.PI * 2 * index) / markerColors.length;
        const end = -Math.PI / 2 + (Math.PI * 2 * (index + 1)) / markerColors.length;
        return `<path d="${arcSlicePath(x, y, radius, start, end)}" fill="${color}"></path>`;
      }).join("");
    }

    function arcSlicePath(x, y, radius, start, end) {
      const startX = x + Math.cos(start) * radius;
      const startY = y + Math.sin(start) * radius;
      const endX = x + Math.cos(end) * radius;
      const endY = y + Math.sin(end) * radius;
      const largeArc = end - start > Math.PI ? 1 : 0;
      return [
        `M ${x.toFixed(2)} ${y.toFixed(2)}`,
        `L ${startX.toFixed(2)} ${startY.toFixed(2)}`,
        `A ${radius} ${radius} 0 ${largeArc} 1 ${endX.toFixed(2)} ${endY.toFixed(2)}`,
        "Z"
      ].join(" ");
    }

    function stationLineColors(codes) {
      const colors = [];
      for (const code of codes || []) {
        const color = lineColor(lineNameForCode(code));
        if (!colors.includes(color)) colors.push(color);
      }
      return colors;
    }

    function lineNameForCode(code) {
      const prefix = String(code).replace(/[0-9]+.*/, "");
      return {
        NS: "North South Line",
        EW: "East West Line",
        CG: "East West Line",
        NE: "North East Line",
        CC: "Circle Line",
        CE: "Circle Line",
        DT: "Downtown Line",
        TE: "Thomson-East Coast Line"
      }[prefix] || "";
    }

    function labelSvg(item, index) {
        const label = `#${item.rank} ${item.name}`;
        const labelX = Math.min(item.x + 13, MAP_WIDTH - label.length * 7 - 10);
        const labelY = Math.max(16, Math.min(item.y + (index % 2 ? 15 : -15), MAP_HEIGHT - 16));
        return `<text class="marker-label" x="${labelX}" y="${labelY}">${escapeHtml(label)}</text>`;
    }

    function legendSvg(width, height) {
      const items = [
        ["North South Line", "NSL"],
        ["East West Line", "EWL"],
        ["North East Line", "NEL"],
        ["Circle Line", "CCL"],
        ["Downtown Line", "DTL"],
        ["Thomson-East Coast Line", "TEL"]
      ];
      const x = 14;
      const y = height - 20;
      const legendItems = items.map(([lineName, label], index) => {
        const offset = index * 54;
        return `
          <circle cx="${x + offset + 5}" cy="${y}" r="5" fill="${lineColor(lineName)}" stroke="#1b2628" stroke-width="1.5" vector-effect="non-scaling-stroke"></circle>
          <text x="${x + offset + 14}" y="${y + 4}" fill="#1b2628" font-size="11" font-weight="800">${label}</text>
        `;
      }).join("");
      return `<g class="map-legend">${legendItems}</g>`;
    }

    function showMapTooltip(marker) {
      mapTooltip.innerHTML = `${escapeHtml(marker.dataset.label)}<span>${escapeHtml(marker.dataset.detail)}</span>`;
      mapTooltip.classList.add("is-visible");
      const markerRect = marker.getBoundingClientRect();
      const shellRect = resultMap.parentElement.getBoundingClientRect();
      const tooltipWidth = mapTooltip.offsetWidth || 180;
      const tooltipHeight = mapTooltip.offsetHeight || 54;
      const x = markerRect.left + markerRect.width / 2 - shellRect.left;
      const y = markerRect.top + markerRect.height / 2 - shellRect.top;
      const left = Math.min(Math.max(8, x + 12), shellRect.width - tooltipWidth - 8);
      const top = Math.min(Math.max(tooltipHeight / 2 + 8, y), shellRect.height - tooltipHeight / 2 - 8);
      mapTooltip.style.left = `${left}px`;
      mapTooltip.style.top = `${top}px`;
    }

    function hideMapTooltip() {
      mapTooltip.classList.remove("is-visible");
    }

    function routeTimeline(item, destination) {
      const displayRoute = item.origin.direction === "out" ? [...item.route].reverse() : item.route;
      const startName = item.origin.direction === "out" ? destination.name : item.origin.name;
      const endName = item.origin.direction === "out" ? item.origin.name : destination.name;
      return `
        <span class="route-title">
          <span>${escapeHtml(startName)} to ${escapeHtml(endName)}</span>
          <span>${item.hops} cost</span>
        </span>
        <span class="route-timeline">
          ${displayRoute.map((step, index) => {
            const station = state.graph.stations.get(step.stationId);
            const nextStep = displayRoute[index + 1];
            const segmentLine = step.line || nextStep?.line || "";
            const labelLine = index === 0 ? "Start" : lineShortName(segmentLine);
            return `
              <span class="route-step" style="--route-color: ${lineColor(segmentLine)}">
                <span class="route-dot"></span>
                <span class="route-stop">
                  <strong>${escapeHtml(station.name)}</strong>
                  <span>${escapeHtml(labelLine)}</span>
                </span>
              </span>
            `;
          }).join("")}
        </span>
      `;
    }

    function showRoutePopover(trigger) {
      routePopover.innerHTML = trigger.dataset.route || "";
      routePopover.classList.add("is-visible");
      routePopover.setAttribute("aria-hidden", "false");

      const triggerRect = trigger.getBoundingClientRect();
      const popoverRect = routePopover.getBoundingClientRect();
      const gap = 10;
      const viewportPadding = 12;
      const preferredLeft = triggerRect.left;
      const left = Math.max(
        viewportPadding,
        Math.min(preferredLeft, window.innerWidth - popoverRect.width - viewportPadding)
      );
      const above = triggerRect.top - popoverRect.height - gap;
      const below = triggerRect.bottom + gap;
      const top = above >= viewportPadding
        ? above
        : Math.min(below, window.innerHeight - popoverRect.height - viewportPadding);

      routePopover.style.left = `${left}px`;
      routePopover.style.top = `${Math.max(viewportPadding, top)}px`;
    }

    function hideRoutePopover() {
      routePopover.classList.remove("is-visible");
      routePopover.setAttribute("aria-hidden", "true");
    }

    function lineColor(line) {
      return LINE_COLORS[line] || "#d7dfdc";
    }

    function lineShortName(line) {
      return line
        .replace("North South Line", "NSL")
        .replace("East West Line", "EWL")
        .replace("North East Line", "NEL")
        .replace("Circle Line", "CCL")
        .replace("Downtown Line", "DTL")
        .replace("Thomson-East Coast Line", "TEL");
    }

    function showMessage(value) {
      message.textContent = value;
    }

    function clearMessage() {
      message.textContent = "";
    }

    function escapeHtml(value) {
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function escapeAttribute(value) {
      return escapeHtml(value).replaceAll("`", "&#096;");
    }
  </script>
</body>
</html>
"""
