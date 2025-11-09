import React, { useEffect, useState } from 'react';
import { fetchRoiSummary } from '../api';

type RoiSummary = {
  month: string;
  total_protected_usd: number;
  components: {
    dead_stock?: { usd: number };
    stockouts?: { usd: number };
    promo_bleed?: { usd: number };
    alerts?: { usd: number };
  };
};

const currency = (n: number | undefined) => (typeof n === 'number' ? n.toLocaleString(undefined, { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }) : '--');

const RoiWidget: React.FC = () => {
  const [data, setData] = useState<RoiSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true); setError(null);
    try {
      const res = await fetchRoiSummary();
      setData(res);
    } catch (e: any) {
      setError(e?.response?.data?.error || 'Failed to load ROI');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  return (
    <div className="card">
      <h2>ROI Protection</h2>
      {error && <div className="alert error">{error}</div>}
      {loading && <div>Loading...</div>}
      {!loading && data && (
        <>
          <div style={{fontSize: 28, fontWeight: 700, marginBottom: 8}}>
            This month you protected {currency(data.total_protected_usd)}
          </div>
          <div className="row">
            <div className="card"><strong>Dead stock</strong><div>{currency(data.components.dead_stock?.usd)}</div></div>
            <div className="card"><strong>Stockouts</strong><div>{currency(data.components.stockouts?.usd)}</div></div>
            <div className="card"><strong>Promo bleed</strong><div>{currency(data.components.promo_bleed?.usd)}</div></div>
            <div className="card"><strong>Alerts mix</strong><div>{currency(data.components.alerts?.usd)}</div></div>
          </div>
          <button className="button" onClick={load} style={{marginTop: 12}}>Refresh</button>
        </>
      )}
    </div>
  );
};

export default RoiWidget;
