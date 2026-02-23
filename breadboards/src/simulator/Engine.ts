import * as math from 'mathjs';

export type ComponentType = 'R' | 'L' | 'C' | 'V_DC' | 'V_AC';

export interface Component {
    id: string;
    type: ComponentType;
    nodeA: string;
    nodeB: string;
    value: number;
    frequency?: number; // for V_AC
}

export class CircuitSimulator {
    components: Component[] = [];
    nodeMap: Map<string, number> = new Map();
    nodeNames: string[] = [];

    // Transient state
    time = 0;
    dt = 0.001; // 1ms
    states: Record<string, number> = {}; // Stores previous currents/voltages for C and L

    constructor() { }

    addComponent(comp: Component) {
        this.components.push(comp);
    }

    removeComponent(id: string) {
        this.components = this.components.filter(c => c.id !== id);
    }

    clear() {
        this.components = [];
        this.time = 0;
        this.states = {};
    }

    _buildNodeMap() {
        this.nodeMap.clear();
        this.nodeNames = [];
        let idx = 1; // 0 is reserved for ground

        const addNode = (n: string) => {
            if (n === 'gnd' && !this.nodeMap.has('gnd')) {
                this.nodeMap.set('gnd', 0);
                this.nodeNames[0] = 'gnd';
                return;
            }
            if (!this.nodeMap.has(n)) {
                this.nodeMap.set(n, idx);
                this.nodeNames[idx] = n;
                idx++;
            }
        };

        // If 'gnd' isn't explicitly defined, we pick the first node as ground (node 0)
        let hasGnd = this.components.some(c => c.nodeA === 'gnd' || c.nodeB === 'gnd');

        for (const c of this.components) {
            if (!hasGnd) {
                this.nodeMap.set(c.nodeA, 0);
                this.nodeNames[0] = c.nodeA;
                hasGnd = true;
            } else {
                addNode(c.nodeA);
            }
            addNode(c.nodeB);
        }
    }

    // Returns { nodeVoltages, branchCurrents }
    stepTransient(): { voltages: Record<string, number>, currents: Record<string, number> } {
        this._buildNodeMap();
        const N = this.nodeNames.length - 1; // number of non-ground nodes
        if (N < 0) return { voltages: {}, currents: {} };

        // Find voltage sources to allocate branch current variables
        const vSources = this.components.filter(c => c.type === 'V_DC' || c.type === 'V_AC');
        const M = vSources.length;

        const size = N + M;
        if (size === 0) return { voltages: {}, currents: {} };

        const G = math.zeros(size, size) as math.Matrix;
        const b = math.zeros(size, 1) as math.Matrix;

        const addG = (i: number, j: number, val: number) => {
            if (i > 0 && j > 0) G.set([i - 1, j - 1], G.get([i - 1, j - 1]) + val);
        };
        const addB = (i: number, val: number) => {
            if (i > 0) b.set([i - 1, 0], b.get([i - 1, 0]) + val);
        };

        const curTime = this.time;

        vSources.forEach((vs, idx) => {
            const iA = this.nodeMap.get(vs.nodeA)!;
            const iB = this.nodeMap.get(vs.nodeB)!;
            const mIdx = N + idx;

            if (iA > 0) { G.set([iA - 1, mIdx], 1); G.set([mIdx, iA - 1], 1); }
            if (iB > 0) { G.set([iB - 1, mIdx], -1); G.set([mIdx, iB - 1], -1); }

            let v = vs.value;
            if (vs.type === 'V_AC') {
                const freq = vs.frequency || 60;
                v = vs.value * Math.sin(2 * Math.PI * freq * curTime);
            }
            b.set([mIdx, 0], v);
        });

        for (const c of this.components) {
            const iA = this.nodeMap.get(c.nodeA)!;
            const iB = this.nodeMap.get(c.nodeB)!;

            if (c.type === 'R') {
                const g = 1 / Math.max(c.value, 1e-6);
                addG(iA, iA, g); addG(iB, iB, g);
                addG(iA, iB, -g); addG(iB, iA, -g);
            } else if (c.type === 'C') {
                const g = c.value / this.dt;
                addG(iA, iA, g); addG(iB, iB, g);
                addG(iA, iB, -g); addG(iB, iA, -g);

                let vPrev = this.states[`${c.id}_v`] || 0;
                let iEq = (c.value * vPrev) / this.dt;
                addB(iA, iEq);
                addB(iB, -iEq);
            } else if (c.type === 'L') {
                const g = this.dt / c.value;
                addG(iA, iA, g); addG(iB, iB, g);
                addG(iA, iB, -g); addG(iB, iA, -g);

                let iPrev = this.states[`${c.id}_i`] || 0;
                addB(iA, -iPrev);
                addB(iB, iPrev);
            }
        }

        let x: any;
        try {
            x = math.lusolve(G, b) as math.Matrix;
        } catch (e) {
            // Singular matrix (e.g. floating nodes)
            x = math.zeros(size, 1);
        }

        const voltages: Record<string, number> = { 'gnd': 0 };
        for (let i = 1; i <= N; i++) {
            const v = x.get([i - 1, 0]);
            voltages[this.nodeNames[i]] = isNaN(v) ? 0 : v;
        }
        if (this.nodeNames[0]) voltages[this.nodeNames[0]] = 0;

        const currents: Record<string, number> = {};

        // Update states and calculate currents
        vSources.forEach((vs, idx) => {
            const iCur = x.get([N + idx, 0]);
            currents[vs.id] = isNaN(iCur) ? 0 : iCur;
        });

        for (const c of this.components) {
            const vA = voltages[c.nodeA] || 0;
            const vB = voltages[c.nodeB] || 0;
            const vDiff = vA - vB;

            if (c.type === 'R') {
                currents[c.id] = vDiff / Math.max(c.value, 1e-6);
            } else if (c.type === 'C') {
                this.states[`${c.id}_v`] = vDiff;
                currents[c.id] = c.value * (vDiff - (this.states[`${c.id}_v_prev`] || 0)) / this.dt;
                this.states[`${c.id}_v_prev`] = vDiff;
            } else if (c.type === 'L') {
                const iNew = (this.states[`${c.id}_i`] || 0) + (this.dt / c.value) * vDiff;
                this.states[`${c.id}_i`] = iNew;
                currents[c.id] = iNew;
            }
        }

        this.time += this.dt;

        return { voltages, currents };
    }

