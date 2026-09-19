export default function PlanetTable({ planets }) {
  return (
    <div className="overflow-hidden rounded-2xl bg-white/70 shadow-sm">
      <table className="w-full text-left text-sm">
        <thead className="bg-brand-blue/30 text-xs uppercase tracking-wide text-brand-slate/60">
          <tr>
            <th className="px-4 py-3">Planet</th>
            <th className="px-4 py-3">Sign</th>
            <th className="px-4 py-3">House</th>
            <th className="px-4 py-3">Degree</th>
            <th className="px-4 py-3">Retrograde</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-brand-blue/20">
          {planets.map((planet) => (
            <tr key={planet.name}>
              <td className="px-4 py-2.5 font-medium text-brand-slate">{planet.name}</td>
              <td className="px-4 py-2.5">{planet.sign}</td>
              <td className="px-4 py-2.5">{planet.house}</td>
              <td className="px-4 py-2.5">{planet.degree}°</td>
              <td className="px-4 py-2.5">{planet.retrograde ? "Yes" : "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
