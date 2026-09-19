import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import LoadingState from "../components/LoadingState";
import ErrorState from "../components/ErrorState";

export default function Clients() {
  const [profiles, setProfiles] = useState(null);
  const [query, setQuery] = useState("");
  const [error, setError] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [editingName, setEditingName] = useState("");

  useEffect(() => {
    loadProfiles();
  }, []);

  function loadProfiles() {
    api
      .listProfiles()
      .then(setProfiles)
      .catch((err) => setError(err.message || "Could not load your profiles."));
  }

  async function handleDelete(profileId, name) {
    if (!window.confirm(`Delete ${name}'s profile? This removes their chart, numerology and chat history too.`)) return;
    try {
      await api.deleteProfile(profileId);
      setProfiles((prev) => prev.filter((p) => p.id !== profileId));
    } catch (err) {
      setError(err.message || "Could not delete this profile.");
    }
  }

  function startEditing(profile) {
    setEditingId(profile.id);
    setEditingName(profile.full_name);
  }

  async function saveEditing(profileId) {
    try {
      const updated = await api.updateProfile(profileId, { full_name: editingName });
      setProfiles((prev) => prev.map((p) => (p.id === profileId ? updated : p)));
      setEditingId(null);
    } catch (err) {
      setError(err.message || "Could not update this profile.");
    }
  }

  if (error) return <ErrorState message={error} />;
  if (!profiles) return <LoadingState label="Loading your clients..." />;

  const filtered = profiles.filter((p) => {
    const haystack = `${p.full_name} ${p.city} ${p.country}`.toLowerCase();
    return haystack.includes(query.toLowerCase());
  });

  return (
    <div className="mx-auto max-w-4xl px-6 py-10">
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <h1 className="text-2xl font-bold text-brand-slate">My Clients</h1>
        <Link
          to="/create-profile"
          className="rounded-full bg-brand-blue-deep px-5 py-2 text-sm font-semibold text-white shadow-sm transition hover:shadow-md"
        >
          + Add New Profile
        </Link>
      </div>

      <input
        type="text"
        placeholder="Search by name, city or country..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="mb-6 w-full rounded-xl border border-brand-blue/60 bg-white px-4 py-2.5 text-brand-slate outline-none focus:border-brand-blue-deep focus:ring-2 focus:ring-brand-blue/50"
      />

      {filtered.length === 0 ? (
        <div className="rounded-2xl bg-white/70 p-6 text-center text-sm text-brand-slate/60 shadow-sm">
          {profiles.length === 0 ? "No profiles yet." : "No profiles match your search."}
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((profile) => (
            <div key={profile.id} className="flex items-center justify-between gap-4 rounded-2xl bg-white/70 p-5 shadow-sm">
              <div className="min-w-0 flex-1">
                {editingId === profile.id ? (
                  <div className="flex items-center gap-2">
                    <input
                      type="text"
                      value={editingName}
                      onChange={(e) => setEditingName(e.target.value)}
                      className="rounded-lg border border-brand-blue/50 bg-white px-3 py-1.5 text-sm outline-none focus:border-brand-blue-deep"
                    />
                    <button
                      onClick={() => saveEditing(profile.id)}
                      className="rounded-full bg-brand-blue-deep px-3 py-1.5 text-xs font-semibold text-white"
                    >
                      Save
                    </button>
                    <button onClick={() => setEditingId(null)} className="text-xs text-brand-slate/50">
                      Cancel
                    </button>
                  </div>
                ) : (
                  <button onClick={() => startEditing(profile)} className="font-semibold text-brand-slate hover:underline">
                    {profile.full_name}
                  </button>
                )}
                <p className="mt-1 truncate text-xs text-brand-slate/50">
                  Born {profile.dob} · {profile.city}
                  {profile.state ? `, ${profile.state}` : ""}, {profile.country}
                </p>
              </div>
              <div className="flex shrink-0 items-center gap-2">
                <Link
                  to={`/dashboard/${profile.id}`}
                  className="rounded-full bg-brand-blue/40 px-4 py-1.5 text-xs font-semibold text-brand-slate transition hover:bg-brand-blue/60"
                >
                  View Kundli
                </Link>
                <button
                  onClick={() => handleDelete(profile.id, profile.full_name)}
                  className="rounded-full bg-brand-pink/50 px-4 py-1.5 text-xs font-semibold text-brand-slate transition hover:bg-brand-pink/70"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
