export default function LifeAreaCards({ areas }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {areas.map((area) => (
        <div key={area.title} className="rounded-2xl bg-white/70 p-5 shadow-sm">
          <div className="flex items-center gap-2">
            <span className="text-xl">{area.icon}</span>
            <h3 className="font-semibold text-brand-slate">{area.title}</h3>
          </div>
          <p className="mt-2 text-sm leading-relaxed text-brand-slate/70">{area.text}</p>
          {area.knowledge && (
            <p className="mt-3 border-t border-brand-blue/20 pt-2 text-xs italic leading-relaxed text-brand-slate/50">
              {area.knowledge}
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
