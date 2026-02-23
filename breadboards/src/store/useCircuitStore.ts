import { create } from 'zustand';
import { CircuitSimulator } from '../simulator/Engine';
import type { ComponentType, Component as SimComponent } from '../simulator/Engine';

export interface BreadboardHole {
    id: string; // the electrical node, e.g., 'T+', 'T-', 'Top_1', 'Bot_30'
    position: [number, number, number]; // 3D coordinates
}

export interface PlacedComponent {
    id: string;
    type: ComponentType;
    holeA: BreadboardHole;
    holeB: BreadboardHole;
    value: number;
    frequency?: number;
}

interface CircuitState {
    simulator: CircuitSimulator;
    components: PlacedComponent[];

    placingType: ComponentType | null;
    placingValue: number;

    firstHole: BreadboardHole | null;

    voltages: Record<string, number>;
    currents: Record<string, number>;
    totalInductance: number | null;

    // UI selection
    selectedComponentId: string | null;
    setSelectedComponentId: (id: string | null) => void;

    setPlacingType: (type: ComponentType | null, value?: number) => void;
    setPlacingValue: (val: number) => void;
    clickHole: (hole: BreadboardHole) => void;
    removeComponent: (id: string) => void;
    stepSimulation: () => void;
}

const sim = new CircuitSimulator();

export const useCircuitStore = create<CircuitState>((set, get) => ({
    simulator: sim,
    components: [],

    placingType: null,
    placingValue: 1000,

    firstHole: null,

    voltages: {},
    currents: {},
    totalInductance: null,

    selectedComponentId: null,
    setSelectedComponentId: (id) => set({ selectedComponentId: id }),

    setPlacingType: (type, value) => {
        set({ placingType: type, firstHole: null, selectedComponentId: null });
        if (value !== undefined) {
            set({ placingValue: value });
        }
    },

    setPlacingValue: (val) => set({ placingValue: val }),

    clickHole: (hole) => {
        const { placingType, firstHole, placingValue, simulator, components } = get();

        if (!placingType) return; // not placing

        if (!firstHole) {
            set({ firstHole: hole });
        } else {
            // Create component
            if (firstHole.id === hole.id) {
                set({ firstHole: null }); // can't place in same hole
                return;
            }

            const newId = `${placingType}_${Date.now()}`;
            const newComp: PlacedComponent = {
                id: newId,
                type: placingType,
                holeA: firstHole,
                holeB: hole,
                value: placingValue,
                frequency: placingType === 'V_AC' ? 60 : undefined
            };

            const simComp: SimComponent = {
                id: newId,
                type: placingType,
                nodeA: firstHole.id,
                nodeB: hole.id,
                value: placingValue,
                frequency: newComp.frequency
            };

            simulator.addComponent(simComp);
            const ind = simulator.calculateEquivalentInductance();

            set({
                components: [...components, newComp],
                firstHole: null,
                totalInductance: ind
            });
        }
    },

    removeComponent: (id) => {
        const { simulator, components } = get();
        simulator.removeComponent(id);
        const ind = simulator.calculateEquivalentInductance();
        set({
            components: components.filter(c => c.id !== id),
            totalInductance: ind,
            selectedComponentId: get().selectedComponentId === id ? null : get().selectedComponentId
        });
    },

    stepSimulation: () => {
        const { simulator } = get();
        // To make it look fast and smooth
        // We can run multiple steps per frame if dt is small
        const numSteps = 10;
        let res = { voltages: {}, currents: {} };
        for (let i = 0; i < numSteps; i++) {
            res = simulator.stepTransient();
        }
        set({ voltages: res.voltages, currents: res.currents });
    }
}));
