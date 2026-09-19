import { useEffect, useRef, useState } from "react";

/**
 * Free-text city search backed by OpenStreetMap Nominatim (no API key required).
 * Resolves a typed place into a concrete city/state/country + lat/long.
 * Swap this for a paid geocoding provider later without touching the parent form --
 * it only needs onSelect({ city, state, country, latitude, longitude }).
 */
export default function LocationSearch({ onSelect }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [selectedLabel, setSelectedLabel] = useState("");
  const debounceRef = useRef(null);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (query.trim().length < 3 || query === selectedLabel) {
      setResults([]);
      return;
    }
    debounceRef.current = setTimeout(() => search(query), 400);
    return () => clearTimeout(debounceRef.current);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [query]);

  async function search(text) {
    setIsSearching(true);
    try {
      const url = `https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&limit=5&q=${encodeURIComponent(text)}`;
      const response = await fetch(url, { headers: { Accept: "application/json" } });
      const data = await response.json();
      setResults(data);
    } catch {
      setResults([]);
    } finally {
      setIsSearching(false);
    }
  }

  function handlePick(place) {
    const address = place.address || {};
    const city = address.city || address.town || address.village || address.county || place.display_name;
    const label = place.display_name;
    setQuery(label);
    setSelectedLabel(label);
    setResults([]);
    onSelect({
      birth_place: label,
      city,
      state: address.state || "",
      country: address.country || "",
      latitude: parseFloat(place.lat),
      longitude: parseFloat(place.lon),
    });
  }

  return (
    <div className="relative">
      <label className="block text-sm font-medium text-brand-slate/80">
        Birth place
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Start typing a city..."
          required
          className="mt-1 w-full rounded-xl border border-brand-blue/60 bg-white px-4 py-2.5 text-brand-slate outline-none transition focus:border-brand-blue-deep focus:ring-2 focus:ring-brand-blue/50"
        />
      </label>
      {isSearching && <p className="mt-1 text-xs text-brand-slate/50">Searching...</p>}
      {results.length > 0 && (
        <ul className="absolute z-20 mt-1 w-full overflow-hidden rounded-xl border border-brand-blue/40 bg-white shadow-lg">
          {results.map((place) => (
            <li key={place.place_id}>
              <button
                type="button"
                onClick={() => handlePick(place)}
                className="block w-full px-4 py-2 text-left text-sm text-brand-slate hover:bg-brand-blue/20"
              >
                {place.display_name}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
