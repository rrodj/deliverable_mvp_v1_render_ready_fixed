import React, { useEffect, useState } from 'react';
import { fetchAlerts, createTestAlert } from '../api';
import type { Alert } from '../types';

const AlertsPage: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setError(null);
    try {
      const data = await fetchAlerts();
      setAlerts(data);
    } catch (e: any) {
      setError(e?.response?.data?.error || 'Failed to load alerts');
    }
  };

  const create = async () => {
    try {
      await createTestAlert();
      await load();
    } catch (e: any) {
      setError(e?.response?.data?.error || 'Failed to create alert');
    }
  };

  useEffect(() => { load(); }, []);

  return (
    <div className="card">
      <h2>Alerts</h2>
      {error && <div className="alert error">{error}</div>}
      <button className="button" onClick={create}>Create Test Alert</button>
      <table style={{marginTop:12}}>
        <thead><tr><th>Time</th><th>Level</th><th>Type</th><th>Message</th></tr></thead>
        <tbody>
          {alerts.map(a => (
            <tr key={a.id}>
              <td><small className="mono">{a.timestamp}</small></td>
              <td>{a.level}</td>
              <td>{a.type}</td>
              <td>{a.message}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AlertsPage;
