export default function YogaCard({ yoga }) {
  return (
    <div className="rounded-2xl bg-white/70 p-5 shadow-sm">
      <div className="flex items-center justify-between gap-2">
        <h3 className="font-semibold text-brand-slate">{yoga.name}</h3>
        <span className="rounded-full bg-brand-lavender/60 px-3 py-0.5 text-xs font-medium text-brand-slate/70">
          {yoga.type}
        </span>
      </div>
      <p className="mt-1 text-xs text-brand-slate/50">{yoga.planets.join(" + ")}</p>
      <p className="mt-2 text-sm leading-relaxed text-brand-slate/70">{yoga.description}</p>
      {yoga.knowledge && (
        <p className="mt-3 border-t border-brand-blue/20 pt-2 text-xs italic leading-relaxed text-brand-slate/50">
          {yoga.knowledge}
        </p>
      )}
    </div>
  );
}
