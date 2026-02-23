import React from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Environment, ContactShadows, Sky } from '@react-three/drei';
import { Breadboard } from './components/3d/Breadboard';
import { CircuitComponents } from './components/3d/CircuitComponents';
import { Overlay } from './components/ui/Overlay';
import { useCircuitStore } from './store/useCircuitStore';

function SimulationRunner() {
  const stepSimulation = useCircuitStore(st => st.stepSimulation);

  useFrame(() => {
    // Run simulation every frame
    stepSimulation();
  });

  return null;
}

function App() {
  return (
    <>
      <Canvas
        camera={{ position: [0, 15, 15], fov: 45 }}
        style={{ background: '#0f172a' }} // Dark background matching glassmorphism 
      >
        <color attach="background" args={['#0f172a']} />
        <ambientLight intensity={0.4} />
        <directionalLight position={[10, 20, 10]} intensity={1} castShadow />
        <directionalLight position={[-10, 20, -10]} intensity={0.5} />

        {/* Nice environment map for realistic lighting and reflections */}
        <Environment preset="city" />

        <SimulationRunner />

        <group position={[0, -2, 0]}>
          <Breadboard />
          <CircuitComponents />

          <ContactShadows position={[0, -0.4, 0]} opacity={0.4} scale={40} blur={2} far={4} />
        </group>

        <OrbitControls
          makeDefault
          minPolarAngle={0}
          maxPolarAngle={Math.PI / 2.1}
          maxDistance={50}
          minDistance={10}
        />
      </Canvas>
      <Overlay />
    </>
  );
}

export default App;
