import { useEffect, useState } from "react";
import { api } from "../api/client";
import KundliChart from "./KundliChart";
import LoadingState from "./LoadingState";
import ErrorState from "./ErrorState";

export default function DivisionalCharts({ profileId, available }) {
  const [activeKey, setActiveKey] = useState(available[0]?.key);
  const [chartsByKey, setChartsByKey] = useState({});
  const [error, setError] = useState("");

  useEffect(() => {
    if (!activeKey || chartsByKey[activeKey]) return;
    setError("");
    api
      .getVarga(profileId, activeKey)
      .then((data) => setChartsByKey((prev) => ({ ...prev, [activeKey]: data })))
      .catch((err) => setError(err.message || "Could not load this divisional chart."));
  }, [activeKey, profileId, chartsByKey]);

  const active = chartsByKey[activeKey];

  return (
    <div className="rounded-3xl bg-white/70 p-6 shadow-sm">
      <h2 className="mb-4 font-semibold text-brand-slate">Divisional Charts</h2>

      <div className="mb-4 flex flex-wrap gap-2">
        {available.map((v) => (
          <button
            key={v.key}
            onClick={() => setActiveKey(v.key)}
            className={`rounded-full px-4 py-1.5 text-sm font-medium transition ${
              activeKey === v.key ? "bg-brand-blue-deep text-white shadow-sm" : "bg-brand-blue/30 text-brand-slate/70"
            }`}
          >
            {v.key} · {v.label}
          </button>
        ))}
      </div>

      <ErrorState message={error} />

      {!active && !error && <LoadingState label="Calculating..." />}

      {active && (
        <div className="grid gap-6 md:grid-cols-2">
          <div>
            <p className="mb-3 text-xs text-brand-slate/50">{active.significance}</p>
            <KundliChart chart={active} />
          </div>
          <div>
            <p className="mb-2 text-sm font-medium text-brand-slate">
              {active.label} Lagna: <span className="text-brand-blue-deep">{active.lagna}</span>
            </p>
            <ul className="space-y-1 text-sm text-brand-slate/70">
              {active.planets.map((p) => (
                <li key={p.name} className="flex justify-between border-b border-brand-blue/10 py-1">
                  <span>{p.name}</span>
                  <span>
                    {p.sign} · house {p.house}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
