import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function ProtectedRoute({ children }) {
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("qre_token");
    if (!token) { setIsAuthenticated(false); navigate("/login"); return; }

    fetch(`${API}/auth/me`, {
      headers: { "Authorization": `Bearer ${token}` }
    }).then(r => {
      if (r.ok) setIsAuthenticated(true);
      else { setIsAuthenticated(false); navigate("/login"); }
    }).catch(() => { setIsAuthenticated(false); navigate("/login"); });
  }, [navigate]);

  if (isAuthenticated === null) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <div className="loading-text">Verificando sesión...</div>
      </div>
    );
  }

  if (!isAuthenticated) return null;
  return children;
}

export default ProtectedRoute;
