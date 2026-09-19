import { useState } from "react";

function formatDate(isoString) {
  return new Date(isoString).toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}

function CurrentTrailChip({ label, planet }) {
  return (
    <div className="rounded-2xl bg-white/80 px-4 py-3 text-center shadow-sm">
      <div className="text-[11px] uppercase tracking-wide text-brand-slate/50">{label}</div>
      <div className="mt-1 font-semibold text-brand-slate">{planet || "—"}</div>
    </div>
  );
}

export default function DashaTimeline({ dasha }) {
  const [expanded, setExpanded] = useState(() => new Set());

  function toggle(planet, index) {
    const key = `${planet}-${index}`;
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }

  return (
    <div className="rounded-3xl bg-white/70 p-6 shadow-sm">
      <h2 className="mb-4 font-semibold text-brand-slate">Vimshottari Dasha</h2>

      <div className="grid grid-cols-3 gap-3">
        <CurrentTrailChip label="Mahadasha" planet={dasha.current_mahadasha?.planet} />
        <CurrentTrailChip label="Antardasha" planet={dasha.current_antardasha?.planet} />
        <CurrentTrailChip label="Pratyantardasha" planet={dasha.current_pratyantardasha?.planet} />
      </div>
      {dasha.current_pratyantardasha && (
        <p className="mt-3 text-center text-xs text-brand-slate/50">
          Current period runs until {formatDate(dasha.current_pratyantardasha.end)}
        </p>
      )}

      <h3 className="mb-2 mt-6 text-sm font-semibold text-brand-slate/70">Full Timeline</h3>
      <div className="max-h-80 space-y-2 overflow-y-auto pr-1">
        {dasha.mahadasha_sequence.map((md, i) => {
          const key = `${md.planet}-${i}`;
          const isOpen = expanded.has(key);
          const isCurrent = dasha.current_mahadasha?.start === md.start;
          return (
            <div key={key} className="rounded-xl bg-brand-lavender/20">
              <button
                type="button"
                onClick={() => toggle(md.planet, i)}
                className={`flex w-full items-center justify-between rounded-xl px-4 py-2.5 text-left text-sm ${
                  isCurrent ? "bg-brand-blue/40 font-semibold" : ""
                }`}
              >
                <span className="text-brand-slate">
                  {md.planet} {isCurrent && <span className="text-xs text-brand-blue-deep">(current)</span>}
                </span>
                <span className="text-xs text-brand-slate/50">
                  {formatDate(md.start)} – {formatDate(md.end)}
                </span>
              </button>
              {isOpen && (
                <div className="space-y-1 px-4 pb-3">
                  {md.antardashas.map((ad, j) => {
                    const isCurrentAd = dasha.current_antardasha?.start === ad.start && isCurrent;
                    return (
                      <div
                        key={j}
                        className={`flex items-center justify-between rounded-lg px-3 py-1.5 text-xs ${
                          isCurrentAd ? "bg-brand-pink/40 font-medium" : "bg-white/60"
                        }`}
                      >
                        <span className="text-brand-slate/80">{ad.planet}</span>
                        <span className="text-brand-slate/50">
                          {formatDate(ad.start)} – {formatDate(ad.end)}
                        </span>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
