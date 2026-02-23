import React from 'react';
import { useCircuitStore } from '../../store/useCircuitStore';
import type { ComponentType } from '../../simulator/Engine';
import { Zap, Activity, Grid } from 'lucide-react';

const TOOLS: { type: ComponentType, label: string, defaultVal: number }[] = [
    { type: 'R', label: 'Resistor', defaultVal: 100 },
    { type: 'C', label: 'Capacitor', defaultVal: 0.0001 },
    { type: 'L', label: 'Inductor', defaultVal: 0.01 },
    { type: 'V_DC', label: 'DC Voltage', defaultVal: 5 },
    { type: 'V_AC', label: 'AC Source', defaultVal: 10 },
];

export function Overlay() {
    const {
        placingType, placingValue, setPlacingType, setPlacingValue,
        firstHole, totalInductance,
        selectedComponentId, components, currents, voltages, removeComponent
    } = useCircuitStore();

    const selectedComp = components.find(c => c.id === selectedComponentId);
    const currentVal = selectedComponentId ? (currents[selectedComponentId] || 0) : 0;

    // Format current
    const formatCurrent = (val: number) => {
        const abs = Math.abs(val);
        if (abs < 1e-6) return (val * 1e9).toFixed(2) + ' nA';
        if (abs < 1e-3) return (val * 1e6).toFixed(2) + ' µA';
        if (abs < 1) return (val * 1e3).toFixed(2) + ' mA';
        return val.toFixed(2) + ' A';
    };

    return (
        <div style={{ position: 'absolute', top: 0, left: 0, width: '100vw', height: '100vh', pointerEvents: 'none', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: '20px' }}>
            {/* Top Bar: Live Stats */}
            <div className="glass-panel" style={{ alignSelf: 'center', padding: '12px 24px', borderRadius: '12px', display: 'flex', gap: '20px', alignItems: 'center', pointerEvents: 'auto' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Activity color="#4ADE80" />
                    <span style={{ fontSize: '18px', fontWeight: 600 }}>Total Inductance:</span>
                    <span style={{ fontSize: '20px', color: '#4ADE80', fontWeight: 'bold' }}>
                        {totalInductance !== null ? (totalInductance < 0 ? 'Capacitive' : `${(totalInductance * 1000).toFixed(2)} mH`) : 'N/A'}
                    </span>
                </div>
                <div style={{ padding: '0 10px', color: '#888' }}>|</div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Grid color="#60A5FA" />
                    <span>Components:</span>
                    <span style={{ fontWeight: 'bold' }}>{components.length}</span>
                </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', flex: 1, marginTop: '20px' }}>
                {/* Left Sidebar: Tools */}
                <div className="glass-panel" style={{ width: '250px', padding: '20px', borderRadius: '16px', display: 'flex', flexDirection: 'column', gap: '15px', pointerEvents: 'auto' }}>
                    <h3 style={{ margin: 0, fontSize: '16px', color: '#94A3B8', textTransform: 'uppercase', letterSpacing: '1px' }}>Components</h3>

                    {TOOLS.map(t => (
                        <button
                            key={t.type}
                            onClick={() => setPlacingType(placingType === t.type ? null : t.type, t.defaultVal)}
                            style={{
                                background: placingType === t.type ? 'rgba(59, 130, 246, 0.4)' : 'rgba(255, 255, 255, 0.05)',
                                border: `1px solid ${placingType === t.type ? '#3B82F6' : 'rgba(255,255,255,0.1)'}`,
                                padding: '12px', borderRadius: '8px', color: 'white', cursor: 'pointer',
                                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                                transition: 'all 0.2s'
                            }}
                        >
                            {t.label}
                            {placingType === t.type && <Zap size={16} color="#60A5FA" />}
                        </button>
                    ))}

                    {placingType && (
                        <div style={{ marginTop: '20px', padding: '15px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
                            <label style={{ display: 'block', marginBottom: '8px', fontSize: '14px', color: '#cbd5e1' }}>
                                Value ({placingType === 'R' ? 'Ω' : placingType === 'L' ? 'H' : placingType === 'C' ? 'F' : 'V'})
                            </label>
                            <input
                                type="number"
                                value={placingValue}
                                onChange={e => setPlacingValue(parseFloat(e.target.value) || 0)}
                                step="any"
                                style={{ width: '100%', padding: '8px', background: 'rgba(255,255,255,0.1)', border: '1px solid rgba(255,255,255,0.2)', color: 'white', borderRadius: '4px' }}
                            />

                            <div style={{ marginTop: '15px', fontSize: '13px', color: '#94A3B8', textAlign: 'center' }}>
                                {firstHole ? "Click 2nd hole to place" : "Click 1st hole on board"}
                            </div>
                        </div>
                    )}
                </div>

                {/* Right Sidebar: Selected Info */}
                <div style={{ width: '250px', display: 'flex', flexDirection: 'column', gap: '20px', pointerEvents: 'auto' }}>
                    {selectedComp && (
                        <div className="glass-panel" style={{ padding: '20px', borderRadius: '16px' }}>
                            <h3 style={{ margin: '0 0 15px 0', color: '#FCD34D' }}>Component Details</h3>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '14px' }}>
                                <div><strong>Type:</strong> {selectedComp.type}</div>
                                <div><strong>Value:</strong> {selectedComp.value} {selectedComp.type === 'R' ? 'Ω' : selectedComp.type === 'L' ? 'H' : selectedComp.type === 'C' ? 'F' : 'V'}</div>
                                <div><strong>From:</strong> {selectedComp.holeA.id} <br /> <strong>To:</strong> {selectedComp.holeB.id}</div>

                                <div style={{ marginTop: '15px', padding: '10px', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: '8px' }}>
                                    <strong style={{ color: '#4ADE80' }}>Live Current:</strong><br />
                                    <span style={{ fontSize: '18px', fontFamily: 'monospace' }}>{formatCurrent(currentVal)}</span>
                                </div>

                                <button
                                    onClick={() => removeComponent(selectedComp.id)}
                                    style={{ marginTop: '20px', background: '#EF4444', color: 'white', border: 'none', padding: '10px', borderRadius: '8px', cursor: 'pointer' }}
                                >
                                    Delete Component
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
