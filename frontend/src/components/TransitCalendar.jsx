import { useEffect, useState } from "react";
import { api } from "../api/client";
import LoadingState from "./LoadingState";
import ErrorState from "./ErrorState";

function today() {
  // Local calendar date, not toISOString()'s UTC date -- those disagree for
  // roughly a third of the world's timezones at any given moment.
  const now = new Date();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${now.getFullYear()}-${month}-${day}`;
}

export default function TransitCalendar({ profileId }) {
  const [selectedDate, setSelectedDate] = useState(today());
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    setError("");
    api
      .getTransits(profileId, selectedDate)
      .then(setData)
      .catch((err) => setError(err.message || "Could not load transits for this date."))
      .finally(() => setIsLoading(false));
  }, [profileId, selectedDate]);

  return (
    <div className="rounded-3xl bg-white/70 p-6 shadow-sm">
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <h2 className="font-semibold text-brand-slate">Current Transits</h2>
        <label className="flex items-center gap-2 text-sm text-brand-slate/70">
          Date
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="rounded-lg border border-brand-blue/50 bg-white px-3 py-1.5 text-sm text-brand-slate outline-none focus:border-brand-blue-deep"
          />
        </label>
      </div>

      <ErrorState message={error} />
      {isLoading && <LoadingState label="Checking the sky..." />}

      {data && !isLoading && (
        <>
          {(data.sade_sati.active || data.jupiter_return) && (
            <div className="mb-4 flex flex-wrap gap-2">
              {data.sade_sati.active && (
                <span className="rounded-full bg-brand-pink/50 px-4 py-1.5 text-xs font-medium text-brand-slate">
                  Sade Sati — {data.sade_sati.phase}
                </span>
              )}
              {data.jupiter_return && (
                <span className="rounded-full bg-brand-lavender/60 px-4 py-1.5 text-xs font-medium text-brand-slate">
                  Jupiter Return
                </span>
              )}
            </div>
          )}

          <div className="overflow-x-auto rounded-2xl bg-white/70">
            <table className="w-full text-left text-sm">
              <thead className="bg-brand-blue/30 text-xs uppercase tracking-wide text-brand-slate/60">
                <tr>
                  <th className="px-4 py-3">Planet</th>
                  <th className="px-4 py-3">Sign</th>
                  <th className="px-4 py-3">Degree</th>
                  <th className="px-4 py-3">Retrograde</th>
                  <th className="px-4 py-3">House from Lagna</th>
                  <th className="px-4 py-3">House from Moon</th>
                  <th className="px-4 py-3">Dignity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-brand-blue/20">
                {data.transits.map((t) => (
                  <tr key={t.name}>
                    <td className="px-4 py-2.5 font-medium text-brand-slate">{t.name}</td>
                    <td className="px-4 py-2.5">{t.sign}</td>
                    <td className="px-4 py-2.5">{t.degree}°</td>
                    <td className="px-4 py-2.5">{t.retrograde ? "Yes" : "—"}</td>
                    <td className="px-4 py-2.5">{t.house_from_lagna}</td>
                    <td className="px-4 py-2.5">{t.house_from_moon}</td>
                    <td className="px-4 py-2.5">{t.exalted ? "Exalted" : t.debilitated ? "Debilitated" : "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
