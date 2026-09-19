import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/");
  }

  return (
    <header className="sticky top-0 z-10 border-b border-brand-blue/60 bg-sky-cream/80 backdrop-blur">
      <nav className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
        <Link to="/" className="text-lg font-semibold text-brand-slate">
          ✨ Astro<span className="text-brand-blue-deep">AI</span>
        </Link>
        <div className="flex items-center gap-4 text-sm font-medium">
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="text-brand-slate/80 hover:text-brand-slate">
                My Kundli
              </Link>
              <Link to="/clients" className="text-brand-slate/80 hover:text-brand-slate">
                My Clients
              </Link>
              <button
                onClick={handleLogout}
                className="rounded-full bg-brand-pink px-4 py-2 text-brand-slate shadow-sm transition hover:shadow-md"
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-brand-slate/80 hover:text-brand-slate">
                Log in
              </Link>
              <Link
                to="/signup"
                className="rounded-full bg-brand-blue-deep px-4 py-2 text-white shadow-sm transition hover:shadow-md"
              >
                Get started
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
