import React, { useState } from 'react';
import { uploadMenuCsv } from '../api';

const InventoryPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onUpload = async () => {
    if (!file) { setError('Select a CSV file first'); return; }
    setError(null); setResult(null);
    try {
      const res = await uploadMenuCsv(file);
      setResult(res.items_ingested);
    } catch (e: any) {
      setError(e?.response?.data?.detail || e?.response?.data?.error || 'Upload failed');
    }
  };

  return (
    <div className="card">
      <h2>Inventory — Menus Upload</h2>
      <div className="row">
        <input className="input" type="file" accept=".csv,text/csv" onChange={(e)=>setFile(e.target.files?.[0] || null)} />
        <button className="button" onClick={onUpload}>Upload CSV</button>
      </div>
      <div style={{marginTop:12}}>
        {result !== null && <div className="alert success">Ingested items: {result}</div>}
        {error && <div className="alert error">{error}</div>}
      </div>
      <div style={{marginTop:12}}>
        <small className="mono">CSV headers: sku,name,price</small>
      </div>
    </div>
  );
};

export default InventoryPage;
