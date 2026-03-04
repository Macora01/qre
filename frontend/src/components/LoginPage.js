import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    // Load saved email
    const saved = localStorage.getItem("qre_email");
    if (saved) setEmail(saved);

    // Check if already authenticated
    const checkAuth = async () => {
      try {
        const response = await fetch(`${API}/auth/me`, { credentials: "include" });
        if (response.ok) {
          navigate("/scanner");
          return;
        }
      } catch (e) { /* not authenticated */ }
      setChecking(false);
    };
    checkAuth();
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const trimmed = email.trim().toLowerCase();
    if (!trimmed) {
      setError("Ingresa un correo electrónico");
      return;
    }

    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(trimmed)) {
      setError("Formato de correo inválido");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email: trimmed }),
      });

      if (response.ok) {
        const userData = await response.json();
        localStorage.setItem("qre_email", trimmed);
        navigate("/scanner", { state: { user: userData }, replace: true });
      } else {
        const data = await response.json();
        setError(data.detail || "Error al iniciar sesión");
      }
    } catch (err) {
      setError("Error de conexión. Intenta de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  if (checking) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <div className="loading-text">Verificando sesión...</div>
      </div>
    );
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h1 className="login-title" data-testid="login-title">Escáner QR</h1>
        <p className="login-subtitle">
          Ingresa tu correo para comenzar a escanear
        </p>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            className="login-input"
            placeholder="tu@correo.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
            autoFocus
            data-testid="email-input"
          />
          {error && (
            <div className="login-error" data-testid="login-error">{error}</div>
          )}
          <button
            type="submit"
            className="login-button"
            disabled={loading}
            data-testid="login-button"
          >
            {loading ? "Ingresando..." : "Entrar"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
