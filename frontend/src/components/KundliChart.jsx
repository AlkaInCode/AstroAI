// Classic North Indian Vedic chart: an outer square, both diagonals, and an
// inner diamond connecting the midpoints of the four sides. Together these
// lines carve out the 12 house regions. House 1 is fixed at the top-center
// and the rest run clockwise, per the North Indian convention.
const HOUSE_LABEL_POSITIONS = {
  1: { x: 50, y: 20 },
  2: { x: 27, y: 12 },
  3: { x: 12, y: 27 },
  4: { x: 20, y: 50 },
  5: { x: 12, y: 73 },
  6: { x: 27, y: 88 },
  7: { x: 50, y: 80 },
  8: { x: 73, y: 88 },
  9: { x: 88, y: 73 },
  10: { x: 80, y: 50 },
  11: { x: 88, y: 27 },
  12: { x: 73, y: 12 },
};

export default function KundliChart({ chart }) {
  const planetAbbrevByHouse = Array.from({ length: 12 }, (_, i) => i + 1).reduce((acc, house) => {
    acc[house] = chart.planets.filter((p) => p.house === house).map((p) => p.name.slice(0, 2));
    return acc;
  }, {});

  return (
    <svg viewBox="0 0 100 100" className="mx-auto w-full max-w-sm drop-shadow-sm">
      <rect x="2" y="2" width="96" height="96" fill="white" stroke="#8fc6f0" strokeWidth="1.5" rx="4" />
      <line x1="2" y1="2" x2="98" y2="98" stroke="#8fc6f0" strokeWidth="1" />
      <line x1="98" y1="2" x2="2" y2="98" stroke="#8fc6f0" strokeWidth="1" />
      <polygon points="50,2 98,50 50,98 2,50" fill="none" stroke="#8fc6f0" strokeWidth="1" />

      {Object.entries(HOUSE_LABEL_POSITIONS).map(([house, pos]) => (
        <g key={house}>
          <text x={pos.x} y={pos.y - 3} textAnchor="middle" fontSize="4" fill="#4a5568" opacity="0.5">
            {house}
          </text>
          <text x={pos.x} y={pos.y + 3} textAnchor="middle" fontSize="4.2" fontWeight="600" fill="#4a5568">
            {planetAbbrevByHouse[house].join(" ") || ""}
          </text>
        </g>
      ))}
    </svg>
  );
}