    // Calculate equivalent inductance seen from the first voltage source at a given frequency
    calculateEquivalentInductance(): number | null {
        const vSources = this.components.filter(c => c.type === 'V_DC' || c.type === 'V_AC');
        if (vSources.length === 0) return null;

        const vs = vSources[0]; // Measure from the first source
        const omega = 1000; // rad/s for testing AC impedance

        this._buildNodeMap();
        const N = this.nodeNames.length - 1;
        const M = vSources.length;
        if (N < 0) return null;
        const size = N + M;

        // Complex Matrix
        const G = math.zeros(size, size) as any;
        const b = math.zeros(size, 1) as any;

        const addG = (i: number, j: number, val: math.Complex) => { // mathjs handles complex in matrices
            if (i > 0 && j > 0) {
                const prev = G.get([i - 1, j - 1]);
                G.set([i - 1, j - 1], math.add(prev, val));
            }
        };

        vSources.forEach((src, idx) => {
            const iA = this.nodeMap.get(src.nodeA)!;
            const iB = this.nodeMap.get(src.nodeB)!;
            const mIdx = N + idx;

            if (iA > 0) { G.set([iA - 1, mIdx], 1); G.set([mIdx, iA - 1], 1); }
            if (iB > 0) { G.set([iB - 1, mIdx], -1); G.set([mIdx, iB - 1], -1); }

            if (src.id === vs.id) b.set([mIdx, 0], math.complex(1, 0)); // Test 1V source
            else b.set([mIdx, 0], 0);
        });

        for (const c of this.components) {
            const iA = this.nodeMap.get(c.nodeA)!;
            const iB = this.nodeMap.get(c.nodeB)!;
            let y: math.Complex;

            if (c.type === 'R') {
                y = math.complex(1 / Math.max(c.value, 1e-6), 0);
            } else if (c.type === 'C') {
                y = math.complex(0, omega * c.value);
            } else if (c.type === 'L') {
                y = math.complex(0, -1 / (omega * c.value));
            } else continue;

            addG(iA, iA, y); addG(iB, iB, y);
            addG(iA, iB, math.multiply(-1, y) as math.Complex);
            addG(iB, iA, math.multiply(-1, y) as math.Complex);
        }

        let x: any;
        try {
            x = math.lusolve(G, b);
        } catch (e) {
            return null; // unable to solve
        }

        // the current through vs is x[N]
        // Z = V / I = 1 / I
        const I = x.get([N, 0]);
        if (!I || (I.re === 0 && I.im === 0)) return null;

        const Z = math.divide(math.complex(1, 0), I) as math.Complex;

        // Z = R + jX => X = omega * L => L = X / omega
        // We expect Z.im > 0 for inductive, Z.im < 0 for capacitive
        const L = Z.im / omega;
        return L;
    }
}
