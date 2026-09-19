import { useState } from "react";
import LocationSearch from "./LocationSearch";
import ErrorState from "./ErrorState";
import { Field, SubmitButton } from "./FormPrimitives";
import { COMMON_TIMEZONES, guessTimezone } from "../utils/timezones";

const initialState = {
  full_name: "",
  gender: "female",
  dob: "",
  birth_time: "",
  timezone: "UTC",
};

export default function BirthDetailsForm({ onSubmit, isSubmitting, error }) {
  const [form, setForm] = useState(initialState);
  const [location, setLocation] = useState(null);
  const [validationError, setValidationError] = useState("");

  function update(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  function handleLocationSelect(resolved) {
    setLocation(resolved);
    update("timezone", guessTimezone(resolved.longitude));
  }

  function handleSubmit(e) {
    e.preventDefault();
    if (!location) {
      setValidationError("Please pick your birth place from the search results.");
      return;
    }
    setValidationError("");
    onSubmit({ ...form, ...location });
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <Field label="Full name" value={form.full_name} onChange={(v) => update("full_name", v)} required />

      <label className="block text-sm font-medium text-brand-slate/80">
        Gender
        <select
          value={form.gender}
          onChange={(e) => update("gender", e.target.value)}
          className="mt-1 w-full rounded-xl border border-brand-blue/60 bg-white px-4 py-2.5 text-brand-slate outline-none focus:border-brand-blue-deep focus:ring-2 focus:ring-brand-blue/50"
        >
          <option value="female">Female</option>
          <option value="male">Male</option>
          <option value="non_binary">Non-binary</option>
          <option value="prefer_not_to_say">Prefer not to say</option>
        </select>
      </label>

      <div className="grid grid-cols-2 gap-4">
        <Field label="Date of birth" type="date" value={form.dob} onChange={(v) => update("dob", v)} required />
        <Field label="Exact birth time" type="time" value={form.birth_time} onChange={(v) => update("birth_time", v)} required />
      </div>
      <p className="-mt-3 text-xs text-brand-slate/50">
        Exact birth time matters — it determines your Lagna (Ascendant) and house placements.
      </p>

      <LocationSearch onSelect={handleLocationSelect} />
      {location && (
        <div className="rounded-xl bg-brand-lavender/40 px-4 py-2 text-xs text-brand-slate/70">
          {location.city}, {location.state ? `${location.state}, ` : ""}
          {location.country} · {location.latitude.toFixed(3)}, {location.longitude.toFixed(3)}
        </div>
      )}

      <label className="block text-sm font-medium text-brand-slate/80">
        Timezone
        <select
          value={form.timezone}
          onChange={(e) => update("timezone", e.target.value)}
          className="mt-1 w-full rounded-xl border border-brand-blue/60 bg-white px-4 py-2.5 text-brand-slate outline-none focus:border-brand-blue-deep focus:ring-2 focus:ring-brand-blue/50"
        >
          {COMMON_TIMEZONES.map((tz) => (
            <option key={tz} value={tz}>
              {tz}
            </option>
          ))}
        </select>
      </label>

      <ErrorState message={validationError || error} />
      <SubmitButton isSubmitting={isSubmitting} label="Generate my Kundli" />
    </form>
  );
}
