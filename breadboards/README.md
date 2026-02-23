# 3D Breadboard Simulator 🔌

## About The Project
A smart and impressive 3D interactive breadboard simulator designed to accurately model real electronic circuits. This application empowers users to build, visualize, and simulate circuits in a fully interactive 3D browser environment.

It provides an intuitive interface for placing components—such as DC/AC power sources, resistors, capacitors, and inductors—onto a virtual breadboard exactly as one would in real life. Behind the scenes, the simulator calculates electrical properties and visualizes live metrics, such as total inductance, while allowing users to click on specific points to inspect current flow and voltage.

## Technology Stack
- **Framework**: React 19, TypeScript
- **3D Rendering**: Three.js, React Three Fiber (`@react-three/fiber`), `@react-three/drei`
- **State Management**: Zustand
- **Math/Simulation**: `mathjs` for complex circuit calculations (Nodal Analysis, etc.)
- **Icons/UI Tools**: `lucide-react`
- **Build Tool**: Vite

## Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) (v18 or higher recommended)
- npm (comes with Node.js)

### Installation & Running Locally

1. **Install dependencies**:
   ```bash
   npm install
   ```
2. **Start the development server**:
   ```bash
   npm run dev
   ```
3. **Open the App**:
   Navigate your browser to the local URL provided by Vite (usually `http://localhost:5173`).

### Building for Production
To generate a production-ready bundle:
```bash
npm run build
```
To preview that build locally:
```bash
npm run preview
```

---

## 🤖 Future Roadmap & AI Agent Reference

*This section provides a clear operational roadmap and guiding vision for any AI agent continuing the development of this simulator.*

### End Vision
The ultimate goal is to build an interactive, physically-accurate, real-time 3D circuit simulation tool that acts as a true digital twin of a hardware lab. The experience must be **visually stunning** (boss-impressive UX/UI) and mathematically correct, solving complex circuit matrices for both DC and AC domains.

### Development Roadmap

#### Phase 1: 3D Interactions & Core Board Modeling
- [ ] **Breadboard Interaction**: Ensure the breadboard holes have correct snapping and hit-testing logic for component placement.
- [ ] **Internal Routing**: Map out the internal connections of the breadboard (power rails horizontally, terminal strips vertically).
- [ ] **3D Models**: Add realistic (or stylized high-quality) 3D representations for Resistors, Capacitors, Inductors, Wires, and Power Sources.

#### Phase 2: The Circuit Simulation Engine
- [ ] **Netlist Generation**: Write logic to dynamically traverse the 3D components on the breadboard and compile a standard netlist.
- [ ] **Mathematical Modeling**: Implement Modified Nodal Analysis (MNA) using `mathjs` to solve for voltages at every node and current through every connected branch.
- [ ] **AC/DC Support**: Handle steady-state DC as well as AC phasor analysis (vital for capacitors and inductors).
- [ ] **Aggregated Metrics**: Implement the requested "live total inductance" (and capacitance/resistance) display for the active circuit view.

#### Phase 3: Visualizing Physics & Polishing UI
- [ ] **Interactive Probing**: Enable a feature where clicking on any wire/node/component displays a rich pop-up detailing the current flow (Amps) and potential (Volts).
- [ ] **Current Visualization**: Implement subtle micro-animations (e.g., animated particles or shaders on wires) that represent the direction and magnitude of current flow.
- [ ] **UI Presentation**: Add an "Oscilloscope" or "Multimeter" overlay using glassmorphism styling and modern typography. Avoid generic visual presentation; it needs to look premium.

### Agent Implementation Guidelines
1. **Performance First**: The 3D render loop must maintain 60FPS. Lean on Zustand for state, preventing unnecessary React re-renders. For many identical components, consider using Three.js `InstancedMesh`.
2. **Separation of Concerns**: Keep the visual/React-Tree layer completely decoupled from the mathematical circuit solver.
3. **Aesthetic Requirements**: Always optimize for "wow factor". Use deliberate color palettes, smooth camera transitions (via `drei` CameraControls), and rich lighting models (environment maps, soft shadows).
