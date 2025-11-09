import React from 'react';
import { NavLink, Route, Routes, Navigate, useLocation } from 'react-router-dom';
import LoginPage from './pages/Login';
import OverviewPage from './pages/Overview';
import AlertsPage from './pages/Alerts';
import InventoryPage from './pages/Inventory';
import CalibrationsPage from './pages/Calibrations';
import TrialKitsPage from './pages/TrialKits';
import SettingsPage from './pages/Settings';
import ProtectedRoute from './components/ProtectedRoute';

const Header: React.FC = () => {
  const location = useLocation();
  const authed = !!localStorage.getItem('token');
  return (
    <header className="header">
      <div className="brand">Inventory Guardian</div>
      <nav className="nav">
        {authed ? (
          <>
            <NavLink className={({isActive}) => isActive ? 'active' : ''} to="/overview">Overview</NavLink>
            <NavLink className={({isActive}) => isActive ? 'active' : ''} to="/alerts">Alerts</NavLink>
            <NavLink className={({isActive}) => isActive ? 'active' : ''} to="/inventory">Inventory</NavLink>
            <NavLink className={({isActive}) => isActive ? 'active' : ''} to="/calibrations">Calibrations</NavLink>
            <NavLink className={({isActive}) => isActive ? 'active' : ''} to="/trial-kits">Trial Kits</NavLink>
            <NavLink className={({isActive}) => isActive ? 'active' : ''} to="/settings">Settings</NavLink>
          </>
        ) : (
          <NavLink className={({isActive}) => isActive ? 'active' : ''} to="/login">Login</NavLink>
        )}
      </nav>
    </header>
  );
};

const App: React.FC = () => {
  const authed = !!localStorage.getItem('token');
  return (
    <>
      <Header />
      <div className="container">
        <Routes>
          <Route path="/login" element={authed ? <Navigate to="/overview" replace /> : <LoginPage />} />
          <Route path="/" element={<Navigate to={authed ? "/overview" : "/login"} replace />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/overview" element={<OverviewPage />} />
            <Route path="/alerts" element={<AlertsPage />} />
            <Route path="/inventory" element={<InventoryPage />} />
            <Route path="/calibrations" element={<CalibrationsPage />} />
            <Route path="/trial-kits" element={<TrialKitsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>
          <Route path="*" element={<div className="card">Not Found</div>} />
        </Routes>
      </div>
      <footer className="footer"><small className="mono">MVP • build scaffold</small></footer>
    </>
  );
};

export default App;
