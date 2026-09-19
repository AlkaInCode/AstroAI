import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import { api } from "../api/client";
import LoadingState from "../components/LoadingState";
import ErrorState from "../components/ErrorState";

// Entry point for /dashboard with no profile id yet -- sends the customer
// straight to their one Kundli, to the clients list if they have several
// (e.g. family members), or to profile creation if this is their first visit.
export default function DashboardRedirect() {
  const [target, setTarget] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .listProfiles()
      .then((profiles) => {
        if (profiles.length === 0) setTarget("/create-profile");
        else if (profiles.length === 1) setTarget(`/dashboard/${profiles[0].id}`);
        else setTarget("/clients");
      })
      .catch((err) => setError(err.message || "Could not load your profiles."));
  }, []);

  if (error) return <ErrorState message={error} />;
  if (!target) return <LoadingState />;
  return <Navigate to={target} replace />;
}
