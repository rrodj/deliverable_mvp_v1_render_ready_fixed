import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { login } from '../api';

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('demo');
  const [password, setPassword] = useState('demo');
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const location = useLocation() as any;
  const from = location.state?.from?.pathname || '/overview';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await login(username, password);
      localStorage.setItem('token', res.access_token);
      navigate(from, { replace: true });
    } catch (err: any) {
      setError(err?.response?.data?.error || 'Login failed');
    }
  };

  return (
    <div className="card" style={{maxWidth: 420, margin: "40px auto"}}>
      <h2>Login</h2>
      <p className="small muted">Use any credentials in MVP; a demo token will be returned.</p>
      {error && <div className="alert error">{error}</div>}
      <form onSubmit={handleSubmit} className="row">
        <input className="input" value={username} onChange={(e)=>setUsername(e.target.value)} placeholder="Username" />
        <input className="input" type="password" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="Password" />
        <button className="button" type="submit">Sign in</button>
      </form>
      <div style={{marginTop:12}}><small className="mono">API: {import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}</small></div>
    </div>
  );
};

export default LoginPage;
