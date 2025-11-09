import React, { useEffect, useState } from 'react';
import { fetchHealth, fetchWeekly } from '../api';
import RoiWidget from '../components/RoiWidget';
import type { WeeklyReport } from '../types';

const OverviewPage: React.FC = () => {
  const [health, setHealth] = useState<any>(null);
  const [report, setReport] = useState<WeeklyReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setError(null);
    try {
      const [h, r] = await Promise.all([fetchHealth(), fetchWeekly()]);
      setHealth(h); setReport(r);
    } catch (e: any) {
      setError(e?.response?.data?.error || 'Failed to load');
    }
  };

  useEffect(() => { load(); }, []);

  return (
    <>
      <RoiWidget />

      <div className="card">
        <h2>System Health</h2>
        {error && <div className="alert error">{error}</div>}
        {health ? (
          <div className="grid">
            <div className="card"><strong>Status:</strong> {health.status}</div>
            <div className="card"><strong>Version:</strong> {health.version}</div>
            <div className="card"><strong>Env:</strong> {health.env}</div>
          </div>
        ) : <div>Loading...</div>}
      </div>

      <div className="card">
        <h2>Weekly Snapshot</h2>
        {report ? (
          <div className="grid">
            <div className="card"><strong>Menu Items:</strong> {report.totals.menu_items}</div>
            <div className="card"><strong>Calibrations:</strong> {report.totals.calibrations}</div>
            <div className="card"><strong>Alerts:</strong> {report.totals.alerts}</div>
          </div>
        ) : <div>Loading...</div>}
        <button className="button" onClick={load} style={{marginTop:12}}>Refresh</button>
      </div>
    </>
  );
};

export default OverviewPage;
