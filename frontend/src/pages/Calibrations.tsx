import React, { useEffect, useState } from 'react';
import { fetchCalibrations, createCalibration } from '../api';
import type { Calibration } from '../types';

const CalibrationsPage: React.FC = () => {
  const [items, setItems] = useState<Calibration[]>([]);
  const [deviceId, setDeviceId] = useState('scale-1');
  const [offset, setOffset] = useState('-0.30');
  const [note, setNote] = useState('initial');
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setError(null);
    try {
      const data = await fetchCalibrations();
      setItems(data);
    } catch (e: any) {
      setError(e?.response?.data?.error || 'Failed to load');
    }
  };

  const create = async () => {
    setError(null);
    try {
      await createCalibration({ device_id: deviceId, offset: Number(offset), note });
      await load();
    } catch (e: any) {
      setError(e?.response?.data?.error || 'Failed to create');
    }
  };

  useEffect(() => { load(); }, []);

  return (
    <div className="card">
      <h2>Calibrations</h2>
      {error && <div className="alert error">{error}</div>}
      <div className="row" style={{marginBottom:12}}>
        <input className="input" value={deviceId} onChange={(e)=>setDeviceId(e.target.value)} placeholder="device_id" />
        <input className="input" value={offset} onChange={(e)=>setOffset(e.target.value)} placeholder="offset e.g. -0.30" />
        <input className="input" value={note} onChange={(e)=>setNote(e.target.value)} placeholder="note" />
        <button className="button" onClick={create}>Create</button>
        <button className="button" onClick={load}>Refresh</button>
      </div>
      <table>
        <thead><tr><th>Time</th><th>Device</th><th>Offset</th><th>Note</th><th>ID</th></tr></thead>
        <tbody>
          {items.map(c => (
            <tr key={c.id}>
              <td><small className="mono">{c.timestamp}</small></td>
              <td>{c.device_id}</td>
              <td>{c.offset}</td>
              <td>{c.note}</td>
              <td><small className="mono">{c.id}</small></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CalibrationsPage;
