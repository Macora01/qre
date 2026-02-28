import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import "./App.css";
import LoginPage from "./components/LoginPage";
import AuthCallback from "./components/AuthCallback";
import Scanner from "./components/Scanner";
import ProtectedRoute from "./components/ProtectedRoute";

function AppRouter() {
  const location = useLocation();
  
  // CRITICAL: Check URL fragment synchronously during render (NOT in useEffect)
  // This prevents race conditions - we must process session_id BEFORE any auth checks
  if (location.hash?.includes('session_id=')) {
    return <AuthCallback />;
  }
  
  return (
    <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/scanner"
        element={
          <ProtectedRoute>
            <Scanner />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <AppRouter />
      </BrowserRouter>
    </div>
  );
}

export default App;
