import React, { useMemo } from 'react';
import { useCircuitStore } from '../../store/useCircuitStore';
import type { BreadboardHole } from '../../store/useCircuitStore';
import * as THREE from 'three';

export function Breadboard() {
    const clickHole = useCircuitStore(st => st.clickHole);
    const firstHole = useCircuitStore(st => st.firstHole);
    const placingType = useCircuitStore(st => st.placingType);

    const holes: BreadboardHole[] = useMemo(() => {
        const list: BreadboardHole[] = [];

        // Columns 1 to 30
        for (let col = 1; col <= 30; col++) {
            const x = col - 15.5; // centering around 0

            // Top +
            list.push({ id: `T+`, position: [x, 0, -4] });
            // Top -
            list.push({ id: `T-`, position: [x, 0, -3] });

            // Top Terminal (A-E)
            list.push({ id: `Top_${col}`, position: [x, 0, -1.5] });
            list.push({ id: `Top_${col}`, position: [x, 0, -1.0] });
            list.push({ id: `Top_${col}`, position: [x, 0, -0.5] });
            list.push({ id: `Top_${col}`, position: [x, 0, 0.0] });
            list.push({ id: `Top_${col}`, position: [x, 0, 0.5] });

            // Bottom Terminal (F-J)
            list.push({ id: `Bot_${col}`, position: [x, 0, 1.5] });
            list.push({ id: `Bot_${col}`, position: [x, 0, 2.0] });
            list.push({ id: `Bot_${col}`, position: [x, 0, 2.5] });
            list.push({ id: `Bot_${col}`, position: [x, 0, 3.0] });
            list.push({ id: `Bot_${col}`, position: [x, 0, 3.5] });

            // Bottom -
            list.push({ id: `B-`, position: [x, 0, 5] });
            // Bottom +
            list.push({ id: `B+`, position: [x, 0, 6] });
        }

        // Add unique internal IDs to rendering, since multiple holes share electrical IDs.
        // We will augment the objects locally for rendering.
        return list;
    }, []);

    return (
        <group>
            {/* Breadboard Base */}
            <mesh position={[0, -0.2, 1]} receiveShadow castShadow>
                <boxGeometry args={[34, 0.4, 14]} />
                <meshStandardMaterial color="#eeeeee" roughness={0.8} />
            </mesh>

            {/* Center gap marker */}
            <mesh position={[0, -0.19, 1]}>
                <boxGeometry args={[34, 0.41, 0.5]} />
                <meshStandardMaterial color="#cccccc" roughness={0.9} />
            </mesh>

            {/* Holes */}
            {holes.map((h, i) => {
                const isSelected = firstHole && firstHole.position[0] === h.position[0] && firstHole.position[2] === h.position[2];
                const color = isSelected ? "#00ff00" : (placingType ? "#444" : "#222");
                return (
                    <mesh
                        key={i}
                        position={new THREE.Vector3(...h.position)}
                        onClick={(e) => { e.stopPropagation(); clickHole(h); }}
                        onPointerOver={() => document.body.style.cursor = placingType ? 'pointer' : 'auto'}
                        onPointerOut={() => document.body.style.cursor = 'auto'}
                    >
                        <boxGeometry args={[0.6, 0.05, 0.6]} />
                        <meshStandardMaterial color={color} emissive={isSelected ? "#00aa00" : "#000000"} />
                    </mesh>
                );
            })}
        </group>
    );
}
