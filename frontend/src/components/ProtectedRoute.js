import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function ProtectedRoute({ children }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [isAuthenticated, setIsAuthenticated] = useState(
    location.state?.user ? true : null
  );

  useEffect(() => {
    if (location.state?.user) {
      setIsAuthenticated(true);
      return;
    }

    const checkAuth = async () => {
      try {
        const response = await fetch(`${API}/auth/me`, { credentials: "include" });
        if (!response.ok) throw new Error("Not authenticated");
        setIsAuthenticated(true);
      } catch (error) {
        setIsAuthenticated(false);
        navigate("/login");
      }
    };

    checkAuth();
  }, [navigate, location.state]);

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
