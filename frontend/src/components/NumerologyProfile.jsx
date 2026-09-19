const CARDS = [
  { key: "life_path", title: "Life Path", icon: "🧭" },
  { key: "expression", title: "Expression", icon: "🌟" },
  { key: "soul_urge", title: "Soul Urge", icon: "💗" },
  { key: "personality", title: "Personality", icon: "🎭" },
  { key: "chaldean_destiny", title: "Chaldean Destiny", icon: "🔮" },
];

export default function NumerologyProfile({ numerology }) {
  return (
    <div className="rounded-3xl bg-white/70 p-6 shadow-sm">
      <h2 className="mb-1 font-semibold text-brand-slate">Numerology</h2>
      <p className="mb-4 text-xs text-brand-slate/50">Calculated from {numerology.full_name_used} and your date of birth.</p>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {CARDS.map(({ key, title, icon }) => {
          const entry = numerology[key];
          return (
            <div key={key} className="rounded-2xl bg-brand-lavender/20 p-5">
              <div className="flex items-center gap-2">
                <span className="text-xl">{icon}</span>
                <h3 className="text-sm font-semibold text-brand-slate">{title}</h3>
              </div>
              <div className="mt-2 text-3xl font-bold text-brand-blue-deep">{entry.number}</div>
              {entry.knowledge && (
                <p className="mt-2 text-xs leading-relaxed text-brand-slate/60">{entry.knowledge}</p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
