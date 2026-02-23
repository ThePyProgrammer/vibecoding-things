import React, { useRef } from 'react';
import { useCircuitStore } from '../../store/useCircuitStore';
import * as THREE from 'three';
import { Text } from '@react-three/drei';

function ComponentModel({ comp, isSelected, onClick }: any) {
    const pA = new THREE.Vector3(...comp.holeA.position);
    const pB = new THREE.Vector3(...comp.holeB.position);
    const mid = pA.clone().lerp(pB, 0.5);
    mid.y += 1.5; // elevate component body

    const distance = pA.distanceTo(pB);

    // Calculate rotation to point from A to B
    const direction = pB.clone().sub(pA).normalize();
    const axis = new THREE.Vector3(0, 1, 0); // initial cylinder axis
    const quaternion = new THREE.Quaternion().setFromUnitVectors(axis, direction);
    const euler = new THREE.Euler().setFromQuaternion(quaternion);

    return (
        <group onClick={(e) => { e.stopPropagation(); onClick(); }}>
            {/* Leads */}
            <line>
                <bufferGeometry attach="geometry">
                    <bufferAttribute
                        attach="attributes-position"
                        count={2}
                        array={new Float32Array([...pA.toArray(), ...mid.toArray()])}
                        itemSize={3}
                    />
                </bufferGeometry>
                <lineBasicMaterial attach="material" color="#888" linewidth={2} />
            </line>
            <line>
                <bufferGeometry attach="geometry">
                    <bufferAttribute
                        attach="attributes-position"
                        count={2}
                        array={new Float32Array([...mid.toArray(), ...pB.toArray()])}
                        itemSize={3}
                    />
                </bufferGeometry>
                <lineBasicMaterial attach="material" color="#888" linewidth={2} />
            </line>

            {/* Component Body */}
            <group position={mid} rotation={euler}>
                {comp.type === 'R' && (
                    <mesh>
                        <cylinderGeometry args={[0.3, 0.3, distance * 0.4, 16]} />
                        <meshStandardMaterial color={isSelected ? "#00ff00" : "#d4b383"} />
                    </mesh>
                )}
                {comp.type === 'C' && (
                    <mesh>
                        <cylinderGeometry args={[0.5, 0.5, 0.2, 16]} />
                        <meshStandardMaterial color={isSelected ? "#00ff00" : "#e68a00"} />
                    </mesh>
                )}
                {comp.type === 'L' && (
                    <mesh>
                        <cylinderGeometry args={[0.4, 0.4, distance * 0.5, 16]} />
                        <meshStandardMaterial color={isSelected ? "#00ff00" : "#228B22"} wireframe={true} />
                    </mesh>
                )}
                {['V_DC', 'V_AC'].includes(comp.type) && (
                    <mesh>
                        <boxGeometry args={[distance * 0.6, 0.8, 0.8]} />
                        <meshStandardMaterial color={isSelected ? "#00ff00" : "#ff3333"} />
                    </mesh>
                )}

                {/* Value Tag */}
                <Text
                    position={[0, 0.6, 0]}
                    rotation={[0, 0, 0]} // Make text face upwards or lock rotation. It's inside rotating group, so it inherits.
                    fontSize={0.4}
                    color="white"
                    anchorX="center"
                    anchorY="middle"
                >
                    {comp.type === 'R' ? `${comp.value}Ω` :
                        comp.type === 'C' ? `${comp.value}F` :
                            comp.type === 'L' ? `${comp.value}H` :
                                `${comp.value}V`}
                </Text>
            </group>
        </group>
    );
}

export function CircuitComponents() {
    const components = useCircuitStore(st => st.components);
    const selectedComponentId = useCircuitStore(st => st.selectedComponentId);
    const setSelectedComponentId = useCircuitStore(st => st.setSelectedComponentId);

    return (
        <group>
            {components.map(c => (
                <ComponentModel
                    key={c.id}
                    comp={c}
                    isSelected={selectedComponentId === c.id}
                    onClick={() => setSelectedComponentId(c.id === selectedComponentId ? null : c.id)}
                />
            ))}
        </group>
    );
}
