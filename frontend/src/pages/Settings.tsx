import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchBillingPrices, fetchBillingStatus, fetchBillingPortal } from '../api';

const SettingsPage: React.FC = () => {
  const navigate = useNavigate();
  const logout = () => { localStorage.removeItem('token'); navigate('/login', { replace: true }); };

  const [prices, setPrices] = useState<any>(null);
  const [billing, setBilling] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setError(null);
    try {
      const [p, s] = await Promise.all([fetchBillingPrices(), fetchBillingStatus()]);
      setPrices(p); setBilling(s);
    } catch (e: any) {
      setError(e?.response?.data?.error || 'Failed to load billing');
    }
  };

  useEffect(()=>{ load(); }, []);

  const openPortal = async () => {
    try {
      const p = await fetchBillingPortal();
      window.open(p.portal_url, '_blank');
    } catch (e: any) {
      setError(e?.response?.data?.error || 'Portal unavailable');
    }
  };

  const plan = billing?.state?.plan || 'unconfigured';

  return (
    <div className="card">
      <h2>Settings</h2>
      {error && <div className="alert error">{error}</div>}
      <div className="grid">
        <div className="card">
          <strong>API Base URL</strong>
          <div><small className="mono">{import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}</small></div>
        </div>
        <div className="card">
          <strong>Session</strong>
          <div className="row" style={{marginTop:8}}>
            <button className="button" onClick={logout}>Logout</button>
          </div>
        </div>
        <div className="card">
          <strong>Billing</strong>
          <div>Plan: <b>{plan}</b></div>
          <div style={{marginTop:8}} className="row">
            <button className="button" onClick={openPortal}>Open Billing Portal</button>
            <button className="button" onClick={load}>Refresh</button>
          </div>
          {prices && (
            <div style={{marginTop:8}}>
              <small className="mono">Starter: {prices.plans?.starter?.price_id || '(unset)'} | Pro: {prices.plans?.pro?.price_id || '(unset)'} | Enterprise: {prices.plans?.enterprise?.price_id || '(unset)'}</small>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
